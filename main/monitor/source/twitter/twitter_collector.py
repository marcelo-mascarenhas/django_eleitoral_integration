import json
import time
import datetime as date

from retry import retry
from TwitterAPI import *
from TwitterAPI.TwitterAPI import HydrateType, OAuthType, TwitterResponse
from TwitterAPI.TwitterError import TwitterError
from .aux_functions import *



PLACE_FIELDS = 'country,name,place_type'
EXPANSIONS = 'referenced_tweets.id.author_id'
TWEET_FIELDS = 'author_id,created_at,public_metrics,text'
USER_FIELDS = 'created_at,description,id,name,username,verified,location,url'


class TwitterCollector():
  """
  Class that stores information of the twitter configuration file, manage keys and have methods to .
  
  """
  def __init__(self, configuration_file):     
   
    #API Handlers
    self.__api = list()
    self.__authenticate(configuration_file['access_keys'])
    
    #Word Handlers
    self.words = get_word_list(make_unique(configuration_file['keywords'])) \
      if len(configuration_file['keywords']) != 0 else None
    if self.words == None:
      raise Exception('No words registered in the configurations file.')
    
    
    #Time Handlers
    self.times = [date.datetime.now() - date.timedelta(minutes=15) if i > 0 
                  else date.datetime.now() for i in range(len(self.__api))]
    self.curr = 0

    self.only_pt = configuration_file['only_portuguese'] if 'only_portuguese' in configuration_file else False
    
  def __authenticate(self, key_set):
    """ Method responsible to authenticate the API keys and store in the class.

    Args:
        key_set (list of dictionaries): Contains the keys to communicate with the API.

    Raises:
        Exception: Invalid or missing keys for Twitter's API authentication.
    """
    for item in key_set:
      try:
        api_object = TwitterAPI(
          item['consumer_key'], 
          item['consumer_secret'],
          item['access_token'], 
          item['access_token_secret'],
          auth_type=OAuthType.OAUTH2,
          api_version='2')
        
        self.__api.append(api_object)
      
      except Exception:
        print(f"Invalid keys: \n{key_set}\n ")
      
    if len(self.__api) == 0:
      raise Exception("Invalid or missing keys for Twitter's API authentication in the configuration file.")
    
  def __next_api(self):
    """Change to the next key"""
    self.curr = (self.curr + 1) % (len(self.__api))
  
  
  def __rate_limit(self):
    API_TIME_RESET = 901 #Seconds
    API_TIME_SLEEP = 5 #Seconds

    while True:
      time_window = date.datetime.now() - self.times[self.curr]
      
      if time_window.seconds >= API_TIME_RESET:
        break
      
      else:
        time.sleep(API_TIME_SLEEP)
        self.__next_api()
        
    self.times[self.curr] = date.datetime.now()
    
    print("Changed Keys")  
  
  def __treat_exhausted_keys(self):
    del self.__api[self.curr]
    del self.times[self.curr]
            
    if len(self.__api) == 0:
        raise Exception('All keys are exhausted.')    
    
    self.__next_api()
    
  def __wipe_previous_rules(self):
    
    rule_ids = []
    r = self.__api[self.curr].request('tweets/search/stream/rules', method_override='GET')
    for item in r:
      if 'id' in item:
        rule_ids.append(item['id'])
    if len(rule_ids) > 0:
      r = self.__api[self.curr].request('tweets/search/stream/rules', {'delete': {'ids':rule_ids}})
  
  @retry((TwitterConnectionError), delay=30, tries=5)
  def getStreamCursor(self):
    """[summary]

    Raises:
        Exception: [description]

    Returns:
        [type]: [description]
    """
    while True:
      try:
        self.__wipe_previous_rules()
        filter_language = 'lang:pt' if self.only_pt else ""
        self.__api[self.curr].request('tweets/search/stream/rules', {'add': [{'value':f'({self.words}) {filter_language}'}]})
        response = TwitterPager(self.__api[self.curr], 'tweets/search/stream',{
            'tweet.fields': TWEET_FIELDS,
            'expansions': EXPANSIONS,
            'user.fields': USER_FIELDS,
            'place.fields': PLACE_FIELDS},
            hydrate_type=HydrateType.APPEND)
        
        cursor = response.get_iterator()
        
        first_tweet = cursor.__next__()

        return first_tweet, cursor

      except TwitterRequestError as e:        
        
        comparator = json.loads(e.msg)['title']
        # print("Deu ruim aqui ó")
        
        if comparator == "UsageCapExceeded":
          self.__treat_exhausted_keys()
        
        elif comparator == "Too Many Requests":
          self.__rate_limit()
        
        else:
          raise TwitterRequestError(e)

        continue      
      
      except Exception as e:
        
        raise Exception(f"{e}")

if __name__ == "__main__":
  pass