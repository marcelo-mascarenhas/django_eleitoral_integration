import django_rq
import json
import datetime


from .models import ExecutionHandler, MachineLearningMethod, Tweet

from integrated.settings import COLLECTOR_JOB_ID, CONFIGURATION_PATH, TWITTER_FILE_NAME, ELECT_FILE_NAME
from .monitor.source.identificacao.identificacao import METODOS_POSSIVEIS


def doesJobExists(job_name):
  task_queue = django_rq.get_queue()
  job = task_queue.fetch_job(job_id=job_name)
  if job == None:
    return False
  else:
    return True
  
def getJob(job_name):
  job = (django_rq.get_queue()).fetch_job(job_id=job_name)
  return job


  
def executionObjectSetter(run=True):
  """
  Set ExecutionHandler object to True or false, to control the flow of execution.
  """
  process = None
  try:
    process = ExecutionHandler.objects.get(process_id=COLLECTOR_JOB_ID)
    process.continue_run = run
    process.save()
    
  except ExecutionHandler.DoesNotExist:
    process = ExecutionHandler(process_id=COLLECTOR_JOB_ID, continue_run=run)
    process.save()
    
    
def createMachineLearningMethods():
  for name in METODOS_POSSIVEIS:
    if not MachineLearningMethod.objects.filter(method=name).exists():
      obj = MachineLearningMethod(method=name)
      obj.save()

class FilterHandler():
  
  def create_filter_attributes(self, request):
    """
    Create all fields that will be used in the filter variable.
    
    """
    
    filters = {}
    
    filters['search_bar'] = request.GET.get('search_bar') if request.GET.get('search_bar') != None else ""
    
    filters['max_date'] = request.GET.get('data_max') if request.GET.get('data_max') != None else ""
    
    filters['min_date'] = request.GET.get('data_min') if request.GET.get('data_min') != None else ""  
    
    filters['min_score'] = request.GET.get('score_min') if request.GET.get('min_value') != None else 0
    
    filters['max_score'] = request.GET.get('score_max') if request.GET.get('max_value') != None else 1
    
    filters['sort_by'] = request.GET.get('mtd') if request.GET.get('mtd') != None else "electoral_score"
    
    return filters

  def getFilteredTwitterList(self, filters):
    """
    Aplica todos os filtros nos Tweet objects, considerando os valores dos filtros passados.
    
    """
    
    twitter_list = Tweet.objects.all().order_by(filters['sort_by']).reverse()
    
    #Nested filtering.
    if filters['search_bar'] != "":
      twitter_list = twitter_list.filter(text__icontains=filters['search_bar'])
    
    if filters['max_date'] != "" and filters['min_date'] != "":
      
      inferior_range = [int(x) for x in filters['min_date'].split('/')]
      
      superior_range = [int(x) for x in filters['max_date'].split('/')]
      #Format the data DD/MM/YYYY to YYYY/MM/DD
      twitter_list = twitter_list.filter(
        created_at__range=[datetime.date(inferior_range[2], inferior_range[1], inferior_range[0]), 
          datetime.date(superior_range[2], superior_range[1], superior_range[0])])
    
    
    twitter_list = twitter_list.filter(electoral_score__range=[filters['min_score'], filters['max_score']])
    
    
    return twitter_list
    

class FileHandler():
  
  def getTwitterConfigurationFile(self):
    with open(f'{CONFIGURATION_PATH}/{TWITTER_FILE_NAME}', 'r') as f:
      file_information = json.load(f)
      
    file_information = json.dumps(file_information)
    return file_information
  
  def saveInformationFiles(self, twitter_data, selected_method):
    """
    Save the information in Twitter/Electoral files.
    """
    td = json.loads(twitter_data)
    
    self.__saveTwitterFile(td)     
    self.__saveElectoralFile(selected_method)
  
  
  def selectedMlMethod(self):
    
    with open(f'{CONFIGURATION_PATH}/{ELECT_FILE_NAME}', 'r') as f:
      file_information = json.load(f)
    method = file_information['metodo_selecionado']
    
    return method
  

  def __saveTwitterFile(self, data):
    with open(f'{CONFIGURATION_PATH}/{TWITTER_FILE_NAME}', 'r+') as f:
      file_information = json.load(f)
            
      for field in data:
        file_information[field] = data[field]
      
      f.seek(0)
      f.truncate()
      json.dump(file_information, f, indent=5, ensure_ascii=False)
      f.flush()
      f.close()
      
  def __saveElectoralFile(self,data):
    with open(f'{CONFIGURATION_PATH}/{ELECT_FILE_NAME}', 'r+') as f:
      file_information = json.load(f)
      
      file_information["metodo_selecionado"] = data
      
      f.seek(0)
      f.truncate()
      json.dump(file_information, f, indent=7, ensure_ascii=False)  
      f.flush()
      f.close()
      
    