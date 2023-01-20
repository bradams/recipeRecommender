import pandas as pd
import json

from os import listdir
from os.path import isfile, join

#This file goes through the data returned from API call and sets into a dataframe for easier parsing by the detailsAPICall.py


def fileToParse():
	#DF for all final data
	recipeDataDF = pd.DataFrame()

	#Path to data directory
	mypath = 'C:/Users/bradl/OneDrive/Desktop/Git/recipeRecommender/JSON'

	#loop through data files
	for f in listdir(mypath):

		#ignore hidden files
		if not f.startswith('.'):

			filename = mypath + "/" + f

			print("Current file: ", f)

			#open data file
			currF = open(filename, encoding = 'utf-8')

			#load json file
			data=json.load(currF)


			#loop through data, store necessary stuffs
			for recipe in data['results']:

				#dict to hold current recipe data
				recipeDataDict = {}

				#loop through recipe data
				for recipeInfo,recipeData in recipe.items():

					if recipeInfo == 'id':
						recipeDataDict[recipeInfo] = int(recipeData)

				#add current id to the DF
				recipeDataDF = recipeDataDF.append(recipeDataDict, ignore_index=True)

	#dump ids to CSV file
	recipeDataDF.to_csv('recipeData.csv',index=False)



#Driver 
fileToParse()



