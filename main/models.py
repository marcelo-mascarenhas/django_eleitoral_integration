from django.db import models


class User(models.Model):
  
  dui = models.AutoField(primary_key=True)
  
  user_id = models.BigIntegerField(unique=True, blank=False)
    
  user_screen_name = models.CharField(max_length=50, blank=True, null=True)
  
  user_name = models.CharField(max_length=150, blank=True, null=True)
  
  user_verified = models.BooleanField(blank=True, null=True)
  
  user_location = models.CharField(max_length=150, blank=True, null=True)
  
  created_at = models.DateTimeField(blank=True, null=True)
 

class Tweet(models.Model):
  
  tweet_id = models.BigIntegerField(primary_key=True)
  
  author_id = models.ForeignKey(User, on_delete=models.CASCADE)
  
  text = models.CharField(max_length=280)
    
  created_at = models.DateTimeField()
  
  electoral_score = models.FloatField(null=True)  
  
  evaluation_method = models.CharField(max_length=12, null=True) 
    
  retweet_count = models.SmallIntegerField()
  
  reply_count = models.SmallIntegerField()
  
  like_count = models.SmallIntegerField()
  
  quote_count = models.SmallIntegerField()
  
  tweet_type = models.CharField(max_length=12, null=True)

  
class MachineLearningMethod(models.Model):
  
  method = models.CharField(primary_key=True, max_length=15)
  
class ExecutionHandler(models.Model):
  
  process_id = models.PositiveIntegerField(primary_key=True)
  
  continue_run = models.BooleanField()
  