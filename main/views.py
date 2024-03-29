from shutil import move
from unicodedata import name
import django_rq
import time
import itertools
import os

from datetime import timedelta
from django.utils import timezone

from django.db.models import Count
from django.views.generic.edit import FormView
from django.db.models import Avg
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


from .plots.wordCloud import generateWordCloud
from .plots.co_occurr_net import generateCoOccurrence
from .monitor.source.identificacao.utils.text_processor import TextProcessor 
from integrated.settings import BASE_DIR, COLLECTOR_JOB_NAME, MAX_INT, ERROR_MSG, HTML_PATH

from main.monitor.caller import django_caller
from main.utils import *

from .forms import *
from .models import *

def index(request):
  """
  Load the dashboard and the initial configuration.
  
  """
  createExecutionHandler()
  createMachineLearningMethods()
  #Number of tweets in the database.
  tt = Tweet.objects.count()
  
  #Number of different users in the database.
  authors = Tweet.objects.values('author_id').annotate(Count('author_id')).order_by('-author_id__count')
  number_of_authors = authors.count()
  #Tweets retrieved in the last week
  london_time = timezone.now() + timedelta(hours=3)
  tlw = Tweet.objects.filter(created_at__range=[london_time - timedelta(days=7), london_time])
  tld = Tweet.objects.filter(created_at__range=[london_time - timedelta(days=1), london_time])
  tld = tld.count()
  tlw = tlw.count()
  running = dje(COLLECTOR_JOB_NAME)

  avg_score = None
  try:
    #Average score of the database.
    avg_score = Tweet.objects.aggregate(Avg('electoral_score')) 
    avg_score = round(avg_score['electoral_score__avg'], 5)
  except:
    avg_score = 0
 
  return render(request, 'main/index.html', {
    'total_tweets' :tt,
    'avg_score': avg_score,
    'n_of_authors': number_of_authors,
    'n_of_tlw': tlw,
    'n_of_tld': tld,
    'authors': authors,
    'running': running
  })
  
@user_passes_test(lambda u: u.is_superuser)
def execution(request, status=None):
  running = doesJobExists(COLLECTOR_JOB_NAME)
  
  if running == True:
    collector_job = getJob(COLLECTOR_JOB_NAME)
    condition = collector_job.get_status()
    print(condition)
    
    if condition == "failed":
      
      running = False
      condition = collector_job.exc_info
      status = condition if ERROR_MSG not in condition else None
      
  return render(request, 'main/execucao.html', {
    'running': running,
    'error_msg': status
  })

@user_passes_test(lambda u: u.is_superuser)
def executeCollector(request):
  queue = django_rq.get_queue(autocommit=True, default_timeout=MAX_INT, is_async=True)
  if not queue.is_empty():
    queue.empty()
  
  queue.enqueue(django_caller, job_id=COLLECTOR_JOB_NAME, result_ttl=MAX_INT)
  executionObjectSetter()
      
  return redirect(execution)

@user_passes_test(lambda u: u.is_superuser)
def stopCollector(request):
  collector_job = getJob(COLLECTOR_JOB_NAME)
  
  collector_job.delete()
  executionObjectSetter(run=False)
  
  time.sleep(1)
  return redirect(execution)


# class GetScores(APIView):
#   authentication_classes = []
#   permission_classes = []
  
#   def get(self, request):
#     pass



# class ListUsers(APIView):
#   authentication_classes = []
#   permission_classes = []

#   def get(self, request):
#     NUMBER_OF_AUTHORS = 15

#     score = request.GET.get('score')
#     verified = request.GET.get('verified')
    
#     check = True if verified == "True" else False
    
#     users =  Tweet.objects.filter(electoral_score__gte = score)
    
#     if check:
#       users = users.filter(author_id__user_verified=check)
    
#     users = users.values('author_id').annotate(Count('author_id')).order_by('-author_id__count')[:NUMBER_OF_AUTHORS]
    
