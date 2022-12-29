#https://towardsdatascience.com/building-a-recipe-recommendation-system-297c229dda7b

#This file will be used to actually create a recommender based off the recipe data

import pandas as pd
import numpy as np
from time import time

import flask

import ast

from scipy.spatial.distance import cosine, euclidean, hamming
from sklearn.preprocessing import normalize
#from keras.preprocessing import image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from gensim.models import Word2Vec


'''
1) possible to only get recipes with nutrition facts?


'''

class tfidEmbeddingVectorizer(object):

    def __init__(self,model):
        self.model=model
        self.wordIdfWeight = None
        self.vectorSize = model.wv.vector_size

    def fit(self, documents):

        textDocs = []

        for doc in documents:
            textDocs.append(" ".join(doc))

        tfidf = TfidfVectorizer()

        tfidf.fit(textDocs)

        max_idf = max(tfidf.idf_) 
        self.wordIdfWeight = defaultdict(
            lambda: max_idf,
            [(word, tfidf.idf_[i]) for word, i in tfidf.vocabulary_.items()],
        )

        return self

    def transform(self, documents):
        docWordVector = self.docAverageList(documents)
        return docWordVector

    def docAverage(self,document):

        mean = []

        for word in document:
            if word in self.model.wv.index_to_key:
                mean.append(
                    self.model.wv.get_vector(word) * self.wordIdfWeight[word]
                    )
        if not mean:  
            return np.zeros(self.vector_size)
        else:
            mean = np.array(mean).mean(axis=0)
            return mean

    def docAverageList(self, docs):
        return np.vstack([self.docAverage(doc) for doc in docs])






def cleanIngredients(row):


    ingredientStopWords = ['teaspoon','tablespoon','cup','clove','gram','fluid ounce','fl oz','pint','quart','gallon','mg','g','kg','pound','lb','ounce','oz','milliliter',
                            'ml','liter','l','deciliter','dl']



    cleanedIngredientList = []

    #convert str to list
    row = ast.literal_eval(row)
    for ingredient in row:

        currIngredient = []

        for word in ingredient.split():
            if word in ingredientStopWords:
                pass
            if word not in ingredientStopWords:
                currIngredient.append(word.lower())

        cleanedIngredientList.append(' '.join(currIngredient))

    return cleanedIngredientList




def cleanIngredients1(row):


    ingredientStopWords = ['teaspoon','tablespoon','cup','clove','gram','fluid ounce','fl oz','pint','quart','gallon','mg','g','kg','pound','lb','ounce','oz','milliliter',
                            'ml','liter','l','deciliter','dl']



    cleanedIngredientList = []

    #convert str to list
    for ingredient in row:

        currIngredient = []

        for word in ingredient.split():
            if word in ingredientStopWords:
                pass
            if word not in ingredientStopWords:
                currIngredient.append(word.lower())

        cleanedIngredientList.append(' '.join(currIngredient))

    return cleanedIngredientList



#sorts a given list in alphabetical order
def sortCorpus(row,col):

    sortedCorpus = []

    for document in row[col].values:
        document.sort()
        sortedCorpus.append(document)
    return sortedCorpus


#gets average legnth of document - used in sliding window for Word2Vec
def lengthOfDocument(corpus):
    lengths = [len(doc) for doc in corpus]
    avgLen = float(sum(lengths) / len(lengths))
    return round(avgLen)





def ingredientRecommender(data):


    #remove stopwords
    for row in range(len(data)):
        data['cleanedIngredientList'][row] = cleanIngredients(data['ingredient_list'][row])



    #data['ingredient_list'] = 



def getRecommendations(N, scores, recipes):

    #Returns index of the highest N scores in the list
    topMatches = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]

    print(recipes.columns)

    recommendation = pd.DataFrame(columns=["recipe", "ingredients", "score"])
    count = 0
    for i in topMatches:
        recommendation.at[count, "recipe"] = recipes["recipeName"][i]
        recommendation.at[count, "ingredients"] = cleanIngredients(recipes["ingredient_list"][i])
        recommendation.at[count, "score"] = round(scores[i],3)

        count += 1
    return recommendation



#Driver###############

print('\n\n\n\n\n')

#Read data
recipeData = pd.read_csv('recipeDataDetailed1.csv')

#initialize empty column
recipeData['cleanedIngredientList'] = None

#recommender system based on ingredients
ingredientRecommender(recipeData)

#sort ingredients list
corpus = sortCorpus(recipeData, 'cleanedIngredientList')

print(f"Length of corpus: {len(corpus)}")

#Word2Vec model
model_cbow = Word2Vec(
    corpus, sg=0, workers=8, window=lengthOfDocument(corpus), min_count=1, vector_size=100
)

print("Word2Vec model successfully trained")



# use TF-IDF as weights for each word embedding
tfidf_vec_tr = tfidEmbeddingVectorizer(model_cbow)
tfidf_vec_tr.fit(corpus)
doc_vec = tfidf_vec_tr.transform(corpus)
doc_vec = [doc.reshape(1, -1) for doc in doc_vec]
assert len(doc_vec) == len(corpus)


#recipe to be checked
inpt = "sour cream, sugar, holiday sprinkles"

inpt = inpt.split(",")

print(inpt)

#parse input
inpt = cleanIngredients1(inpt)


input_embedding = tfidf_vec_tr.transform([inpt])[0].reshape(1, -1)


cos_sim = map(lambda x: cosine_similarity(input_embedding, x)[0][0], doc_vec)
scores = list(cos_sim)

print(scores)

getRecommendations(3, scores, recipeData)

