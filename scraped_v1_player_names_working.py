import requests
from bs4 import BeautifulSoup

url = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
response = requests.get(url)
html_content = response.text.replace('<!--', '').replace('-->', '') #removes player data comment out  
soup = BeautifulSoup(html_content, 'lxml')

cell_data =[]
player_name =[]

full_table= soup.find(id= 'stats_standard')

for th in full_table.find_all("tr"):
  th.th.decompose()
for sh in soup.select('tr.thead'):
  sh.decompose()

#data = [x.text for x in 
for x in soup.select('td[data-stat="player"]'): 
  data = x.get_text()
  player_name.append(data)


print(player_name[0])