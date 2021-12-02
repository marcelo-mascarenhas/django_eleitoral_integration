from django import forms
from .monitor.source.identificacao.identificacao import METODOS_POSSIVEIS

def calculatePossible(listinha):
  nds = []
  for item in listinha:
    nds.append((item, item.capitalize()))
  
  return nds

class ConfigurationForm(forms.Form):
  choices = calculatePossible(METODOS_POSSIVEIS)

  mtd = forms.CharField(label='Escolha um método de detecção: ', \
    widget=forms.Select(choices=choices))
  