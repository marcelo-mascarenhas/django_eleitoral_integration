from django.db import models


class User(models.Model):
  
  user_id = models.BigIntegerField(primary_key=True)
  
  user_screen_name = models.CharField(max_length=50)
  
  user_name = models.CharField(max_length=150)
  
  user_verified = models.BooleanField()
  
  user_location = models.CharField(max_length=150)
  
  created_at = models.DateTimeField()
 
class Tweet(models.Model):
  
  tweet_id = models.BigIntegerField(primary_key=True)
  
  author_id = models.BigIntegerField()
  
  text = models.CharField(max_length=280)
  
  lang = models.CharField(max_length=6, null=True)
  
  created_at = models.DateTimeField()
  
  electoral_score = models.FloatField(null=True)  
  
  evaluation_method = models.CharField(max_length=12, null=True) 
  
  
class MachineLearningMethods(models.Model):
  
  method = models.CharField(primary_key=True, max_length=15)
  
class ExecutionHandler(models.Model):
  
  process_id = models.PositiveIntegerField(primary_key=True)
  
  continue_run = models.BooleanField()