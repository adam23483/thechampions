import requests
from bs4 import BeautifulSoup
import array as arr

url = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
response = requests.get(url)
html_content = response.text.replace('<!--', '').replace('-->', '') #.replace() removes player data comment out  
soup = BeautifulSoup(html_content, 'lxml')

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
player_stats = {"player":[]}
#loop for getting stats then adding to data_stat array 
  #1)gets tag id from list 
  #2)create text for .select() search
  #3)adds to array


#finds standard stats table on fbref
full_table= soup.find(id= 'stats_standard')

#one function for all decompose requests 
#removes standard stats: header, mid row headers, and match colomn
def decompose_items():
  for x in soup.select('tr.thead'):
        x.decompose()
  for x in full_table.find_all("tr"):
        x.th.decompose()
  for x in full_table.find("tbody").find_all('td',string='Matches'):
        x.decompose()
decompose_items()
 
def stat_id_selector(data_stats_ids):
    selected_id =[]
    for stat_id in data_stats_ids:
        selected_id = 'td[data-stat="'+  stat_id +'"]'

        
      

stat_id_selector(data_stats_ids)


    
def id_selector(stat_id):
  stat_id_selector()
  
  return selected_id

"""def player_stat_creator(selected_id):
  id_selector()
  for data_row in full_table.find('tbody').select("tr", class_="data-row="):
    current_data = data_row.select(selected_id)
    return current_data
  
def player_finder(current_data,stat_id):
    player_stat_creator()
    if stat_id == "player":
       player_stats["player"].append(current_data.get_text())
       name_siblings = current_data.find_next_siblings()
    return name_siblings

def find_data(name_siblings,stat_id,selected_id):
  player_finder()
  for this_player in name_siblings:
     player_stat_creator(name_siblings)

     player_stats["player"].append(stat_id + ":" +)
     player_stats["player"][stat_id].append()  
if stat_id_selector() == ""
def data_id_tag():
  for data in
def id_matcher():    
  for stat_id_fucntion in iter(data_stats_ids):
    selected_id = 'td[data-stat="'+ stat_id_fucntion +'"]'

      return all_data_rows

def player_row_data():
  for player_data in id_matcher:
    
  return name_siblings

print(all_data_rows)

if id_matcher(stat_id_fuctio)

    name = player_data.get_text()
    player_stats["player"].append(name) 
    print(name)

          for x in name_siblings:
        if all_data_rows != None:
          info = x.get_text()
          z = str(stat_id + " : " + info)
          print(z)


#notes for me 
# 1) try out getting the data-row tag should help orgonzie data
# 2) sort how array is strutured and how data is placed into it 
# 3) speeed up code takes forever to get all the data




"""