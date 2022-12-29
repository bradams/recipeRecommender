import pandas as pd
import json

from os import listdir
from os.path import isfile, join

#This file goes through the data returned from API call and sets into a dataframe for easier parsing by the detailsAPICall.py


def fileToParse():
	#DF for all final data
	recipeDataDF = pd.DataFrame()

	#Path to data directory
	mypath = '/Users/bradadams/Desktop/Python/Recipe Recommender/Data'

	#loop through data files
	for f in listdir(mypath):

		#ignore hidden files
		if not f.startswith('.'):
			filename = mypath + "/" + f

			print(filename)

			#open data file
			currF = open(filename)

			#load json file
			data=json.load(currF)


			#loop through data, store necessary stuffs
			for recipe in data['results']:

				#dict to hold current recipe data
				recipeDataDict = {}

				#loop through recipe data
				for recipeInfo,recipeData in recipe.items():
					#print(recipeInfo)
					#if recipeInfo == 'name':
					#	recipeDataDict[recipeInfo] = recipeData
					#if recipeInfo == 'cook_time_minutes':
					#	recipeDataDict[recipeInfo] = recipeData		
					#if recipeInfo == 'prep_time_minutes':
					#	recipeDataDict[recipeInfo] = recipeData	

					#if recipeInfo == 'instructions':
					#	recipeDataDict[recipeInfo] = recipeData

						#Get id from instructions....need this to get ingredients
						#for instructionInfo, instructionData in recipeData[0].items():
						#	if instructionInfo == 'id':
						#		recipeDataDict['ID'] = instructionData

					if recipeInfo == 'id':
						recipeDataDict[recipeInfo] = int(recipeData)

					#if recipeInfo == 'nutrition':
					#	recipeDataDict[recipeInfo] = recipeData

				recipeDataDF = recipeDataDF.append(recipeDataDict, ignore_index=True)



	recipeDataDF.to_csv('recipeData.csv',index=False)



#Driver 
fileToParse()



