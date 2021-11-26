from django_rq.decorators import job
from integrated.settings import CONFIGURATION_PATH, MODEL_FILES_PATH
from .source.integrator import Integrator
import os

@job("default")
def django_caller():
  intobj = Integrator(CONFIGURATION_PATH, MODEL_FILES_PATH)
  intobj.streamTweets(classify=True)  


  

  
  