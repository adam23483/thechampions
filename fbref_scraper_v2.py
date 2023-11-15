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



#finds standard stats table on fbref
full_table= soup.find(id= 'stats_standard')

#removes standard stats table header
for sh in soup.select('tr.thead'):
  sh.decompose()

#removes mid row headers form standard stats table
for th in full_table.find_all("tr"):
  th.th.decompose()
#removes match column form standard stats table
for match in full_table.find("tbody").find_all('td',string='Matches'):
  match.decompose()
  
#loop for getting stats then adding to data_stat array 
  #1)gets tag id from list 
  #2)create text for .select() search
  #3)adds to array

for data_row in full_table.find('tbody').select("tr", class_="data-row="):
  for stat_id in iter(data_stats_ids):
    selected_id = 'td[data-stat="'+ stat_id +'"]'
    all_data_rows = data_row.select(selected_id)
  
  if stat_id == "player":
    for player_data in all_data_rows:
      name_siblings = player_data.find_next_siblings()
      name = player_data.get_text()
      player_stats["player"].append(name) 
      print(name)
      for k in name_siblings:
      
      
       

        

        for x in name_siblings:
          if all_data_rows != None:
            info = x.get_text()
            z = str(stat_id + " : " + info)
            print(z)

          
        
          
            
          

        




'''
 for x in name_siblings:
          
            for y in all_data_td:
               '''
 

#notes for me 
# 1) try out getting the data-row tag should help orgonzie data
# 2) sort how array is strutured and how data is placed into it 
# 3) speeed up code takes forever to get all the data




