from django import forms
from .utils import FileHandler
from .monitor.source.identificacao.identificacao import METODOS_POSSIVEIS



def calculatePossible(listinha):
  """
  Calculate all ML methods that can be used in the retrieval of twitter data. 
  """
  nds = []
  for item in listinha:
    nds.append((item, item.capitalize()))
  
  return nds

class ConfigurationForm(forms.Form):
  choices = calculatePossible(METODOS_POSSIVEIS)
  mtd = forms.CharField(label='Choose a detection method: ', \
    widget=forms.Select(choices=choices))
  
  twitter_configuration = forms.CharField()
  
class OrderBy(forms.Form):
  MY_CHOICES = (
    ('created_at', 'Creation Date'),
    ('like_count', 'Like Count'),
    ('retweet_count', 'Retweet Count'),
    ('reply_count', 'Answer Count'),
    ('electoral_score', 'Score'),
  )
  mtd = forms.CharField(label='Order by:', \
    widget=forms.Select(choices=MY_CHOICES))

  score_min = forms.FloatField()
  
  score_max = forms.FloatField()
