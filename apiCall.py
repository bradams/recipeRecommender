import requests
import json


#API call to get a list of recipes as a JSON object - namely using this to get a bunch of IDs and names which can join to details
#dumps into Data directory

def callAPI(tagName):

	#Base URL for the API
	url = "https://tasty.p.rapidapi.com/recipes/list"

	#query for the api - change parameters as needed
	querystring = {"from":"0","size":"40","tags": tagName}

	#headers for API call
	headers = {
		"X-RapidAPI-Key": "",
		"X-RapidAPI-Host": "tasty.p.rapidapi.com"
	}

	#get response, convert to JSON
	response = requests.request("GET", url, headers=headers, params=querystring)
	data = response.json()

	#open and store intermedite JSON file
	with open("C:/Users/bradl/OneDrive/Desktop/Git/recipeRecommender/JSON/" + tagName +".json", 'w', encoding = 'utf-8') as f:
		json.dump(data, f, ensure_ascii = False, indent=4)
	f.close()

##Driver
callAPI("easter")





#Need to get a list of recipe IDs from /list and then get nutrition info, ingredients from /detail