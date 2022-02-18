import io
import base64
import urllib
from wordcloud import WordCloud, STOPWORDS

import matplotlib.pyplot as plt


def generateWordCloud(text_corpus):

  #Generate the wordCloud
  wordcloud = WordCloud(width=1920, height=960, collocations = False,
                          stopwords=STOPWORDS).generate(text_corpus)
  #Adjust figure
  plt.figure(figsize=(20,10))
  plt.imshow(wordcloud,interpolation= 'bilinear')
  plt.axis("off")

  image = io.BytesIO()
  plt.savefig(image, format='png')
  image.seek(0)  # rewind the data
  string = base64.b64encode(image.read())

  final_img = 'data:image/png;base64,' + urllib.parse.quote(string)
  
  return final_img
