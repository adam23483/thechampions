import requests
from bs4 import BeautifulSoup

url = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
response = requests.get(url)
html_content = response.text.replace('<!--', '').replace('-->', '') #.replace() removes player data comment out  
soup = BeautifulSoup(html_content, 'lxml')

#list for tags for player data. EX data-stat ="player" --> player name 
data_stats  = [
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

#finds standard stats table on fbref
full_table= soup.find(id= 'stats_standard')

#removes standard stats table header
for sh in soup.select('tr.thead'):
  sh.decompose()

#removes mid row headers form standard stats table
for th in full_table.find_all("tr"):
  th.th.decompose()

#loop for getting stats then adding to data_stat array 
  #1)gets tag id from list 
  #2)create text for .select() search
  #3)adds to array  
for stat_id in iter(data_stats):  
  selected_id = str('td[data-stat="'+ stat_id +'"]') 
  for data in soup.select(selected_id):   
    data = x.get_text() 
    data_stats.append(data) 
print(data_stats) 

