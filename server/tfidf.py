import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#getting the data
data_frame = pd.read_csv('papers.csv' , index_col = False)
data_frame = data_frame.loc[:, ~data_frame.columns.str.match('Unnamed')]


#Getting only the required data like id and title
new_data_frame= data_frame[['id','title']]


#Making into vectors
tfidfvectorizer = TfidfVectorizer()
tfidfmatrix = tfidfvectorizer.fit_transform(new_data_frame['title'])
#print(tfidfmatrix)
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
    print(uniq)
    return (uniq , recommended_id)

#Giving the input
recommendations('mars')