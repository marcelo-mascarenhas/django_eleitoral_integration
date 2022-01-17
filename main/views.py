from pickle import NONE
from django.views.generic.base import View
import django_rq
import json
import time

from .forms import *

from django.views.generic.edit import FormView

from .models import *

from django.db.models import Avg

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.paginator import Paginator

from integrated.settings import COLLECTOR_JOB_NAME, MAX_INT, ERROR_MSG

from main.monitor.caller import django_caller
from main.utils import *



def index(request):
  """
  Load the dashboard and the initial configuration.
  
  """
  createMachineLearningMethods()
  
  tt = Tweet.objects.count()
  avg_score = NONE
  try:
    avg_score = Tweet.objects.aggregate(Avg('electoral_score')) 
    avg_score = round(avg_score['electoral_score__avg'], 5)
  except:
    avg_score = 0
 
  return render(request, 'main/index.html', {
    'total_tweets' :tt,
    'avg_score': avg_score,
    
  })

def data_analysis(request, sort_by=None):
  search = ""
  
  min_score = 0
  
  max_score = 1
  
  min_date = request.POST.get('min_value')
  
  max_date = request.POST.get('min_value')
  
  
  if request.method == "POST":
    
    search = request.POST.get('search_bar')
    
    min_score = request.POST.get('min_value')
    
    max_score = request.POST.get('max_value')
    
    min_date = request.POST.get('min_value')
    
    max_date = request.POST.get('min_value')
    
  filter_by = OrderBy()
  sort_by = "like_count" if sort_by == None else sort_by
    
  tweet_list = Tweet.objects.all().order_by(sort_by).reverse()
  
  paginator = Paginator(tweet_list, 10)
  
  page_number = request.GET.get('page')
  
  page_obj = paginator.get_page(page_number)

  return render(request, 'main/analise.html',
    {'tweets': page_obj,
     'filtros': filter_by            
    })
  
  
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

def executeCollector(request):
  queue = django_rq.get_queue(autocommit=True, default_timeout=MAX_INT, is_async=True)
  if not queue.is_empty():
    queue.empty()
  
  queue.enqueue(django_caller, job_id=COLLECTOR_JOB_NAME, result_ttl=MAX_INT)
  executionObjectSetter()
      
  return redirect(execution)

def stopCollector(request):
  collector_job = getJob(COLLECTOR_JOB_NAME)
  
  collector_job.delete()
  executionObjectSetter(run=False)
  
  time.sleep(1)
  return redirect(execution)

class Configuration(FormView):
  """
  Stores the methods related to the configuration page. Also contains the class object reponsible
  for the manipulation of the configuration (JSON) files, located at /monitor/configurations/...
  
  """
  
  template_name = 'main/configuration.html'
  
  config_forms = ConfigurationForm()   
  
  fih = FileHandler()
  
  def get(self, request, error_msg=None):    
    file_information = self.fih.getTwitterConfigurationFile()
    selected = self.fih.selectedMlMethod()

    
    print(self.fih.selectedMlMethod())
    
    return render(request, self.template_name, {
      'json_information': file_information,
      'ml_methods': self.config_forms,
      'error': error_msg,
      'selected': selected
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
