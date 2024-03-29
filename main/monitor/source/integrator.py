from textwrap import indent
from TwitterAPI.TwitterError import TwitterRequestError, TwitterConnectionError

from .twitter.twitter_collector import *

from .identificacao.identificacao import PropagandaIdentifier
from integrated.settings import TWITTER_FILE_NAME, ELECT_FILE_NAME 


from .db_interactors.db_saver import InformationHandler
from .db_interactors.controller import Controller

import json
import os


class Integrator():
  """
  Integrates Twitter Streaming Tool, the Electoral Propaganda Identifier, the Database Handler and control
  the flow of execution.
  """
  def __init__(self, cf, mp):
    
    self.configuration_path = cf if os.path.exists(cf) else None
    self.model_path = mp if os.path.exists(mp) else None
   
    if self.configuration_path == None or self.model_path == None:
      raise ValueError('Caminho para o arquivo de configuração ou diretório do modelo não existem.')
  
  def __createTwitterObject(self):
    """
      Open json configuration file and create TwitterCollector object
    
    """
    abs_path = os.path.join(self.configuration_path,TWITTER_FILE_NAME)
    
    with open(abs_path, 'r') as f:
      config_file = json.load(f)
    
    twitterobj = TwitterCollector(config_file)
    return twitterobj

  def __createIdObject(self):
    """
      Open json configuration file and create PropagandaIdentifier object.
    """
    abs_path = os.path.join(self.configuration_path, ELECT_FILE_NAME)
    
    with open(abs_path, 'r') as f:
      config_file = json.load(f)
    
    electobj = PropagandaIdentifier(config_file, self.model_path)
    return electobj  

  def streamTweets(self, classify=False):
    twitterobj = self.__createTwitterObject()
    
    #Create classify object and check if the parameters are valid#
    if classify:
      electobj = self.__createIdObject()
      veracity = electobj.is_parametros_validos()
      if not veracity:
        raise FileNotFoundError('Model files not found.')
    
    database_interactor = InformationHandler()
    controller_object = Controller()
    
    first_tweet, cursor = twitterobj.getStreamCursor()
    
    while True:
      try:
        first_tweet_data = first_tweet['data']
        print(json.dumps(first_tweet_data, indent=5))       
        if classify:
          
          if 'referenced_tweets' in first_tweet_data:
            for ref_tweet in first_tweet_data['referenced_tweets']:
              if 'id_hydrate' in ref_tweet:
                new_tt = ref_tweet['id_hydrate']
                
                new_tt['score'] = str(electobj.escreve_score_metodo(new_tt['text']))
                
                new_tt['utilized_method'] = electobj.metodo_selecionado

                author_info = None
                complete = True
                #Try to search informations of the author in the entities field.
                if 'mentions' in first_tweet_data['entities']:
                  for item in first_tweet_data['entities']['mentions']:
                    if item['id'] == new_tt['author_id'] and 'id_hydrate' in item:
                      author_info = item['id_hydrate']
                      break
                  
                if author_info == None:
                  author_info = {'id': new_tt['author_id']}
                  complete = False
                
                database_interactor.saveInformation(new_tt, author_info, complete)
            
            
          score = electobj.escreve_score_metodo(first_tweet_data['text'])
          
          first_tweet_data['score'] = str(score)
          
          first_tweet_data['utilized_method'] = electobj.metodo_selecionado
      
        
        database_interactor.saveInformation(first_tweet_data, first_tweet_data['author_id_hydrate'])
                
        controller_object.shouldContinue()
        first_tweet = cursor.__next__()

      except (TwitterConnectionError,TwitterRequestError) as e:
        #Calls getStreamCursor again that handles all exception.
        first_tweet, cursor = twitterobj.getStreamCursor()
        continue
      
      except Exception as e:
        raise Exception(f'{e}. Chora.')  