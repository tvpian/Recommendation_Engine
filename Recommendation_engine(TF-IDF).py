import numpy as np
import pandas as pd
import sklearn
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel


ds = pd.read_csv('sample-data.csv')

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['description'])
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

print(cosine_similarities)


idx=24#For the item with ID 24 all the top 10 similiar products are stated
for row in ds.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-10:-1]
            similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]
            items = [ ds['description'][i].split("-")[0] for i in similar_indices

items=list(dict.fromkeys(items)) # To extract the unique items alone from the list
items
