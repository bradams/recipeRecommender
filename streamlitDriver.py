import streamlit as st
from PIL import Image
import os

#Header image
image1 = Image.open('C:/Users/bradl/OneDrive/Desktop/Git/recipeRecommender/testPicture.jpg').resize((1005,450))
st.image(image1)

#Page title
st.title("Recipe Recommender")


#Allow user to enter ingredients
st.text_input("Please enter the ingredients you wish to use/have on hand")


#button
st.button("Recommend me something!")


#or...see some random recipes by tag
st.selectbox("Or...choose a type of food you'd like some recipes for!",['Greek','Mexican','Italian'])

