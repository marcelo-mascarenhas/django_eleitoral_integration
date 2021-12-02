import django_rq
import json
import time

from .forms import ConfigurationForm


from .models import *
from django.shortcuts import render, redirect
from integrated.settings import COLLECTOR_JOB_NAME, MAX_INT, ERROR_MSG
from main.monitor.caller import django_caller
from main.utils import *


def index(request):
  createMachineLearningMethods()
  return render(request, 'main/index.html')

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

def configuration(request):
  
  fih = FileHandler()
  file_information = fih.getTwitterConfigurationFile()
  config_forms = ConfigurationForm()
  config_forms.fields['mtd'].initial = fih.selectedMlMethod()
  
  return render(request, 'main/configuration.html', {
    'json_information': file_information,
    'ml_methods': config_forms
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