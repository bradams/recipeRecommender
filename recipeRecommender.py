#https://towardsdatascience.com/building-a-recipe-recommendation-system-297c229dda7b

#This file will be used to actually create a recommender based off the recipe data

import pandas as pd
import numpy as np
from time import time

import ast

from scipy.spatial.distance import cosine, euclidean, hamming
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from gensim.models import Word2Vec




class tfidEmbeddingVectorizer(object):

    #Constructor
    def __init__(self,model):
        self.model=model
        self.wordIdfWeight = None
        #self.vectorSize = model.wv.vector_size

    #Function to fit the word2vec model - passes in all recipes/ingredient lists in the dataset
    def fit(self, documents):

        #list to hold text documents
        textDocs = []

        #loop through inputted documents, append recipe onto the textDocs list as a single long string
        #needed to create the embeddings - TfIDF works with single elements
        for doc in documents:
            textDocs.append(" ".join(doc))

        #tfidf vectorizer
        #opted for this as it will have more weight for the "rarer" ingredients - not garlic, salt, etc.
        tfidf = TfidfVectorizer()

        #fit vectorizer to textdocs
        tfidf.fit(textDocs)

        #get max idf weight
        max_idf = max(tfidf.idf_) 

        #Store the idf weights for all words in the corpus
        self.wordIdfWeight = defaultdict(
            lambda: max_idf,
            [(word, tfidf.idf_[i]) for word, i in tfidf.vocabulary_.items()],
        )

        #return class object
        return self


    #get average length of the documents (ingredient lists)
    def transform(self, documents):
        docWordVector = self.docAverageList(documents)
        return docWordVector


    def docAverage(self,document):

        #holds average of all documents
        mean = []

        #loop through words in a given document
        for word in document:
            if word in self.model.wv.index_to_key:
                mean.append(
                    self.model.wv.get_vector(word) * self.wordIdfWeight[word]
                    )
        #if not mean:  
        #    return np.zeros(self.vector_size)
        else:
            return np.array(mean).mean(axis=0)


    def docAverageList(self, docs):
        return np.vstack([self.docAverage(doc) for doc in docs])


#function to clean the ingredients list - remove stopwords, etc.
def cleanIngredients(row):

    #ingredient words to remove - essentially stopwords
    ingredientStopWords = ['teaspoon','tablespoon','cup','clove','gram','fluid ounce','fl oz','pint','quart','gallon','mg','g','kg','pound','lb','ounce','oz','milliliter',
                            'ml','liter','l','deciliter','dl']

    #will hold ingredient lists once they are cleaned up
    cleanedIngredientList = []

    #convert str to list
    try:
        row = ast.literal_eval(row)
    except ValueError:
        pass

    #loop through individual ingredients in ingredient list
    for ingredient in row:

        #will hold the cleaned ingredient 
        currIngredient = []

        #dont append word if in the stopwords list - otherwise add the lowercase
        for word in ingredient.split():
            if word in ingredientStopWords:
                pass
            if word not in ingredientStopWords:
                currIngredient.append(word.lower())

        cleanedIngredientList.append(' '.join(currIngredient))

    return cleanedIngredientList


#sorts a list in alphabetical order
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


#function to train and store word2vec model
def trainWord2Vec(toTrain, data):

    if toTrain == 0:
        pass
    if toTrain == 1:

        corpus = sortCorpus(recipeData, 'cleanedIngredientList')


        print(f"Length of corpus: {len(corpus)}")


        #Word2Vec model
        model_cbow = Word2Vec(
            corpus, sg=0, workers=8, window=lengthOfDocument(corpus), min_count=1, vector_size=100
        )
        model_cbow.save('model_cbow.bin')
        print("Training finished")


#function to create recommendations
def createRecommendations(userInput, recipeData):

    #load in word2vec model
    model = Word2Vec.load("model_cbow.bin")

    # use TF-IDF as weights for each word embedding
    tfidf_vec_tr = tfidEmbeddingVectorizer(model)

    #sort corpus before fitting
    corpus = sortCorpus(recipeData, 'cleanedIngredientList')

    tfidf_vec_tr.fit(corpus)
    doc_vec = tfidf_vec_tr.transform(corpus)
    doc_vec = [doc.reshape(1, -1) for doc in doc_vec]
    assert len(doc_vec) == len(corpus)


    userInput = userInput.split(",")

    print(userInput)

    #parse input
    userInput = cleanIngredients(userInput)


    input_embedding = tfidf_vec_tr.transform([userInput])[0].reshape(1, -1)

    cos_sim = map(lambda x: cosine_similarity(input_embedding, x)[0][0], doc_vec)
    scores = list(cos_sim)

    print(getRecommendations(3, scores, recipeData))



#Function to get top N recommendations and return 
def getRecommendations(N, scores, recipes):

    #Returns index of the highest N scores in the list
    topMatches = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]

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

#remove stopwords
for row in range(len(recipeData)):
    recipeData['cleanedIngredientList'][row] = cleanIngredients(recipeData['ingredient_list'][row])


#recommender system based on ingredients
trainWord2Vec(0, recipeData)


createRecommendations('holiday sprinkles, cream cheese, gingerbread',recipeData)


