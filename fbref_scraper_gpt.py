import requests
from bs4 import BeautifulSoup
import array as arr
import json
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import json
#import openai

cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  password="7410",
  database="standard_stats_db"
)

if cnx.is_connected():
  print("Connected to the MySQL database.")
else:
  print("Failed to connect to the MySQL database.")
cursor = cnx.cursor(buffered=True)

cursor.execute("""DROP TABLE IF EXISTS current_stats""")
cursor.execute("""DROP TABLE IF EXISTS expected_stats""")
cursor.execute("""DROP TABLE IF EXISTS player_info""")
cursor.execute("""DROP TABLE IF EXISTS teams""")
cursor.execute("""DROP TABLE IF EXISTS league""")
 

premier_league = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
la_liga = 'https://fbref.com/en/comps/12/stats/La-Liga-Stats'
serie_a= 'https://fbref.com/en/comps/11/stats/Serie-A-Stats'
bundesliga = 'https://fbref.com/en/comps/20/stats/Bundesliga-Stats'
ligue_1 = 'https://fbref.com/en/comps/13/stats/Ligue-1-Stats'


def get_data(url):
  response = requests.get(url)

  if response.ok:
  # .replace() removes player data comment out   
    html_content = response.text.replace('<!--', '').replace('-->', '')
    soup = BeautifulSoup(html_content, 'lxml')
  # Error trapping site response
    print("Retrieved HTML content.")
  else:
    print("Failed to retrieve the HTML content.")

  # list for tags for player data

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
  "npxg_xg_assist_per90"
  ]
  #player_stats dict creation
  player_stats = {}

  # finds standard stats table on fbref
  full_table = soup.find(id= 'stats_standard')
  stat_table = full_table.find('tbody').select("tr", class_="data-row=")

  # finds league and season
  table_caption = soup.find('caption').select_one("span").get_text().split(" ",1)
  league = table_caption[1]
  season = table_caption[0]
  season = season.replace("-", "/")
  print(league)
  print(season)

  # removes standard stats: header, mid row headers, and match colomn
  def decompose_items():
    for x in soup.select('tr.thead'):
      x.decompose()
    for x in full_table.find_all("tr"):
      x.th.decompose()
    for x in full_table.find("tbody").find_all('td',string='Matches'):
      x.decompose()
  decompose_items()

  # reformats age text: 36-099 -> 36
  def age_format(age):
    if isinstance(age,str) == False:
      return age
    else:
      age_parts = age.split('-')
      years = int(age_parts[0])
      return years

  # replace country code with country name
  def get_country_name(country_code):
    country_mapping = {
      'af': 'Afghanistan',
      'al': 'Albania',
      'dz': 'Algeria',
      'as': 'American Samoa',
      'ad': 'Andorra',
      'ao': 'Angola',
      'ai': 'Anguilla',
      'ag': 'Antigua and Barbuda',
      'ar': 'Argentina',
      'am': 'Armenia',
      'aw': 'Aruba',
      'au': 'Australia',
      'at': 'Austria',
      'az': 'Azerbaijan',
      'bs': 'Bahamas',
      'bh': 'Bahrain',
      'bd': 'Bangladesh',
      'bb': 'Barbados',
      'by': 'Belarus',
      'be': 'Belgium',
      'bz': 'Belize',
      'bj': 'Benin',
      'bm': 'Bermuda',
      'bt': 'Bhutan',
      'bo': 'Bolivia',
      'bq': 'Bonaire',
      'ba': 'Bosnia and Herzegovina',
      'bw': 'Botswana',
      'br': 'Brazil',
      'vg': 'British Virgin Islands',
      'bn': 'Brunei Darussalam',
      'bg': 'Bulgaria',
      'bf': 'Burkina Faso',
      'bi': 'Burundi',
      'kh': 'Cambodia',
      'cm': 'Cameroon',
      'ca': 'Canada',
      'cv': 'Cape Verde',
      'ky': 'Cayman Islands',
      'cf': 'Central African Republic',
      'td': 'Chad',
      'cl': 'Chile',
      'cn': 'China PR',
      'tw': 'Chinese Taipei',
      'co': 'Colombia',
      'xc': 'Commonwealth of Independent States',
      'km': 'Comoros',
      'cg': 'Congo',
      'cd': 'Congo DR',
      'ck': 'Cook Islands',
      'cr': 'Costa Rica',
      'ci': "Côte d'Ivoire",
      'hr': 'Croatia',
      'cu': 'Cuba',
      'cw': 'Curaçao',
      'cy': 'Cyprus',
      'cz': 'Czech Republic',
      'cs': 'Czechoslovakia',
      'dk': 'Denmark',
      'dj': 'Djibouti',
      'dm': 'Dominica',
      'do': 'Dominican Republic',
      'ec': 'Ecuador',
      'eg': 'Egypt',
      'sv': 'El Salvador',
      'eng': 'England',
      'gq': 'Equatorial Guinea',
      'er': 'Eritrea',
      'ee': 'Estonia',
      'sz': 'Eswatini',
      'et': 'Ethiopia',
      'fo': 'Faroe Islands',
      'fj': 'Fiji',
      'fi': 'Finland',
      'fr': 'France',
      'gf': 'French Guiana',
      'ga': 'Gabon',
      'gm': 'Gambia',
      'ge': 'Georgia',
      'de': 'Germany',
      'dd': 'Germany DR',
      'gh': 'Ghana',
      'gi': 'Gibraltar',
      'gb': 'Great Britain',
      'gr': 'Greece',
      'gd': 'Grenada',
      'gp': 'Guadeloupe',
      'gu': 'Guam',
      'gt': 'Guatemala',
      'gn': 'Guinea',
      'gw': 'Guinea-Bissau',
      'gy': 'Guyana',
      'ht': 'Haiti',
      'hn': 'Honduras',
      'hk': 'Hong Kong',
      'hu': 'Hungary',
      'is': 'Iceland',
      'in': 'India',
      'id': 'Indonesia',
      'ir': 'IR Iran',
      'iq': 'Iraq',
      'il': 'Israel',
      'it': 'Italy',
      'jm': 'Jamaica',
      'jp': 'Japan',
      'jo': 'Jordan',
      'kz': 'Kazakhstan',
      'ke': 'Kenya',
      'kp': 'Korea DPR',
      'kr': 'Korea Republic',
      'xk': 'Kosovo',
      'kw': 'Kuwait',
      'kg': 'Kyrgyz Republic',
      'la': 'Laos',
      'lv': 'Latvia',
      'lb': 'Lebanon',
      'ls': 'Lesotho',
      'lr': 'Liberia',
      'ly': 'Libya',
      'li': 'Liechtenstein',
      'lt': 'Lithuania',
      'lu': 'Luxembourg',
      'mo': 'Macau',
      'mg': 'Madagascar',
      'mw': 'Malawi',
      'my': 'Malaysia',
      'mv': 'Maldives',
      'ml': 'Mali',
      'mt': 'Malta',
      'mq': 'Martinique',
      'mr': 'Mauritania',
      'mu': 'Mauritius',
      'mx': 'Mexico',
      'md': 'Moldova',
      'mn': 'Mongolia',
      'me': 'Montenegro',
      'ms': 'Montserrat',
      'ma': 'Morocco',
      'mz': 'Mozambique',
      'mm': 'Myanmar',
      'na': 'Namibia',
      'np': 'Nepal',
      'nl': 'Netherlands',
      'nc': 'New Caledonia',
      'nz': 'New Zealand',
      'ni': 'Nicaragua',
      'ne': 'Niger',
      'ng': 'Nigeria',
      'mk': 'North Macedonia',
      'nir': 'Northern Ireland',
      'no': 'Norway',
      'om': 'Oman',
      'pk': 'Pakistan',
      'ps': 'Palestine',
      'pa': 'Panama',
      'pg': 'Papua New Guinea',
      'py': 'Paraguay',
      'pe': 'Peru',
      'ph': 'Philippines',
      'pl': 'Poland',
      'pt': 'Portugal',
      'pr': 'Puerto Rico',
      'qa': 'Qatar',
      'ie': 'Republic of Ireland',
      're': 'Réunion',
      'ro': 'Romania',
      'ru': 'Russia',
      'rw': 'Rwanda',
      'ws': 'Samoa',
      'sm': 'San Marino',
      'st': 'São Tomé and Príncipe',
      'sa': 'Saudi Arabia',
      'sct': 'Scotland',
      'sn': 'Senegal',
      'sk': 'Slovakia',
      'rs': 'Serbia',
      'su': 'Soviet Union',
      'es': 'Spain',
      'lk': 'Sri Lanka',
      'kn': 'St. Kitts and Nevis',
      'lc': 'St. Lucia',
      'vc': 'St. Vincent and the Grenadines',
      'sd': 'Sudan',
      'sr': 'Suriname',
      'se': 'Sweden',
      'ch': 'Switzerland',
      'sy': 'Syria',
      'pf': 'Tahiti',
      'tj': 'Tajikistan',
      'tz': 'Tanzania',
      'th': 'Thailand',
      'tl': 'Timor-Leste',
      'tg': 'Togo',
      'to': 'Tonga',
      'tt': 'Trinidad and Tobago',
      'tn': 'Tunisia',
      'tr': 'Türkiye',
      'tm': 'Turkmenistan',
      'tc': 'Turks and Caicos Islands',
      'ug': 'Uganda',
      'ua': 'Ukraine',
      'ae': 'United Arab Emirates',
      'us': 'United States',
      'uy': 'Uruguay',
      'vi': 'US Virgin Islands',
      'uz': 'Uzbekistan',
      'vu': 'Vanuatu',
      've': 'Venezuela',
      'vn': 'Vietnam',
      'wls': 'Wales',
      'ye': 'Yemen',
      'yu': 'Yugoslavia',
      'zm': 'Zambia',
      'zw': 'Zimbabwe',
      'za': 'South Africa'
  }
    for code, country in country_mapping.items():
      if isinstance(country_code,str) == False:
        continue
      else:
        country_code = country_code.split()[0]
        if code == country_code:
          return country
        

  # list iterator
  def list_iterator(list):
    for item in list:
      yield item  

  # finds player tags in table
  def get_player_tags (table):
    for data_row in list_iterator(table):
      player = data_row.select('td[data-stat="player"]')
      yield from player
    
  # finds parent of "player" tag
  def get_player_parents():
    for player_row in get_player_tags(stat_table):
      name_text = player_row.get_text()
      all_stats = player_row.parent
  # prints each player name found
      #print(name_text)
      yield all_stats

  # converts stat text to int or float
  def float_zero_int(text):
    text = text.replace(",", "")
    try:
      value = int(text)
      return value
    except ValueError:
      try:
        value = float(text)
        return value
      except ValueError:
        if text == "0" or text == "":
          return 0
        else:
          return text

  # converts position code to position name
  def get_position(position):
      position_mapping = {
          'GK': 'Goalkeeper',
          'DF': 'Defender',
          'MF': 'Midfielder',
          'FW': 'Forward',
          'FB': 'Fullback',
          'LB': 'Left Back',
          'RB': 'Right Back',
          'CB': 'Center Back',
          'DM': 'Defensive Midfielder',
          'CM': 'Central Midfielder',
          'LM': 'Left Midfielder',
          'RM': 'Right Midfielder',
          'WM': 'Wide Midfielder',
          'LW': 'Left Winger',
          'RW': 'Right Winger',
          'AM': 'Attacking Midfielder'
      }

      positions = []
      current_position = ''

      for x in position:
          current_position += x
          if current_position in position_mapping:
              positions.append(position_mapping[current_position])
              current_position = ''

      if positions:
          return ', '.join(positions)
      else:
          return 'Unknown Position'      

  # finds and adds stats to player_stats dict
  def get_stats():
    for stat_group in get_player_parents():
      for stat_id in data_stats_ids:
        selected_id = 'td[data-stat="' + stat_id + '"]'     
        stat = stat_group.select_one(selected_id)
        stat_text = stat.get_text() if stat else print("None")
        
      # converts stat text to int or float
        stat_text= float_zero_int(stat_text)
        if stat_id == "player":
          this_player = stat_text
          # update() adds player to player_stats dict
          player_stats.update({this_player:{}})

      # finds country name from country code
        if stat_id == "nationality":
          #print(stat_text)
          stat_text = get_country_name(stat_text)
          
      # converts age in days to date of birth
        if stat_id == "age":
          stat_text = age_format(stat_text)
      # converts position codes to position names
        if stat_id == "position":
          stat_text = get_position(stat_text)
      # adds stats to player name in dict
        player_stats[this_player].update({stat_id:stat_text})

  # run get_stats() function 
  get_stats()

  # converts player_stats dict to json for easy reading
  player_stats_json = json.dumps(player_stats, indent = 4, ensure_ascii=False)
  #print (player_stats_json)

  # connect to the MySQL database

  ###################################################################################
  def league_table(league, season):
    league_table_query = """
      CREATE TABLE IF NOT EXISTS league (
        league_id INT AUTO_INCREMENT PRIMARY KEY,
        league_name VARCHAR(255),
        season VARCHAR(255)
      )
      """
    cursor.execute(league_table_query)
    league_insert_query = """
      INSERT INTO league (league_name, season)
      VALUES ( %s, %s)
      """
    cursor.execute(league_insert_query, (league, season))
    cnx.commit()
    league_id = cursor.lastrowid
    return league_id

  ###################################################################################
  def team_table (team, league_id):
      team_id = []
      team_table_query = """ 
      CREATE TABLE IF NOT EXISTS teams (
        team_id INT AUTO_INCREMENT PRIMARY KEY,
        team_name VARCHAR(255),
        league_id INT,
        FOREIGN KEY (league_id) REFERENCES league(league_id)
      )
      """
      cursor.execute(team_table_query)
      team_insert_query = """
        INSERT INTO teams (team_name, league_id)
        SELECT %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM teams 
            WHERE team_name = %s
        );
      """
      cursor.execute(team_insert_query, (team, league_id, team))
      cnx.commit()

      find_team_id = """ SELECT team_id FROM teams WHERE team_name = (%s) """
      cursor.execute(find_team_id, (team,))
      fetch_team_id = cursor.fetchone()
      fetch_team_id = fetch_team_id[0]
      return fetch_team_id  
  ###################################################################################
  def player_table (player, position, team_id, nationality, age, birth_year):
    
    player_table_query = """ 
    CREATE TABLE IF NOT EXISTS player_info (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player VARCHAR(255),
    position VARCHAR(255),
    team_id INT,
    nationality VARCHAR(255),
    age INT,
    birth_year INT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
    )
    """
    cursor.execute(player_table_query)
    player_insert_query = """
    INSERT INTO player_info (player, position, team_id, nationality, age, birth_year)
    VALUES ( %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(player_insert_query, (player, position, team_id, nationality, age, birth_year))
    cnx.commit()
    player_id = cursor.lastrowid
    return player_id

  ###################################################################################
  def current_stats_table (player_id, games, games_starts, minutes, minutes_90s, goals, 
              assists, goals_assists, goals_pens, pens_made, pens_att, cards_yellow, 
              cards_red, progressive_carries, progressive_passes, progressive_passes_received, goals_per90, assists_per90, goals_assists_per90, goals_pens_per90, goals_assists_pens_per90
  ):
    
    current_stats_table_query ="""
        CREATE TABLE IF NOT EXISTS current_stats (
              current_stats_id INT AUTO_INCREMENT PRIMARY KEY,
              player_id INT,
              games INT,
              games_starts INT,
              minutes INT,
              minutes_90s FLOAT,
              goals INT,
              assists INT,
              goals_assists INT,
              goals_pens INT,
              pens_made INT,
              pens_att INT,
              cards_yellow INT,
              cards_red INT,
              progressive_carries INT,  
              progressive_passes INT,   
              progressive_passes_received INT,
              goals_per90 FLOAT,
              assists_per90 FLOAT,
              goals_assists_per90 FLOAT,
              goals_pens_per90 FLOAT,
              goals_assists_pens_per90 FLOAT,
              FOREIGN KEY (player_id) REFERENCES player_info(player_id)
          )
      """
    cursor.execute(current_stats_table_query)
    current_stats_insert_query = """
              INSERT INTO current_stats(
              player_id,
              games, 
              games_starts, 
              minutes, 
              minutes_90s, 
              goals, 
              assists, 
              goals_assists, 
              goals_pens, 
              pens_made, 
              pens_att, 
              cards_yellow, 
              cards_red, 
              progressive_carries, 
              progressive_passes, 
              progressive_passes_received,
              goals_per90,
              assists_per90,
              goals_assists_per90,
              goals_pens_per90,
              goals_assists_pens_per90
          )
          VALUES 
              (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
      """
    cursor.execute(current_stats_insert_query, (player_id, games, games_starts, minutes, minutes_90s, goals, 
              assists, goals_assists, goals_pens, pens_made, pens_att, cards_yellow, 
              cards_red, progressive_carries, progressive_passes, progressive_passes_received,
              goals_per90, assists_per90, goals_assists_per90, goals_pens_per90, goals_assists_pens_per90
              ))
    cnx.commit()
  ###################################################################################

  def expected_stats_table (player_id, xg, npxg, xg_assist,
                      npxg_xg_assist,xg_per90, xg_assist_per90, 
                      xg_xg_assist_per90, npxg_per90, npxg_xg_assist_per90):
    
    expected_stats_table_query =("""
          CREATE TABLE IF NOT EXISTS expected_stats (
              expected_stats_id INT AUTO_INCREMENT PRIMARY KEY,
              player_id INT,
              xg FLOAT,
              npxg FLOAT,
              xg_assist FLOAT,
              npxg_xg_assist FLOAT,
              xg_per90 FLOAT,
              xg_assist_per90 FLOAT,
              xg_xg_assist_per90 FLOAT,
              npxg_per90 FLOAT,
              npxg_xg_assist_per90 FLOAT,
              FOREIGN KEY (player_id) REFERENCES player_info(player_id)
          );
      """)
    cursor.execute(expected_stats_table_query)
    expected_stats_insert_query = """
              INSERT INTO expected_stats(
              player_id,
              xg,
              npxg,
              xg_assist,
              npxg_xg_assist,
              xg_per90,
              xg_assist_per90,
              xg_xg_assist_per90,
              npxg_per90, 
              npxg_xg_assist_per90
              )
              VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
          """
    cursor.execute(expected_stats_insert_query, (player_id,xg, npxg, xg_assist, 
                                                npxg_xg_assist, xg_per90, xg_assist_per90, 
                                                xg_xg_assist_per90, npxg_per90, npxg_xg_assist_per90))
    cnx.commit()

  ###################################################################################
  def create_tables():
    league_id = league_table(league, season)
    
  
    for player, stats in player_stats.items():
      player = stats.get('player', '')
      position = stats.get('position', '')
      team = stats.get('team', '')
      nationality = stats.get('nationality', '')
      age = stats.get('age', '')
      birth_year = stats.get('birth_year', '')
      games = stats.get('games', '')
      games_starts = stats.get('games_starts', '')
      minutes = stats.get('minutes', '')
      minutes_90s = stats.get('minutes_90s', '')
      goals = stats.get('goals', '')
      assists = stats.get('assists', '')
      goals_assists = stats.get('goals_assists', '')
      goals_pens = stats.get('goals_pens', '')
      pens_made = stats.get('pens_made', '')
      pens_att = stats.get('pens_att', '')
      cards_yellow = stats.get('cards_yellow', '')
      cards_red = stats.get('cards_red', '')
      xg = stats.get('xg', '')
      npxg = stats.get('npxg', '')
      xg_assist = stats.get('xg_assist', '')
      npxg_xg_assist = stats.get('npxg_xg_assist', '')
      progressive_carries = stats.get('progressive_carries', '')
      progressive_passes = stats.get('progressive_passes', '')
      progressive_passes_received = stats.get('progressive_passes_received', '')
      goals_per90 = stats.get('goals_per90', '')
      assists_per90 = stats.get('assists_per90', '')
      goals_assists_per90 = stats.get('goals_assists_per90', '')
      goals_pens_per90 = stats.get('goals_pens_per90', '')
      goals_assists_pens_per90 = stats.get('goals_assists_pens_per90', '')
      xg_per90 = stats.get('xg_per90', '')
      xg_assist_per90 = stats.get('xg_assist_per90', '')
      xg_xg_assist_per90 = stats.get('xg_xg_assist_per90', '')
      npxg_per90 = stats.get('npxg_per90', '')
      npxg_xg_assist_per90 = stats.get('npxg_xg_assist_per90', '')
      
      team_id = team_table(team,league_id)

      player_id = player_table(player, position, team_id, nationality, age, birth_year) 
    
      
      current_stats_table(player_id,games, games_starts, minutes, minutes_90s, goals, 
              assists, goals_assists, goals_pens, pens_made, pens_att, cards_yellow, 
              cards_red, progressive_carries, progressive_passes, progressive_passes_received,
              goals_per90, assists_per90, goals_assists_per90, goals_pens_per90, goals_assists_pens_per90
              )
      
      expected_stats_table (player_id, xg, npxg, xg_assist,
                      npxg_xg_assist,xg_per90, xg_assist_per90, 
                      xg_xg_assist_per90, npxg_per90, npxg_xg_assist_per90)
      
  create_tables()
   
  cnx.commit()
  

get_data(premier_league)
get_data(la_liga)
get_data(serie_a)
get_data(bundesliga)
get_data(ligue_1)

"""
# CHATGPT 3.5 INTEGRATION ##############################################################################################################
def gpt_fetch_data(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# Function to interact with GPT-3.5
def query_gpt_3_5(prompt):
    openai.api_key = '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'
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      max_tokens=150
    )
    return response.choices[0].text.strip()

# Main logic
def main():
    data = gpt_fetch_data("SELECT * FROM your_table")
    # Process and format your data as needed
    formatted_data = format_data_for_gpt(data)

    # Query GPT-3.5
    gpt_response = query_gpt_3_5(formatted_data)

    # Process GPT-3.5 response
    process_gpt_response(gpt_response)

if __name__ == "__main__":
    main()



"""
cursor.close()
cnx.close()