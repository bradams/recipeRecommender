import requests
import json 
import pandas as pd
import time
import pickle

#Details API call to get the actual information for each recipe. ingredients, etc.

#API url
url = "https://tasty.p.rapidapi.com/recipes/get-more-info"

#headers
headers = {
	"X-RapidAPI-Key": "",
	"X-RapidAPI-Host": "tasty.p.rapidapi.com"
}


#recipe list - has IDs for recipes
recipeData = pd.read_csv('recipeData.csv')


#Holds final data to be exported to CSV
recipeDataFinal = pd.DataFrame()

#loop through IDs - call API to get related details and store
for i in range(len(recipeData['id'])):

	#output ID being checked
	print(recipeData['id'][i].astype('int'))

	#Query parameter for the API call - grab ID here
	querystring = {"id":recipeData['id'][i].astype('int')}
	response = requests.request("GET", url, headers=headers, params=querystring)

	#ensure response has data, store if so
	response.raise_for_status()  # raises exception when not a 2xx response
	if response.status_code != 204:
   		data = response.json()

	#holds row-level data to be appended onto dataframe
	recipeDataDict = {}

	#relevant details
	recipeDataDict['id'] = data['id']
	recipeDataDict['recipeName'] = data['name']
	recipeDataDict['cook_time_minutes'] = data['cook_time_minutes']
	recipeDataDict['prep_time_minutes'] = data['prep_time_minutes']
	recipeDataDict['total_time_minutes'] = data['total_time_minutes']
	recipeDataDict['num_servings'] = data['num_servings']
	recipeDataDict['videoURL'] = data['original_video_url']

	#loop through recipe to get ingredients, tags, etc.
	for key, val in data.items():

		#INGREDIENTS
		if key == 'sections':

			#hold ingredient list for the relevant recipe
			ingredientList = []

			#loop through ingredients
			for i in range(len(val[0]['components'])):
				
				#append ingredients to the ingredientList 
				ingredientList.append(val[0]['components'][i]['ingredient']['name'])

			#add ingredient list as column
			recipeDataDict['ingredient_list'] = ingredientList

		#TAGS
		if key == 'tags':

			#holds final list of tags 
			tagList = []

			#loop through tags and append to list
			for i in range(len(val)):
				tagList.append(val[i]['name'])

			#append tag list as column to dataframe
			recipeDataDict['tag_list'] = tagList




		if key == 'instructions':

			instructionList = []

			for i in range(len(val)):

				#Get step # and instruction for that step
				instructionList.append(str(val[i]['position']) + " - " + val[i]['display_text'])


			recipeDataDict['instructions'] = instructionList



	#Add current dict of data onto dataframe
	recipeDataFinal = recipeDataFinal.append(recipeDataDict,ignore_index=True)

	#Wait .5 seconds - ensure program does not exceed rate limit
	time.sleep(.5)
	


#send dataframe to CSV file for storage
with open('recipeDataDetailed.pickle','wb') as f:
    pickle.dump(recipeDataFinal, f)

