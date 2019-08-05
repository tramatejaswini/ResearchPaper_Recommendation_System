from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import euclidean_distances
from gensim.models import Word2Vec
from sklearn.neighbors import DistanceMetric
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import nltk
import pickle
import numpy as np
import csv

colnames = ['no','id', 'title', 'abstract', 'citation', 'references']
data = pd.read_csv('papers.csv',names=colnames)

new_df= data[['id','title']]

col_titlesentences = data.title.tolist ()

col_id=data.id.tolist()

# coverting list to string
str1 = ""
str1 = str1.join ( col_titlesentences )

# feature engineering-remove punctuation
tokenizer = RegexpTokenizer ( r'\w+' )
tokenizer.tokenize ( str1 )
sentences = nltk.sent_tokenize ( str1 )

# text processing
stemmer = PorterStemmer ()
for i in range ( len ( sentences ) ):
    wordsStemmer = nltk.word_tokenize ( sentences[i] )
    wordsStemmer = [stemmer.stem ( word ) for word in wordsStemmer]
    sentences[i] = ' '.join ( wordsStemmer )

# text processing two words are same then it will normalization
lemmatizer = WordNetLemmatizer ()
for i in range ( len ( sentences ) ):
    wordslemmatizer = nltk.word_tokenize ( sentences[i] )
    wordslemmatizer = [lemmatizer.lemmatize ( word ) for word in wordslemmatizer]
    sentences[i] = ' '.join ( wordslemmatizer )

sentences = sentences[0].split ( '.' )
del sentences[-1]
stopWords = stopwords.words ( 'english' )

vectorizer = CountVectorizer ( stop_words=stopWords )

featurevectors = vectorizer.fit_transform ( col_titlesentences ).todense ()

dicti = vectorizer.vocabulary_


def word2vec(test2):
   all_words = [nltk.word_tokenize(sent) for sent in col_titlesentences]
   word2vec = Word2Vec(all_words, min_count=2)
   vocabulary = word2vec.wv.vocab
   v1 = word2vec.wv['neural']
   sim_words = word2vec.wv.most_similar('neural')
   wordsnithya = list(word2vec.wv.vocab)
   sentences = [row.split(',') for row in col_titlesentences]
   model = Word2Vec(sentences, min_count=1,size= 50,workers=3, window =3, sg = 1)
   model['A novel Injection Locked Rotary Traveling Wave Oscillator']
   word2vecInput='A novel Injection Locked Rotary Traveling Wave Oscillator'
   word2vecOutput=model.most_similar(word2vecInput)[:5]
   return word2vecOutput

def build_model_knn(test2):
    neigh = NearestNeighbors ( n_neighbors=5 )
    global featurevectors
    neigh.fit ( featurevectors )
    NearestNeighbors ( algorithm='auto', leaf_size=30 )

    final_knn = neigh.kneighbors ( test2, return_distance=False )
    final_knn_list = final_knn.tolist()
   
def recommend_collaborative_filtering(list_of_papers):
    
    target_references = []
    count = 0
    with open('papers.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        for row in readCSV:
            if count > 0:
                if row[2] in list_of_papers:
                    ref = row[6].split(',')
                    for r in ref:
                        target_references.append(r)
                    break
            count+=1

    id_title_dict = {}

    count = 0
    candidate_papers = []
    with open('papers.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if count > 0:

                id_title_dict[row[2]] = row[3]

                refs = row[6].split(',')
                for r in refs:
                    if r in list_of_papers:
                        candidate_papers.append(row[2])
                    if r in target_references:
                        candidate_papers.append(row[2])
                        break
            count+=1

    for paper in candidate_papers:
        if paper in list_of_papers: 
            candidate_papers.remove(paper)

    
    candidate_papers_titles = []
    count = 0
    for id_ in candidate_papers:
        if count > 4:
            break
        count+=1
        candidate_papers_titles.append(id_title_dict.get(id_))

    return candidate_papers_titles


# cosine similarity
def cosine(test2):
    global featurevectors
    cosine_similarities = linear_kernel ( test2, featurevectors ).flatten ()
    related_docs_indices = cosine_similarities.argsort ()[:-5:-1]
    related_docs_indices_list = related_docs_indices.tolist()
    IDS = []
    my_dict={}
    for i in related_docs_indices:
        my_dict[col_id[i]] = col_titlesentences[i]
        IDS.append(col_id[i])
    result = []
    for i in related_docs_indices_list:
        result.append(col_titlesentences[i])
        
    return result,IDS
 
#getting the data
data_frame = pd.read_csv('papers.csv' , index_col = False)
data_frame = data_frame.loc[:, ~data_frame.columns.str.match('Unnamed')]


#Getting only the required data like id and title
new_data_frame= data_frame[['id','title']]


#Making into vectors
tfidfvectorizer = TfidfVectorizer()
tfidfmatrix = tfidfvectorizer.fit_transform(new_data_frame['title'])

data_frame = pd.DataFrame(tfidfmatrix.toarray())


# Caluculating similarity 
cosine_sim = cosine_similarity(data_frame)
df_cosineSim = pd.DataFrame(cosine_sim)

#Recommendations
def recommendations(title, cosine_sim = cosine_sim):
    recommended_titles = []
    recommended_id = []
    idx = new_data_frame[new_data_frame['title'].str.contains(title, case=False)].index[0]
    

    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    top_10_indexes = list(score_series.iloc[1:6].index)
    
    for i in top_10_indexes:
        recommended_titles.append(list(new_data_frame['title'])[i])
        recommended_id.append(list(new_data_frame['id'])[i])
        
        #recommended_titles[new_df['id'][i]] = new_df['title'][i]
        uniq = []
        [uniq.append(x) for x in recommended_titles if x not in uniq]
    
    return (uniq , recommended_id) 

def get_input(title_name):
    test2 = vectorizer.transform ( title_name ).toarray ()
    build_model_knn ( test2 )
    result_knn,ids =cosine ( test2 )
    result_word=word2vec(result_knn[0])	
    uniq , recommended_id=recommendations(title_name[0])
    result_collaborative=recommend_collaborative_filtering(ids)
    print(result_collaborative)
    return result_knn, uniq, result_word,result_collaborative
