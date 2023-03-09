## Phase 0 : Start Here

# ------- Calculate Time
# -------- Abaikan

import time

from datetime import datetime

start_time = time.time()
current_time = datetime.now()

time_str = current_time.strftime("%H:%M:%S")

print("Start Processing Time is:", time_str)

# -----------------------------------------------------
## NOTE: Tinggal diganti <all_reply_tweet_merged.csv> jadi nama file apa aja


import pandas as pd

with open('all_reply_tweet_merged.csv', 'r', encoding='utf-8') as file:
    data_twitter = pd.read_csv(file, sep=',', error_bad_lines=False)

data_twitter = data_twitter.rename(columns={'content':'tweet'})
data_twitter = data_twitter[['tweet']]
data_twitter['twit'] = data_twitter['tweet'].astype(pd.StringDtype())
data_twitter = data_twitter[['twit']][:20000]

## Phase 1
print('STARTING PHASE 1 .................')

import gensim
from gensim.models import CoherenceModel
from gensim.utils import simple_preprocess
from gensim.corpora.dictionary import Dictionary
import re
import string
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
nltk.download('stopwords')

# Clean the data
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove mentions and hashtags
    text = re.sub(r'@\w+|\#\w+', '', text)
    # Remove unwanted characters and symbols
    text = re.sub(r'^\d+$', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    teks = re.sub(r'<.*?>', ' ', text)
    teks = re.sub(r'\(\d+\W+\d+\)', '', text)
    teks = re.sub(r'[(),%]','',text)
    teks = re.sub(r'[0-9]', '',text)
    teks = re.sub(r'[//+\\]', '', text)
    teks = re.sub(r'\.', '', text)
    teks = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'(\s) | (-)', ' ', text)
    
    
    return text

data_twitter['clean_text'] = data_twitter['twit'].apply(clean_text)


## Phase 2 : Remove Stopwords and stemming
print('STARTING PHASE 2 .................')

stemmer = StemmerFactory().create_stemmer()
stopwords = nltk.corpus.stopwords.words('indonesian')

# apply stemming and remove stopwords, and join the words back into sentences
data_twitter['final'] = data_twitter['clean_text'].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split() if word not in stopwords]))


## Phase 3 : Coherence calculation for finding best num of topics
print('STARTING PHASE 3 .................')

from gensim.models.ldamodel import LdaModel

words_after_stem = data_twitter[['final']].replace(' ', '').replace('', pd.NA).dropna()

data_words = words_after_stem['final'].apply(lambda x: gensim.utils.simple_preprocess(x, deacc=True, min_len=3))
dictionary = Dictionary(data_words)
dictionary.filter_extremes(no_below=5, no_above=0.5)


# Convert the text data into a bag of words format
corpus = [dictionary.doc2bow(doc) for doc in data_words]

# Define the range of number of topics to test
min_topics = 2
max_topics = 30
step_size = 1
topics_range = range(min_topics, max_topics, step_size)

# Define the coherence values list
coherence_values = []
# Loop through each number of topics and calculate the coherence value
for num_topics in topics_range:
    lda_model = LdaModel(corpus=corpus,
                         id2word=dictionary,
                         num_topics=num_topics,
                         random_state=100,
                         chunksize=100,
                         passes=10,
                         alpha='auto',
                         per_word_topics=True)
    
    coherence_model_lda = CoherenceModel(model=lda_model,
                                         texts=data_words,
                                         dictionary=dictionary,
                                         coherence='c_v')
    
    coherence = coherence_model_lda.get_coherence()
    coherence_values.append(coherence)
    
best_num_topics = coherence_values.index(max(coherence_values)) + 2
best_num_topics



## Phase 4 : LDA Model
print('STARTING PHASE 4 .................')

import pyLDAvis.gensim_models
import pyLDAvis.sklearn

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=dictionary,
                                            num_topics=best_num_topics,
                                            random_state=100,
                                            update_every=1,
                                            passes=10,
                                            alpha='auto',
                                            per_word_topics=True)

for idx, topic in lda_model.print_topics(-1):
    print(f"Topic {idx}: {topic}")

# Visualize the topics using pyLDAvis
vis_data = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)

# Phase 5 : Labeling each tweet
print('STARTING PHASE 5 .................')

doc_topics = lda_model.get_document_topics(corpus)
df_doc_topics = pd.DataFrame(columns=['doc_id', 'topic_id', 'topic_prob'])
for i, doc_topics in enumerate(lda_model[corpus]):
    for topic in doc_topics:
        df_doc_topics = pd.concat([df_doc_topics, pd.DataFrame({'doc_id': [i], 'topic_id': [topic[0]], 'topic_prob': [topic[1]]})])

df_tag_topics = pd.merge(words_after_stem, df_doc_topics, left_index=True, right_on='doc_id')
df_grouped = df_tag_topics.groupby(['doc_id', 'topic_id'])['topic_prob'].mean().reset_index()
df_pivot = df_grouped.pivot(index='doc_id', columns='topic_id', values='topic_prob').reset_index()
df_tag_topics = pd.merge(df_tag_topics, df_pivot, on='doc_id')
df_tag_topics

# Get the topic ID with the highest score for each document
df_tag_topics['dominant_topic'] = df_tag_topics.iloc[:, 5:].idxmax(axis=1)


## Final Phase : Summarizing
print('STARTING FINAL PHASE .................')

final_tag = df_tag_topics[['final', 'dominant_topic']]
final_tag['count'] = 1
labeled_corpus =  final_tag.groupby(['final', 'dominant_topic']).sum()

labeled_corpus

# save the LDA model and dictionary as pickle files
import pickle

with open('twt20k_lda_model.pkl', 'wb') as f:
    pickle.dump(lda_model, f)
with open('twt20k_dictionary.pkl', 'wb') as f:
    pickle.dump(dictionary, f)

## --------------------------------------

print("-----------------------")
print("Time Spent in Running Query :")
print("-----------------------")

end_time = time.time()

total_time = end_time - start_time

minutes, seconds = divmod(total_time, 60)
hours, minutes = divmod(minutes, 60)

print("Elapsed time: {:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds)))

print('ALL PHASES DONE! .................')

pyLDAvis.display(vis_data)

# ---------------------------
