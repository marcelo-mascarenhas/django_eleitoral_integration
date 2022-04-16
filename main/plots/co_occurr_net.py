from tkinter import font
import networkx as nx
import itertools
import collections
import pandas as pd
import matplotlib.pyplot as plt
from pyvis.network import Network

MIN = 5
MAX = 150


def checkNumber(a):
  if a.isdigit():
    return True
  elif a.replace('.','',1).isdigit() and a.count('.') < 2:
    return True
  elif a.replace(',','',1).isdigit() and a.count(',') < 2:
    return True
  else:
    return False

def normalize_min_max(a, b, ndict):
  """
  [a,b] represents the interval to normalize, and the dictionary contains the values.
  
  """
  min_dict_value = min(ndict.values())
  max_dict_value = max(ndict.values())
  
  for key,value in ndict.items():
    #If the two values are equal, then it will give a ZeroDivisionError. So, the value of all items are 'a'.
    if max_dict_value != min_dict_value:
      ndict[key] = a + ((value - min_dict_value)*(b-a))/(max_dict_value - min_dict_value)
    else:
      ndict[key] = a
      
      
      
def getDict(big, a=0, b=1, normalize=True):
  """
  Calculate the TF of the bigram's terms in the text corpus. If normalize == True, then it will use a and b to 
  normalize the scores in the interval [a,b]
  """
  
  node_dict = {}
  for name_tuple, count in big:
    for item in name_tuple:
      if item not in node_dict:
        node_dict[item] = count
      else:
        node_dict[item] += count
  
  if normalize == True:
    normalize_min_max(a, b, node_dict)
  return node_dict



def generateCoOccurrence(bigrams, name):
  """
  Receives a list of bigrams and a path to save the file. (in html)
  """
  bigrams = list(itertools.chain(*bigrams))
  
  bigram_counts = collections.Counter(bigrams)
  big = bigram_counts.most_common(300)
  
  nodedic = getDict(big, MIN, MAX)
  

  N = Network(height='100%', width='100%', bgcolor='#222222', font_color='white')
  N.barnes_hut()
  
  for key, value in nodedic.items():
    if checkNumber(key):
      continue
    N.add_node(key, size=value, fontSize=value)
  
    
  for name_tuple, count in big:
    id1, id2 = name_tuple
    if id1 == id2 or checkNumber(id2) or checkNumber(id1):
      continue
    N.add_edge(id1, id2, value=count)  
  
  # N.show_buttons()

  # N.set_options('var options = {  "nodes": {    "color": {      "hover": {        "border": "rgba(231,44,233,1)"      }    },    "shape": "dot"  },  "edges": {    "arrowStrikethrough": false,    "color": {      "highlight": "rgba(132,48,51,1)",      "hover": "rgba(128,25,132,1)",      "inherit": false    }},   "physics": {"repulsion": {      "nodeDistance": 400    },"minVelocity": 0.75,    "solver": "repulsion"}}')
  # N.set_options('var options = {"nodes": {    "color": {      "hover": {        "border": "rgba(231,44,233,1)"      }    },    "shape": "dot"  },  "edges": {    "arrowStrikethrough": false,    "color": {      "highlight": "rgba(132,48,51,1)",      "hover": "rgba(128,25,132,1)",      "inherit": false    }}, "physics": {"repulsion": {      "nodeDistance": 400    },"minVelocity": 0.75,    "solver": "repulsion"}}')
  N.set_options("""var options = {
  "nodes": {
    "color": {
      "highlight": {
        "border": "rgba(43,78,233,1)",
        "background": "rgba(47,161,255,1)"
      }
    }
  },
  "edges": {
    "color": {
      "color": "rgba(70,57,132,1)",
      "highlight": "rgba(132,26,50,1)",
      "inherit": false
    },
    "font": {
      "strokeWidth": 6
    },
    "smooth": false
  },
"physics": {
  "repulsion": {      
  "nodeDistance": 550    
  },
  "minVelocity": 0.75,    
  "solver": "repulsion"}
}""")
  N.save_graph(name)
  return True
