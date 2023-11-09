

for row in soup.select('table#stats tbody tr'):
    tds = [td.get_text(strip=True) for td in row.select('td, th')]
    print(*tds)
    
[item['data-bin'] for item in bs.find_all('ul', attrs={'data-bin' : True})]

players = ""
table = soup.find("table")
rows = table.find_all('tr')
for row in rows: 
    players = row.find('td', attrs={'data-stat':'player'}) 

print(players)

players = ""
table = soup.find("table")
rows = table.find_all('tr')
for row in rows: 
    players = row.find('td', attrs={'data-stat':'player'}) 

print(players)

soup = BeautifulSoup(response, 'html.parser')
stat_data = soup.find('a'., , {'herf': True}).text

player = stat_data'



for rows in table:
    cells = rows.find_all('td')
    if len(cells) < 1:
        continue
    rn = cells[0].content 
    
    print(rn.text)

for rows in table:
    cells = rows.find('tr')
    if len(cells) < 1:
        continue
    rn = cells[0]
     
    print(rn.text)


    for data_row in table:
        row = data_row.find()