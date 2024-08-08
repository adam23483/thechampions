import requests
import json

player_name = "Andre Brooks"

# transfermarkt API 
base_url = f"https://transfermarkt-api.vercel.app/players/search/{player_name}"
params = {'player_name': player_name }

player_search = "/players/search/{player_name}"
player_injuries = "/players/{player_id}/injuries"
player_profile = "/players/{player_id}/profile"
params = {'player_name': player_name }
response = requests.get(base_url,)
print(response.json())
