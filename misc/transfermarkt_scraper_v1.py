#No longer being worked on using the transfermarkt API instead due to some data being requested from the API i cant access through scraping
# Description: Script scrapes the player market values from the transfermarkt for the top 5 European leagues



import requests
from bs4 import BeautifulSoup
import math
import re


premier_league_market_value = "https://www.transfermarkt.us/premier-league/marktwertaenderungen/wettbewerb/GB1"
la_liga_market_value = "https://www.transfermarkt.us/primera-division/marktwerte/wettbewerb/ES1"
serie_a_market_value= "https://www.transfermarkt.us/serie-a/marktwerte/wettbewerb/IT1"
bundesliga_market_value = "https://www.transfermarkt.us/bundesliga/marktwerte/wettbewerb/L1" 
ligue_1_market_value = "https://www.transfermarkt.us/ligue-1/marktwerte/wettbewerb/FR1"

# Define the headers - bs4 acts like a user agent
headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }
 
def get_league_pages(league_url,headers):

    table_urls_list = [] #pages of the player market values for league 
    response = requests.get(league_url, headers=headers)
    response.status_code
    soup = BeautifulSoup(response.content, "lxml")
    # finds pages  
    table_pages = soup.find("ul", class_="tm-pagination")
    page_links = table_pages.find_all("a")
    
    for link in page_links:
        page_number = link.get_text()
        try:
            int(page_number)
            link = link.get("href")
            # creates full url for each page
            full_url = league_url + link
            table_urls_list.append(full_url)
            
        except:
            pass
    #print(table_urls_list)
    return table_urls_list

def get_mrkt_values(table_urls_list, headers):
        
    for url in table_urls_list:        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        # table rows of player market values 
        value_table = soup.find("div", class_="responsive-table").find("tbody").find_all("tr",{"class": ["odd", "even",]})
    
        for player in value_table:
            player_title = player.find("td", class_="hauptlink")
            market_values = player.find("td",  {"class": ["rechts hauptlink", "rechts hauptlink mwHoechstwertKarriere"]})
            player_info = player.find_all("img", class_="flaggenrahmen")
            
            if player_title is not None:
                # finds player name through title attribute
                player_name = player_title.find('a')['title']
                print(player_name)
            #finds market values
            if market_values is not None:
                for value in market_values:
                    fee = value.get_text()
                    print(fee)
                    
            #if player_info is not None:
                
                
            

get_mrkt_values(get_league_pages(premier_league_market_value, headers), headers)        

get_league_pages(premier_league_market_value, headers)

# sample of html to scrape 
#<td class="zentriert"><a href="/brighton-amp-hove-albion/startseite/verein/1237/saison_id/2023" title="Brighton &amp; Hove Albion"><img alt="Brighton &amp; Hove Albion" class="" src="https://tmssl.akamaized.net/images/wappen/verysmall/1237.png?lm=1492718902" title="Brighton &amp; Hove Albion"/></a></td>