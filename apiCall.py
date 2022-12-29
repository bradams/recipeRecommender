import requests
import json


#API call to get a list of recipes - namely using this to get a bunch of IDs and names which can join to details
#dumps into Data directory

def callAPI(toRun):
	if toRun == 0:
		pass
	else:
		url = "https://tasty.p.rapidapi.com/recipes/list"


		querystring = {"from":"0","size":"40","tags":"halloween"}

		headers = {
			"X-RapidAPI-Key": "99b6096298mshfeaa3f817596020p162e8cjsnd295cd31f3fe",
			"X-RapidAPI-Host": "tasty.p.rapidapi.com"
		}

		response = requests.request("GET", url, headers=headers, params=querystring)

		data = response.json()

		with open("/Users/bradadams/Desktop/Python/Recipe Recommender/Data/recipeJSONhalloween.json", 'w', encoding = 'utf-8') as f:
			json.dump(data, f, ensure_ascii = False, indent=4)
		f.close()


callAPI(1)





#Need to get a list of recipe IDs from /list and then get nutrition info, ingredients from /detail