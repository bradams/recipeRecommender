import streamlit as st
from PIL import Image
import os

import pandas as pd
import pickle

#own modules
from recipeRecommenderPickle import createRecommendations



#TODO 
#1) make the "click here for instructions" a clickable button that expands
#2) make URL clickable




#Initialize session state object
st.session_state['userInput'] = ''
st.session_state['recipeDF'] = pd.read_pickle('C:/Users/bradl/OneDrive/Desktop/Git/recipeRecommender/recipeDataFinal.pickle')
st.session_state['getRecs'] = ""

#Formatting
image1 = Image.open('C:/Users/bradl/OneDrive/Desktop/Git/recipeRecommender/testPicture.jpg').resize((1005,450))
st.image(image1)
st.title("Recipe Recommender")


#Allow user to enter ingredients
st.session_state['userInput'] = st.text_input("Please enter the ingredients you wish to use/have on hand")


#or...see some random recipes by tag
#st.selectbox("Or...choose a type of food you'd like some recipes for!",['Greek','Mexican','Italian'])


recButton = st.button("Get recommendations")


#if button pushed
if recButton:
	st.write(st.session_state['userInput'])
	instructionButton = st.button("Click for instructions")

	recs = createRecommendations(5, st.session_state['userInput'], st.session_state['recipeDF'])

	st.table(recs[['recipe','cook time','url']])
	with st.sidebar:
		st.write("Instructions for relevant recipes: ")
		for instruction in recs['instructions']:
			st.markdown(instruction)

