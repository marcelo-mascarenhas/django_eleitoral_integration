from textwrap import indent
from main.models import Tweet, User
import re
import json
class InformationHandler():
  """Class that store the methods to save information in the database"""
  
  def __saveTweets(self, tweet, referenced):
    """
    Save a tweet in the database.
    """
    method = tweet['utilized_method'] if 'utilized_method' in tweet else ""
    score = tweet['score'] if 'score' in tweet else ""
  
    new_tweet = None
    tweet['text'] = self.remove_users(tweet['text'])
    #Getting the user which was created in the previous function.
    user = User.objects.get(user_id=tweet['author_id'])
    #Assign each field to a specific value.
    new_tweet = Tweet(tweet_id=tweet['id'], author_id=user, text=tweet['text'], created_at=tweet['created_at'], \
                      evaluation_method=method, electoral_score=score, retweet_count=tweet['public_metrics']['retweet_count'], \
                        reply_count=tweet['public_metrics']['reply_count'], like_count=tweet['public_metrics']['like_count'], \
                          quote_count=tweet['public_metrics']['quote_count'], referenced=True if referenced else False)
        
    new_tweet.save()
        
  def __saveUser(self, author_id):
    # if not User.objects.filter(tweet['id']).exists():
    #   new_user = User(user_id=tweet['id'], user_screen_name=tweet['username'], \
    #     user_name=tweet['name'], user_verified=tweet['verified'], user_location=tweet['location'], \
    #       created_at=tweet['created_at'])
    if not User.objects.filter(user_id=author_id).exists():
      new_user = User(user_id=author_id)
      new_user.save()


  def saveInformation(self, information, referenced=False):
    self.__saveUser(information['author_id'])
    self.__saveTweets(information, referenced=referenced)
    
    
  def remove_users(self, text_msg):
    #Find all users and remove them.
    pattern = "@[a-zA-Z0-9_]+"
    
    text_msg = re.sub(pattern, "", text_msg)
    
    return text_msg