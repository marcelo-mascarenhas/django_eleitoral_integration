import django_rq

def does_JobExists(job_name):
  task_queue = django_rq.get_queue()
  job = task_queue.fetch_job(job_id=job_name)
  if job == None:
    return False
  else:
    return True
  
def getJob(job_name):
  job = (django_rq.get_queue()).fetch_job(job_id=job_name)
  return job