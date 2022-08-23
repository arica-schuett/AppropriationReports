#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 17:30:41 2022

@author: aricaschuett
"""

# import nltk
# nltk.download("all")
# import numpy
# import pandas
# import gensim
# import sklearn

# import pandas as pd

# Here we use 20-Newsgroups dataset (http://qwone.com/~jason/20Newsgroups/) for this example. 
# This version of the dataset contains about 11k newsgroups posts from 20 different topics. 
# This is available as https://raw.githubusercontent.com/selva86/datasets/master/newsgroups.json

with open('HouseAppropriationsReports_manualCleanTest.txt') as f:
    data = f.readlines()                 # Because I do readlines, the length is the number of lines. 
    data_text = data
    documents = data_text


# raw_data

# text = []
# for i in range(0, len(raw_data['content'])):
#   text.append(raw_data['content'][i])
  
# raw_data.head()

# Importing the needed packages
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords
import string
from nltk.stem import WordNetLemmatizer

import gensim
import gensim.corpora as corpora
#import pyLDAvis
#import pyLDAvis.gensim_models




# wrapped function
def extract_topic(data_text, stopwords):
  # tokenization
  tokenized_text = []
  for sentence in data_text:
    tokenized_text.append(word_tokenize(sentence))

  punctuations = string.punctuation  + "*" + "/" + "\\" + "_" + "-"

  lemmatizer = WordNetLemmatizer()

  filtered_text = []

  for sent in tokenized_text:
    filtered_list = []
    for word in sent:
      # filter out tokens that have punctuations and numbers
        # word.isalpha() returns true if a string only contains letters.
      # filter out stop words
      if word.isalpha() and lemmatizer.lemmatize(word.lower()) not in stop_words and len(word) >= 2:
        filtered_list.append(lemmatizer.lemmatize(word.lower()))
    filtered_text.append(filtered_list)


  # Create Dictionary
  id2word = corpora.Dictionary(filtered_text)
  # Create Corpus
  texts = filtered_text

  # Coverting Text to Bag of Words features
  corpus = [id2word.doc2bow(text) for text in texts]

# the num_topics is for the exercise. In the real world, we would test different 
  lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=12, 
                                           random_state= 0,
                                           passes = 10,
                                           alpha='auto')
  

  return lda_model



# filtering stop words (numbers) and punctuations, and lemmatzing
# After stopwords
stop_words = stopwords.words("english")
stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'line', 'organization', 'university', 'wa', 'ha', "'s", "n't", "'d"])

lda_model = extract_topic(data_text, stop_words)



from nltk.corpus import stopwords

# tokenization
tokenized_text = []
for sentence in data_text:
  tokenized_text.append(word_tokenize(sentence))
  
  lda_model.print_topics()
  

from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors

cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'


cloud = WordCloud(stopwords=stop_words,
                  background_color='white',
                  width=2500,
                  height=1800,
                  max_words=20,
                  colormap='tab10',
                  color_func=lambda *args, **kwargs: cols[i],
                  prefer_horizontal=1.0)

topics = lda_model.show_topics(formatted=False)


fig, axes = plt.subplots(3,4, figsize=(19,19), sharex=True, sharey=True)                ## Change Plot layout to match number of topics. 

for i, ax in enumerate(axes.flatten()):
    fig.add_subplot(ax)
    topic_words = dict(topics[i][1])
    cloud.generate_from_frequencies(topic_words, max_font_size=300)
    plt.gca().imshow(cloud)
    plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=16))
    plt.gca().axis('off')


plt.subplots_adjust(wspace=0, hspace=0)
plt.axis('off')
plt.margins(x=0, y=0)
plt.tight_layout()
plt.show()









