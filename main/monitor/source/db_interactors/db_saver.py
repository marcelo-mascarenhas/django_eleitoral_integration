from textwrap import indent
from main.models import Tweet, User
import re
import json
class InformationHandler():
  """Class that store the methods to save information in the database"""
  
  def __saveTweets(self, tweet):
    """
    Save a tweet in the database.
    """
    method = tweet['utilized_method'] if 'utilized_method' in tweet else ""
    score = tweet['score'] if 'score' in tweet else ""
  
  
    tweet_type = tweet['referenced_tweets'][0]['type'] if 'referenced_tweets' in tweet else "Post"
  
    new_tweet = None
    tweet['text'] = self.remove_users(tweet['text'])
    #Getting the user which was created in the previous function.
    user = User.objects.get(user_id=tweet['author_id'])
    #Assign each field to a specific value.
    new_tweet = Tweet(tweet_id=tweet['id'], author_id=user, text=tweet['text'], created_at=tweet['created_at'], \
                      evaluation_method=method, electoral_score=score, retweet_count=tweet['public_metrics']['retweet_count'], \
                        reply_count=tweet['public_metrics']['reply_count'], like_count=tweet['public_metrics']['like_count'], \
                          quote_count=tweet['public_metrics']['quote_count'], tweet_type=tweet_type)
        
    new_tweet.save()
        
  def __saveUser(self, user_info, complete=True):
    #If we have all information about the user, fill all the fields.
    print(json.dumps(user_info, indent=5))
    if complete:
      
      location = user_info['location'] if 'location' in user_info else ""
      if not User.objects.filter(user_id=user_info['id']).exists():
        new_user = User(user_id=user_info['id'], user_screen_name=user_info['username'], \
          user_name=user_info['name'], user_verified=user_info['verified'], user_location=location, \
            created_at=user_info['created_at'])      
        new_user.save()

    else: 
      if not User.objects.filter(user_id=user_info['id']).exists():
        new_user = User(user_id=user_info['id'])
        new_user.save()


  def saveInformation(self, tweet_information, author_information, complete=True):
    self.__saveUser(author_information, complete)
    self.__saveTweets(tweet_information)
    
    
  def remove_users(self, text_msg):
    #Find all users and remove them.
    pattern = "@[a-zA-Z0-9_]+"
    
    text_msg = re.sub(pattern, "", text_msg)
    
    return text_msg