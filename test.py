import requests
from bs4 import BeautifulSoup
import array as arr

url = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
response = requests.get(url)
html_content = response.text.replace('<!--', '').replace('-->', '') #.replace() removes player data comment out  
soup = BeautifulSoup(html_content, 'lxml')

full_table= soup.find(id= 'stats_standard')
all_rows = full_table.find('tbody').select("tr", class_="data-row=")
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

def decompose_items():
  for x in soup.select('tr.thead'):
        x.decompose()
  for x in full_table.find_all("tr"):
        x.th.decompose()
  for x in full_table.find("tbody").find_all('td',string='Matches'):
        x.decompose()
decompose_items()
player_name_tag = []


def id_finder(item_being_searched):
    global stat_id
    data_select = []
    data_select.clear()
    for stat_id in data_stats_ids:
        selected_id = 'td[data-stat="'+  stat_id +'"]'
        for data in item_being_searched:
            for x in data:

                    data_select.append(data.select(selected_id))

    return data_select
print(id_finder(all_rows))


      

for z in player_name_tag:
    player_childern = z.find_next_siblings()
    
     
     
        
            

        




