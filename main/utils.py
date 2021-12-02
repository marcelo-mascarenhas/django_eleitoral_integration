import django_rq
import json

from .models import ExecutionHandler, MachineLearningMethod
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


class FileHandler():
  def getTwitterConfigurationFile(self):
    with open(f'{CONFIGURATION_PATH}/{TWITTER_FILE_NAME}', 'r') as f:
      file_information = json.load(f)
      
    file_information = json.dumps(file_information)
    return file_information
  
  def saveTwitterConfigurationFile(self):
    pass
  
  
  def selectedMlMethod(self):
    
    with open(f'{CONFIGURATION_PATH}/{ELECT_FILE_NAME}', 'r') as f:
      file_information = json.load(f)
    method = file_information['metodo_selecionado']
    
    return method
  
       