#     json_data = {}
#     for item in users.iterator():
#       json_data[item['author_id']] = item['author_id__count']
    
#     return Response(json_data)

class Configuration(FormView):
  """
  Stores the methods related to the configuration page. Also contains the class object reponsible
  for the manipulation of the configuration (JSON) files, located at /monitor/configurations/...
  
  """
  
  template_name = 'main/configuration.html'
  
  config_forms = ConfigurationForm()   
  
  fih = FileHandler()
  
  
  @method_decorator(user_passes_test(lambda u: u.is_superuser))
 
  def get(self, request, error_msg=None):
    running = dje(COLLECTOR_JOB_NAME)
    
    file_information = self.fih.getTwitterConfigurationFile()
    
    selected = self.fih.selectedMlMethod()
    print(self.fih.selectedMlMethod())
    
    return render(request, self.template_name, {
      'json_information': file_information,
      'ml_methods': self.config_forms,
      'error': error_msg,
      'selected': selected,
      'running': running
    })
  
  def post(self, request):
    form = ConfigurationForm(request.POST)
    
    if form.is_valid():
      error = None
      try:
        print(form.cleaned_data['twitter_configuration'], form.cleaned_data['mtd'])
        
        self.fih.saveInformationFiles(form.cleaned_data['twitter_configuration'], \
          form.cleaned_data['mtd'])
        
      except Exception as e:
        error = e
        print(error)
        
      return self.get(request, error_msg=error)
    
    else:
      return HttpResponseRedirect("Ooooops... Something went wrong.")


class DataAnalysis(FormView):
  
  path = 'main/analise.html'
  
  filter_by = OrderBy()
  
  filt_obj = FilterHandler()

  PAG_NUMBER = 10
  
  def get(self, request):
    running = dje(COLLECTOR_JOB_NAME)

    parameters, filters, tweet_list = self.__getParameters(request)

    empty_query = True if tweet_list.count() == 0 else False
    
    #Create the paginator
    paginator = Paginator(tweet_list, self.PAG_NUMBER)
    
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)
    return render(request, self.path,
      {'tweets': page_obj,
     'filtros': self.filter_by,
     'search': filters['search_bar'],
     'data_max': filters['max_date'],
     'data_min': filters['min_date'],
     'min_score': filters['min_score'],
     'max_score': filters['max_score'],
     'sort_by': filters['sort_by'],
     'parameters': parameters,
     'empty_query': empty_query,
     'running': running
    })
  
  def __getParameters(self, request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    filters = self.filt_obj.create_filter_attributes(request)
    
    tweet_list = self.filt_obj.getFilteredTwitterList(filters)

  
    return parameters, filters, tweet_list
  

class GraphPlots(DataAnalysis):
  
  path = "main/graph_plot.html"
  path2 = "main/cooccurr.html"
  plot_type = ""
  
  obj = TextProcessor()
  
  NUMBER_OF_TWEETS = 1000
  
  def get(self, request):
    parameters, filters, tweet_list = self._DataAnalysis__getParameters(request)
    image = None
    
    tweet_list = tweet_list[:self.NUMBER_OF_TWEETS]
    text = tweet_list.values_list("text", flat=True)    
    text = self.obj.text_process(text)

    if self.plot_type == "cloudWord":      
      final_text = list(itertools.chain.from_iterable(text))
    
      final_text = " ".join(final_text)
      
      image = generateWordCloud(final_text)
    
      return render(request, self.path, {'imagem': image})


    if self.plot_type == "coOccurrence":
      #Construct bigrams to generate the co-occurrence graph.
      bigrams = self.obj.construct_bigrams(text)
      
      file_name = (HTML_PATH.split('/'))[-1]
      
      generateCoOccurrence(bigrams, file_name)
      #Move the HTML from the base directory to the HTML folder.
      shutil.move(os.path.join(BASE_DIR, file_name), HTML_PATH)
      return render(request, self.path2)

