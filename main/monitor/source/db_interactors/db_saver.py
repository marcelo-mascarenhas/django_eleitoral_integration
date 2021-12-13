from main.models import Tweet, User

class InformationHandler():
  """Class that store the methods to save information in the database"""
  
  def __saveTweets(self, tweet, referenced):
    
    method = tweet['utilized_method'] if 'utilized_method' in tweet else ""
    score = tweet['score'] if 'score' in tweet else ""
  
    new_tweet = None
    
    new_tweet = Tweet(tweet_id=tweet['id'], author_id=tweet['author_id'] , text=tweet['text'], created_at=tweet['created_at'], \
                      evaluation_method=method, electoral_score=score, retweet_count=tweet['public_metrics']['retweet_count'], \
                        reply_count=tweet['public_metrics']['retweet_count'], like_count=tweet['public_metrics']['like_count'], \
                          quote_count=tweet['public_metrics']['quote_count'], referenced=True if referenced else False)
    
    print(new_tweet.referenced)
    
    new_tweet.save()
        
  def __saveUser(self, tweet):
    if not User.objects.filter(tweet['id']).exists():
      
      new_user = User(user_id=tweet['id'], user_screen_name=tweet['username'], \
        user_name=tweet['name'], user_verified=tweet['verified'], user_location=tweet['location'], \
          created_at=tweet['created_at'])
      
      new_user.save()
      

  def saveInformation(self, information, referenced=False):
    #__saveUser()
    self.__saveTweets(information, referenced=referenced)
    