from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import set_config; set_config("diagram")
import pandas as pd
import os
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import string
from nltk import word_tokenize



# Récupération de la donnée:
def get_data(path_csv):
    data = pd.read_csv(path_csv, sep=",")
    return data

# Data cleaning
def data_cleaning(data):
    duplicate_count = data.duplicated().sum() #duplicate count
    data = data.drop_duplicates() #Drop duplicate
    data = data.drop(columns='Unnamed: 0') #remove unuseful column
    return data

#Preprocess data
def preprocessing(sentence):
    # remove espaces
    sentence = sentence.strip()
    # met en lowercase
    sentence = sentence.lower()
    # remove numbers
    sentence = ''.join(char for char in sentence if not char.isdigit())
    # remove ponctuation
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, ' ')
    # tokenize
    sentence_tokenize = word_tokenize(sentence)
    # enleve les stop words:
    stop_words = set(stopwords.words('french'))
    tokens_cleaned = [w for w in sentence_tokenize if not w in stop_words]
    # lemmatize
    verb_lemmatized = [WordNetLemmatizer().lemmatize(word, pos = "v") for word in tokens_cleaned]
    noun_lemmatized = [WordNetLemmatizer().lemmatize(word, pos = "n") for word in verb_lemmatized]
    sentence_lemma = ' '.join(noun_lemmatized)

    data = data_cleaning(data)
    data['clean_message'] = data['message']
    data['clean_message'] = data['clean_message'].apply(preprocessing)

    return data

# Word topic:
def print_topics(model, vectorizer):
    for idx, topic in enumerate(model.components_):
        print("Topic %d:" % (idx))
        print([(vectorizer.get_feature_names_out()[i], topic[i])
                        for i in topic.argsort()[:-10 - 1:-1]])


# Word most relevant with weight:
def print_topics1(model, vectorizer, top_words):
    # 1. TOPIC MIXTURE OF WORDS FOR EACH TOPIC
    topic_mixture = pd.DataFrame(model.components_,
                                 columns = vectorizer.get_feature_names_out())

    # 2. FINDING THE TOP WORDS FOR EACH TOPIC
    ## Number of topics
    n_components = topic_mixture.shape[0]
    ## Top words for each topic
    for topic in range(n_components):
        print("-"*10)
        print(f"For topic {topic}, here are the the top {top_words} words with weights:")
        topic_df = topic_mixture.iloc[topic]\
                             .sort_values(ascending = False).head(top_words)

        print(round(topic_df,3))



# train/fit LDA with tfid vectorizer
def model_lda_tfid(data):
    vectorizer_tfid = TfidfVectorizer(max_df=20)
    vectorized_data_tfid = vectorizer_tfid.fit_transform(data['clean_message'])
    vectorized_data_tfid = pd.DataFrame(vectorized_data_tfid.toarray(),
                                        columns = vectorizer_tfid.get_feature_names_out())

    # Instantiate the LDA
    lda_model = LatentDirichletAllocation(n_components=10, max_iter = 50)

    # Fit the LDA on the vectorized documents
    model = lda_model.fit(vectorized_data_tfid)

    return print_topics(model,vectorizer_tfid), print_topics1(model, vectorizer_tfid, 10)


# train/fit LDA with n-gram vectorizer (bi-gram, tri-gram)
def model_lda_tfid(data):
    vectorizer_ngram = CountVectorizer(ngram_range = (2,3))
    vectorized_data_ngram = vectorizer_ngram.fit_transform(data_ngram)

    vectorized_data_ngram = pd.DataFrame(
        vectorized_data_ngram.toarray(),
        columns = vectorizer_ngram.get_feature_names_out())

    # Instantiate the LDA
    lda_model = LatentDirichletAllocation(n_components=10, max_iter = 50)

    # Fit the LDA on the vectorized documents
    model = lda_model.fit(vectorized_data_ngram)

    return print_topics(model,vectorizer_ngram), print_topics1(model, vectorizer_ngram, 10)
