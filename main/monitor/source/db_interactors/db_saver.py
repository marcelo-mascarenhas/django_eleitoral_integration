from main.models import Tweet, User

class InformationHandler():
  """Class that save information on the database and is 
  responsible to kill the process if a signal is sent from the Interface  
  """
  
  def __saveTweets(self, tweet):
    method = tweet['utilized_method'] if 'utilized_method' in tweet else ""
    score = tweet['score'] if 'score' in tweet else ""
    new_tweet = None

    if (method and score) != "":
      new_tweet = Tweet(tweet_id=tweet['id'], author_id=tweet['author_id'] , text=tweet['text'], created_at=tweet['created_at'], \
                        evaluation_method=method, electoral_score=score)
    else:
      new_tweet = Tweet(tweet_id=tweet['id'], author_id=tweet['author_id'] ,text=tweet['text'], \
        lang=tweet['lang'], created_at=tweet['created_at'])
      
    new_tweet.save()
        
  def __saveUser(self, tweet):
    if not User.objects.filter(tweet['id']).exists():
      new_user = User(user_id=tweet['id'], user_screen_name=tweet['username'], user_name=tweet['name'], user_verified=tweet['verified'], user_location=tweet['location'], created_at=tweet['created_at'])
      new_user.save()
      

  def saveInformation(self, information):
    #__saveUser()
    self.__saveTweets(information)