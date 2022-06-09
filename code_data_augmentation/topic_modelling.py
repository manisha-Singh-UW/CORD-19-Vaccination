#--------------------------------
# CORD-19 - Vaccinnation
# Topic modelling
#--------------------------------

#Load libraries
import pandas as pd
import csv
import os
import json
from collections import defaultdict, Counter
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from nltk.corpus import stopwords
import numpy as np
import re
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer
from tmtoolkit.topicmod import tm_sklearn, evaluate
from sklearn.manifold import TSNE
from bokeh.plotting import figure, output_file, show
from bokeh.models import Label
from bokeh.io import output_notebook
import matplotlib.pyplot as plt

#Load df
cord_df = pd.read_csv('cord19_vaccine_lang+aff+kw+ssct.csv')

#--------------------------------
#Exploratory Data Analysis
#--------------------------------

#Check number of rows with no linked pdf file
np.sum(pd.isnull(cord_df.pdf_json_files))

#Check language distribution
cord_df.lang_id.value_counts()

#Check possible duplicates
cord_df.title.value_counts(ascending = False).head(20)

#Check number of papers that have no country affiliation
pd.isnull(cord_df.aff_country).value_counts()

pd.isnull(cord_df.aff_country).value_counts(normalize = True)

#--------------------------------
#Data pre-processing
#--------------------------------

#Transform to lower
docs = cord_df[~pd.isnull(cord_df.abstract)].abstract.str.lower()

#Build analyser for the tokenisation in CountVectoriser
analyser = CountVectorizer().build_analyzer()

#Function to get tokenised docs for the Coherence evaluation
def preproc_words(docs):
    wnl = WordNetLemmatizer()
    regex_punctuation = '[^\w\s]'
    regex_small_words = r'(\b\w{1,2}\b)'
    stop_words = set(stopwords.words('english'))
    return [[wnl.lemmatize(t) for t in word_tokenize(doc) 
                if (not re.search(regex_punctuation, t)) and (not re.search(regex_small_words, t))
               and (t not in stop_words)] for doc in docs]

#Tokeniser for CountVectorizer
def preprocess_words(doc):
    wnl = WordNetLemmatizer()
    #Remove punctuation
    regex_punctuation = '[^\w\s]'
    #Remove words of length < 3
    regex_small_words = r'(\b\w{1,2}\b)'
    #Remove stopwords
    stop_words = set(stopwords.words('english'))
    return [wnl.lemmatize(t) for t in word_tokenize(doc) 
                if (not re.search(regex_punctuation, t)) and (not re.search(regex_small_words, t))
               and (t not in stop_words)]

#Get tokenised list of docs
preproc_docs = preproc_words(docs)

#Crea term-frequency matrix using CountVectorizer
tf_vectorizer = CountVectorizer(analyzer = preprocess_words,
                                strip_accents = 'unicode', 
                                max_df = 0.5, 
                                min_df = 10,
                               max_features = 3000)

tf_matrix = tf_vectorizer.fit_transform(docs)

#--------------------------------
#Model training
#--------------------------------

#Train LDA models with different number of topics and calculate the mean coherence value for each of them
results = []
n_components = list(range(5,15,1))

for n in n_components:
    lda = LatentDirichletAllocation(
                                    n_components=n,
                                    max_iter=5,
                                    learning_method="online",
                                    learning_offset=50.0,
                                    random_state=0)
    lda_vec = lda.fit_transform(tf_matrix)
    
    coherence = evaluate.metric_coherence_gensim(measure = 'c_v', topic_word_distrib = lda.components_,
                                    vocab = np.array(list(tf_vectorizer.vocabulary_.keys())),
                                    texts = preproc_docs,
                                     return_mean = True)
    
    results.append([n, coherence])

#--------------------------------
#Evaluation
#--------------------------------

#Plot coherence metric by number of topics
n_topics_df = pd.DataFrame(results, columns = ['n_components', 'coherence'])

fig, ax = plt.subplots(figsize=(8, 5))
ax = n_topics_df.coherence.plot()
ax.set_xticks(n_topics_df.index)
ax.set_xticklabels(n_topics_df.n_components.apply(str))
ax.set_xlabel('Number of topics')
ax.set_title('Coherence by number of topics')

#Train final LDA based on best number of topics
lda = LatentDirichletAllocation(
                                    n_components=5,
                                    max_iter=10,
                                    learning_method="online",
                                    learning_offset=50.0,
                                    random_state=0)
lda_vec = lda.fit_transform(tf_matrix)

evaluate.metric_coherence_gensim(measure = 'c_v', topic_word_distrib = lda.components_,
                                    vocab = np.array(list(tf_vectorizer.vocabulary_.keys())),
                                    texts = preproc_docs,
                                     return_mean = True)

#--------------------------------
#Topic analysis
#--------------------------------

#Get top 20 words for each topic
topic_words = {}
for n in range(len(lda.components_)):
    words = [tf_vectorizer.get_feature_names()[i] for i in lda.components_[n].argsort()[: -20 - 1 : -1]]
    topic_words['topic_' + str(n+1)] = words

topics = ['Vaccine development',
          'Vaccination side-effects / Treatments',
          'Vaccination efficacy (including vaccination in patients with other diseases)',
          'Methodologies for COVID studies (e.g. statistical modelling, simulations)',
          'Vaccine uptake and effects (by factors like age, race, etc.)']

#Get topic distribution
for i, row in pd.Series(lda_vec.argmax(axis = 1)).value_counts(normalize = True).reset_index().iterrows():
    print(topics[int(row['index'])], row[0])

#Reduce dimensionality for plotting
tsne_lda_model = TSNE(n_components=2, perplexity=50, learning_rate=100, 
                        n_iter=2000, verbose=1, random_state=0, angle=0.75)
tsne_lda_vectors = tsne_lda_model.fit_transform(lda_vec)

def get_keys(topic_matrix):
    keys = topic_matrix.argmax(axis=1).tolist()
    return keys

lda_labels = get_keys(lda_vec)

def get_mean_topic_vectors(keys, two_dim_vectors):
    n_topics = len(set(keys))
    mean_topic_vectors = []
    for t in range(n_topics):
        papers_topic = []
        for i in range(len(keys)):
            if keys[i] == t:
                papers_topic.append(two_dim_vectors[i])    
        
        papers_topic = np.vstack(papers_topic)
        mean_paper_topic = np.mean(papers_topic, axis=0)
        mean_topic_vectors.append(mean_paper_topic)
    return mean_topic_vectors

n_topics = len(set(lda_labels))
colormap = np.array([
    "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
    "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
    "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
    "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5" ])

color_key = {i: colormap[i] for i in range(n_topics)}

#Get the mean of the topic vector for the visualization
lda_mean_topic_vectors = get_mean_topic_vectors(lda_labels, tsne_lda_vectors)

fig, ax = plt.subplots(figsize=(14, 10))
ax.scatter(x=tsne_lda_vectors[:,0], y=tsne_lda_vectors[:,1], c = colors)

for t in range(n_topics):
    ax.text(lda_mean_topic_vectors[t][0], lda_mean_topic_vectors[t][1],
           topics[t], bbox=dict(facecolor=colormap[t], alpha=0.5))

