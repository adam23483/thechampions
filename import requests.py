import requests
from bs4 import BeautifulSoup
import array as arr

url = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
response = requests.get(url)

if response.ok:
  html_content = response.text.replace('<!--', '').replace('-->', '') #.replace() removes player data comment out  
  soup = BeautifulSoup(html_content, 'html.parser')
  print("Retrieved HTML content.   "
        )
else:
  print("Failed to retrieve the HTML content.")


#list for tags for player data
data_stats_ids  = [
"player",
"nationality",
"position",
"team",
"age",
"birth_year",
"games",
"games_starts",
"minutes",
"minutes_90s",
"goals",
"assists",
"goals_assists",
"goals_pens",
"pens_made",
"pens_att",
"cards_yellow",
"cards_red",
"xg",
"npxg",
"xg_assist",
"npxg_xg_assist",
"progressive_carries",
"progressive_passes",
"progressive_passes_received",
"goals_per90",
"assists_per90",
"goals_assists_per90",
"goals_pens_per90",
"goals_assists_pens_per90",
"xg_per90",
"xg_assist_per90",
"xg_xg_assist_per90",
"npxg_per90",
"npxg_xg_assist_per90",
"matches"
]

player_stats = []
#dict for the player data 
player_data = {
"player name":[],
"nationality":[],
"position":[],
"team":[],
"age":[],
"birth_year":[],
"games":[],
"games_starts":[],
"minutes":[],
"minutes_90s":[],
"goals":[],
"assists":[],
"goals_assists":[],
"goals_pens":[],
"pens_made":[],
"pens_att":[],
"cards_yellow":[],
"cards_red":[],
"xg":[],
"npxg":[],
"xg_assist":[],
"npxg_xg_assist":[],
"progressive_carries":[],
"progressive_passes":[],
"progressive_passes_received":[],
"goals_per90":[],
"assists_per90":[],
"goals_assists_per90":[],
"goals_pens_per90":[],
"goals_assists_pens_per90":[],
"xg_per90":[],
"xg_assist_per90":[],
"xg_xg_assist_per90":[],
"npxg_per90":[],
"npxg_xg_assist_per90":[],
"matches":[]}


#loop for getting stats then adding to data_stat array 
#1)gets tag id from list 
#2)create text for .select() search
#3)adds to array


# finds standard stats table on fbref
full_table = soup.find(id= 'stats_standard')
stat_table = full_table.find('tbody').select("tr", class_="data-row=")
# one function for all decompose requests 
# removes standard stats: header, mid row headers, and match colomn
def decompose_items():
  for x in soup.select('tr.thead'):
    x.decompose()
  for x in full_table.find_all("tr"):
    x.th.decompose()
  for x in full_table.find("tbody").find_all('td',string='Matches'):
    x.decompose()
decompose_items()

# iterates through lists 
def list_iterator(list):
  for item in list:
    yield item  

# finds players in the table
def player_search(table):
  for data_row in list_iterator(table):
    player = data_row.select('td[data-stat="player"]')
    
    yield from player
   
# looks for the stat_id in a row of data 

# looks for the siblings in the same row of the player id, giving all related stats 
def row_search():
  for player_row in player_search(stat_table):
    name_text = player_row.get_text()
    player_data["player name"].append(name_text)
    all_stats = player_row.parent
    print(name_text)
    yield all_stats
def stat_search():
  for x in row_search():
    for stat_id in data_stats_ids:
      selected_id = 'td[data-stat="' + stat_id + '"]'
      print(stat_id)
      stat = x.select_one(selected_id)
      for text in stat:
        if text == None or text == "":
          stat_text = "0"
        else:
          stat_text = text.get_text()
          print(stat_text)    
stat_search()
