import requests
from bs4 import BeautifulSoup

url = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
response = requests.get(url)
html_content = response.text.replace('<!--', '').replace('-->', '') #removes commented out code   
soup = BeautifulSoup(html_content, 'lxml') 

#finds standard stats table on fbref
full_table= soup.find(id= 'stats_standard')   

#removes standard stats table header
for sh in soup.select('tr.thead'): 
  sh.decompose()

#removes mid row headers form standard stats table
for th in full_table.find_all("tr"):  
  th.th.decompose()

#finds <td? tags with player class/id in standard stats table, parses text, then adds to player_name list
player_name =[] #create list for player names
for x in soup.select('td[data-stat="player"]'): 
  data = x.get_text() 
  player_name.append(data)

#returns first player name in list 
print(player_name[0])