from main.models import ExecutionHandler
from integrated.settings import COLLECTOR_JOB_ID

class Controller():
  """Class that control the exit of the collector when the user says so in the interface."""
  def __init__(self):
    self.__check_process()
  
  def __check_process(self):
    """
    Check if the object responsible to controll the execution of the collector exists in the database.
    If it exists, return it. If it doesn't exists, the function create it and return.
    
    """
    process = None
    try:
      process = ExecutionHandler.objects.get(process_id=COLLECTOR_JOB_ID)
    except ExecutionHandler.DoesNotExist:
      process = ExecutionHandler(process_id=COLLECTOR_JOB_ID, continue_run=True)
      process.save()
    except Exception as e:
      raise Exception(e)
    
    return process
  
  def shouldContinue(self):
    """Check if the object that manages the execution of the collector were set to false. If yes, reset the state of the object
    and quit the program.
    """
    
    process = self.__check_process()
    if process.continue_run == False:
      process.continue_run = True
      process.save()
      exit()