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
  mtd = forms.CharField(label='Escolha um método de detecção: ', \
    widget=forms.Select(choices=choices))
  
  twitter_configuration = forms.CharField()
  
class OrderBy(forms.Form):
  MY_CHOICES = (
    ('created_at', 'Data de Criação'),
    ('like_count', 'Quantidade de Curtidas'),
    ('retweet_count', 'Quantidade de Retweets'),
    ('reply_count', 'Quantidade de Respostas'),
    ('electoral_score', 'Score'),
  )
  mtd = forms.CharField(label='Ordenar por:', \
    widget=forms.Select(choices=MY_CHOICES))

  score_min = forms.FloatField()
  
  score_max = forms.FloatField()
