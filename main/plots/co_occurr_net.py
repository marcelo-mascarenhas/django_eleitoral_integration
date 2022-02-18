from tkinter import font
import networkx as nx
import itertools
import collections
import pandas as pd
import matplotlib.pyplot as plt
from pyvis.network import Network


def getDict(big):
  node_dict = {}
  for name_tuple, count in big:
    for item in name_tuple:
      if item not in node_dict:
        node_dict[item] = count
      else:
        node_dict[item] += count
    
  return node_dict



def generateCoOccurrence(bigrams, name):
  """
  Receives a list of bigrams and a path to save the file. (in html)
  """
  bigrams = list(itertools.chain(*bigrams))
  
  bigram_counts = collections.Counter(bigrams)
  big = bigram_counts.most_common(250)
  
  nodedic = getDict(big)
  

  N = Network(height='100%', width='100%', bgcolor='#222222', font_color='white')
  N.barnes_hut()
  
  for key, value in nodedic.items():
    N.add_node(key, size=value, fontSize=value)
    
  
  for name_tuple, count in big:
    id1, id2 = name_tuple
    N.add_edge(id1, id2, value=count)  
  
  N.show_buttons(filter_=['physics'])
  N.save_graph(name)
  return True
