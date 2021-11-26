import django_rq

from .models import *
from django.shortcuts import render, redirect, reverse
from django_rq.decorators import job
from integrated.settings import COLLECTOR_JOB_NAME, COLLECTOR_JOB_ID
from main.monitor.caller import django_caller
from main.utils import *

MAX_INT = 100000000


def index(request):
  return render(request, 'main/index.html')

def execution(request, status=None):
  running = does_JobExists(COLLECTOR_JOB_NAME)
  
  if running == True:
    collector_job = getJob(COLLECTOR_JOB_NAME)
    status = collector_job.get_status()
    
    if status == "failed":
      running = False
      status = collector_job.exc_info
      print(status)
      
  return render(request, 'main/execucao.html', {
    'running': running,
  })


def executeCollector(request):
  queue = django_rq.get_queue(autocommit=True, default_timeout=MAX_INT, is_async=True)
  if not queue.is_empty():
    queue.empty()
  
  queue.enqueue(django_caller, job_id=COLLECTOR_JOB_NAME, result_ttl=MAX_INT)
  
  return redirect(execution)

def stopCollector(request):
  collector_job = getJob(COLLECTOR_JOB_NAME)
  
  collector_job.delete()
  process = None
  
  try:
    process = ExecutionHandler.objects.get(process_id=COLLECTOR_JOB_ID)
    process.continue_run = False
    process.save()
    
    
  except ExecutionHandler.DoesNotExist:
    process = ExecutionHandler(process_id=COLLECTOR_JOB_ID, continue_run=False)
    process.save()
  
  
  return redirect(execution)