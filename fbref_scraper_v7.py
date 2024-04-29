import requests
from bs4 import BeautifulSoup
import mysql.connector
import json
import time
import asyncio
import aiohttp


# mysql database connection ###################################################
cnx = mysql.connector.connect(
host="localhost",
user="root",
password="7410",
database="standard_stats_db"
)
if cnx.is_connected():
    print("Connected to the MySQL database.")
    cursor = cnx.cursor()
else:
    print("Failed to connect to the MySQL database.")

# drops existing tables in database ###########################################
def drop_table(cursor):
# disable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")   
    try:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
# remove tables in database  
        for (db_table,) in tables:
                cursor.execute(f"DROP TABLE IF EXISTS `{db_table}`;")
                print(f"Dropped table: {db_table}")
# re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;") 
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
drop_table(cursor)
                         
# finds datatype for each stat ################################################
def get_datatype(all_stats, id_datatype):
    player_dict = all_stats["players"]
    for table, data in player_dict.items():
        for player, stats in data.items():
            if player == "player_id":
                continue
            if player == "player_stats":
                for stat, value in stats.items():
                    if stat not in id_datatype:
                        try:
                            this_value = int(value)
                            id_datatype.update({stat: "INT"})
                        except ValueError:
                            try:
                                this_value = float(value)
                                id_datatype.update({stat: "FLOAT"})
                            except ValueError:
                                id_datatype.update({stat: "VARCHAR(255)"})

# converts country code to country name #######################################                         
def get_country_name(country_code):
    # country code mapping
    country_mapping = {
      "af": "Afghanistan",
      "al": "Albania",
      "dz": "Algeria",
      "as": "American Samoa",
      "ad": "Andorra",
      "ao": "Angola",
      "ai": "Anguilla",
      "ag": "Antigua and Barbuda",
      "ar": "Argentina",
      "am": "Armenia",
      "aw": "Aruba",
      "au": "Australia",
      "at": "Austria",
      "az": "Azerbaijan",
      "bs": "Bahamas",
      "bh": "Bahrain",
      "bd": "Bangladesh",
      "bb": "Barbados",
      "by": "Belarus",
      "be": "Belgium",
      "bz": "Belize",
      "bj": "Benin",
      "bm": "Bermuda",
      "bt": "Bhutan",
      "bo": "Bolivia",
      "bq": "Bonaire",
      "ba": "Bosnia and Herzegovina",
      "bw": "Botswana",
      "br": "Brazil",
      "vg": "British Virgin Islands",
      "bn": "Brunei Darussalam",
      "bg": "Bulgaria",
      "bf": "Burkina Faso",
      "bi": "Burundi",
      "kh": "Cambodia",
      "cm": "Cameroon",
      "ca": "Canada",
      "cv": "Cape Verde",
      "ky": "Cayman Islands",
      "cf": "Central African Republic",
      "td": "Chad",
      "cl": "Chile",
      "cn": "China PR",
      "tw": "Chinese Taipei",
      "co": "Colombia",
      "xc": "Commonwealth of Independent States",
      "km": "Comoros",
      "cg": "Congo",
      "cd": "Congo DR",
      "ck": "Cook Islands",
      "cr": "Costa Rica",
      "ci": "Ivory Coast",
      "hr": "Croatia",
      "cu": "Cuba",
      "cw": "Curaçao",
      "cy": "Cyprus",
      "cz": "Czech Republic",
      "cs": "Czechoslovakia",
      "dk": "Denmark",
      "dj": "Djibouti",
      "dm": "Dominica",
      "do": "Dominican Republic",
      "ec": "Ecuador",
      "eg": "Egypt",
      "sv": "El Salvador",
      "eng": "England",
      "gq": "Equatorial Guinea",
      "er": "Eritrea",
      "ee": "Estonia",
      "sz": "Eswatini",
      "et": "Ethiopia",
      "fo": "Faroe Islands",
      "fj": "Fiji",
      "fi": "Finland",
      "fr": "France",
      "gf": "French Guiana",
      "ga": "Gabon",
      "gm": "Gambia",
      "ge": "Georgia",
      "de": "Germany",
      "dd": "Germany DR",
      "gh": "Ghana",
      "gi": "Gibraltar",
      "gb": "Great Britain",
      "gr": "Greece",
      "gd": "Grenada",
      "gp": "Guadeloupe",
      "gu": "Guam",
      "gt": "Guatemala",
      "gn": "Guinea",
      "gw": "Guinea-Bissau",
      "gy": "Guyana",
      "ht": "Haiti",
      "hn": "Honduras",
      "hk": "Hong Kong",
      "hu": "Hungary",
      "is": "Iceland",
      "in": "India",
      "id": "Indonesia",
      "ir": "IR Iran",
      "iq": "Iraq",
      "il": "Israel",
      "it": "Italy",
      "jm": "Jamaica",
      "jp": "Japan",
      "jo": "Jordan",
      "kz": "Kazakhstan",
      "ke": "Kenya",
      "kp": "Korea DPR",
      "kr": "Korea Republic",
      "xk": "Kosovo",
      "kw": "Kuwait",
      "kg": "Kyrgyz Republic",
      "la": "Laos",
      "lv": "Latvia",
      "lb": "Lebanon",
      "ls": "Lesotho",
      "lr": "Liberia",
      "ly": "Libya",
      "li": "Liechtenstein",
      "lt": "Lithuania",
      "lu": "Luxembourg",
      "mo": "Macau",
      "mg": "Madagascar",
      "mw": "Malawi",
      "my": "Malaysia",
      "mv": "Maldives",
      "ml": "Mali",
      "mt": "Malta",
      "mq": "Martinique",
      "mr": "Mauritania",
      "mu": "Mauritius",
      "mx": "Mexico",
      "md": "Moldova",
      "mn": "Mongolia",
      "me": "Montenegro",
      "ms": "Montserrat",
      "ma": "Morocco",
      "mz": "Mozambique",
      "mm": "Myanmar",
      "na": "Namibia",
      "np": "Nepal",
      "nl": "Netherlands",
      "nc": "New Caledonia",
      "nz": "New Zealand",
      "ni": "Nicaragua",
      "ne": "Niger",
      "ng": "Nigeria",
      "mk": "North Macedonia",
      "nir": "Northern Ireland",
      "no": "Norway",
      "om": "Oman",
      "pk": "Pakistan",
      "ps": "Palestine",
      "pa": "Panama",
      "pg": "Papua New Guinea",
      "py": "Paraguay",
      "pe": "Peru",
      "ph": "Philippines",
      "pl": "Poland",
      "pt": "Portugal",
      "pr": "Puerto Rico",
      "qa": "Qatar",
      "ie": "Republic of Ireland",
      "re": "Réunion",
      "ro": "Romania",
      "ru": "Russia",
      "rw": "Rwanda",
      "ws": "Samoa",
      "sm": "San Marino",
      "st": "São Tomé and Príncipe",
      "sa": "Saudi Arabia",
      "sct": "Scotland",
      "sn": "Senegal",
      "sk": "Slovakia",
      "rs": "Serbia",
      "su": "Soviet Union",
      "es": "Spain",
      "lk": "Sri Lanka",
      "kn": "St. Kitts and Nevis",
      "lc": "St. Lucia",
      "vc": "St. Vincent and the Grenadines",
      "sd": "Sudan",
      "sr": "Suriname",
      "se": "Sweden",
      "ch": "Switzerland",
      "sy": "Syria",
      "pf": "Tahiti",
      "tj": "Tajikistan",
      "tz": "Tanzania",
      "th": "Thailand",
      "tl": "Timor-Leste",
      "tg": "Togo",
      "to": "Tonga",
      "tt": "Trinidad and Tobago",
      "tn": "Tunisia",
      "tr": "Türkiye",
      "tm": "Turkmenistan",
      "tc": "Turks and Caicos Islands",
      "ug": "Uganda",
      "ua": "Ukraine",
      "ae": "United Arab Emirates",
      "us": "United States",
      "uy": "Uruguay",
      "vi": "US Virgin Islands",
      "uz": "Uzbekistan",
      "vu": "Vanuatu",
      "ve": "Venezuela",
      "vn": "Vietnam",
      "wls": "Wales",
      "ye": "Yemen",
      "yu": "Yugoslavia",
      "zm": "Zambia",
      "zw": "Zimbabwe",
      "za": "South Africa",
      "si": "Slovenia",
  }
    for code, country in country_mapping.items():
      if isinstance(country_code,str) == False:
        continue
      else:
        country_code = country_code.split()[0]
        if code == country_code:
          return country

# converts string to float or int or leaves as string #########################
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

# converts age to years #######################################################    
def age_format(age):
    if isinstance(age,str) == False:
      return age
    else:
      age_parts = age.split("-")
      years = int(age_parts[0])
      return years

# converts position code to position name #####################################
def get_position(position):
      position_mapping = { 
          "GK": "Goalkeeper",
          "DF": "Defender",
          "MF": "Midfielder",
          "FW": "Forward",
          "FB": "Fullback",
          "LB": "Left Back",
          "RB": "Right Back",
          "CB": "Center Back",
          "DM": "Defensive Midfielder",
          "CM": "Central Midfielder",
          "LM": "Left Midfielder",
          "RM": "Right Midfielder",
          "WM": "Wide Midfielder",
          "LW": "Left Winger",
          "RW": "Right Winger",
          "AM": "Attacking Midfielder"
      }
      positions = []
      current_position = ""

      for x in position:
          current_position += x
          if current_position in position_mapping:
              positions.append(position_mapping[current_position])
              current_position = ""

      if positions:
          return ", ".join(positions)
      else:
          return "Unknown Position"  

# finds league and season #####################################################
def get_caption(soup):
    if soup.find("caption") is None:
        return "Failed HTML Response caption found"
    table_caption = soup.find("caption").select_one("span").get_text().split(" ",1)
    league = table_caption[1]
    season = table_caption[0]
    season = season.replace("-", "/")
    return league, season

# finds player id based on matching stats #####################################
def get_all_players(stats_dict, all_players):
    info = ["player_id","player","team", "position", "age", "birth_year","nationality", "player_name"]
    for player, stats in stats_dict["standard_stats"].items():    
        all_players.update({player:{"player_id":stats["player_id"]}})
        all_players[player].update({"player_info":{}})
        all_players[player].update({"player_stats":{"player_id":stats["player_id"]}}) 
        for key, values in stats.items():
            if key in info:
                all_players[player]["player_info"].update({key:values})
            else:
                all_players[player]["player_stats"].update({key:values})

# checks if player stats match existing players stats #########################
def stats_match_count(player, stats, all_players):
    total_matches = 0
    player_info = all_players[player]["player_info"]
    player_stats = all_players[player]["player_stats"]
    for stat, value in stats.items():
        if stat in player_info and player_info[stat] == value:
            total_matches += 1
        elif stat in player_stats and player_stats[stat] == value:
            total_matches += 1
        else: 
            continue
        if total_matches < 8:
                continue
        else:
            return True
    if total_matches < 8:
        print(f"Player {player} has less than 8 matching stats")
        return False     
    
# matches player stats to existing players ####################################          
def match_player_stats(table_name, stats_dict, all_players):
    current_table = stats_dict[table_name]
    for player, stats in current_table.items():
        if player in all_players:
            if stats_match_count(player, stats, all_players) == True:
                for key, values in stats.items():
                    if key not in all_players[player]["player_stats"]:
                        all_players[player]["player_stats"].update({key:values})                           

# convert the dictionary to a JSON string ####################################
def get_json_data(stats_dict,league):
    json_data = json.dumps(stats_dict, indent = 4, ensure_ascii=False) 
    # create text file for json data
    with open(f'{league} json.txt', 'w', encoding="utf-8") as file:
        file.write(json_data)
        
# creates urls for each stat type in a league ################################
def get_stat_urls(league_url):
    seasons = ("2019-2020", "2020-2021", "2021-2022", "2022-2023")
    # stat_type structure: {"name of page in league url" : "table in db"} 
    stat_type = {"stats" : "standard_stats", "keepers" : "goal_keeping_stats","keepersadv" : "adv_goal_keeping_stats",
                "shooting" : "shooting_stats","passing" : "passing_stats","passing_types" : "adv_passing_stats",
                "gca" : "goal_shot_creation_stats","defense" : "defensive_actions_stats","possession" : "possession_stats",
                "misc" : "miscellaneous_stats"}
    urls_list = {}
    for stat, table in stat_type.items():
        current_stat_type = league_url.replace("/stats/", f"/{stat}/")
        urls_list.update({current_stat_type:table})
        for season in seasons:
            current_season = current_stat_type.replace("Stats", f"{season}/stats/{season}-")
            urls_list.update({current_season:table})
    return urls_list

    # create tables  ###############################################################

# create base tables ##########################################################
def create_base_tables(cursor, id_datatype):
    player_table_sql = """
    CREATE TABLE IF NOT EXISTS players (
        player_id INT PRIMARY KEY,
        player VARCHAR(255),
        nationality VARCHAR(255),
        position VARCHAR(255),
        age INT,
        birth_year INT
    );"""
    try:
        cursor.execute(player_table_sql)
    except mysql.connector.Error as error:
        print(f"Failed to create player table. Error: {error}")
    league_table_sql = """
    CREATE TABLE IF NOT EXISTS leagues (
        league_id INT PRIMARY KEY,
        league VARCHAR(255)
    );"""
    try:
        cursor.execute(league_table_sql)
    except mysql.connector.Error as error:
        print(f"Failed to create league table. Error: {error}")
        
    season_table_sql = """
    CREATE TABLE IF NOT EXISTS seasons (
        season_id INT PRIMARY KEY,
        season VARCHAR(255)
    );"""
    try:
        cursor.execute(season_table_sql)
    except mysql.connector.Error as error:
        print(f"Failed to create season table. Error: {error}")
    
    team_table_sql = """
    CREATE TABLE IF NOT EXISTS teams (
        team_id INT PRIMARY KEY,
        team VARCHAR(255)
    );"""
    try:
        cursor.execute(team_table_sql)
    except mysql.connector.Error as error:
        print(f"Failed to create team table. Error: {error}")
        
    player_stats_table_sql = """
    CREATE TABLE IF NOT EXISTS player_stats (
        player_id INT,
        league_id INT,
        season_id INT,
        team_id INT,
        FOREIGN KEY (player_id) REFERENCES players(player_id),
        FOREIGN KEY (league_id) REFERENCES leagues(league_id),
        FOREIGN KEY (season_id) REFERENCES seasons(season_id),
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
    );"""
    try:
        cursor.execute(player_stats_table_sql)
    except mysql.connector.Error as error:
        print(f"Failed to create player_stats table. Error: {error}")
    alter_player_stats_sql = f"ALTER TABLE player_stats ADD ("
    length = len(id_datatype)
    count = 0 
    for stat, datatype in id_datatype.items():
        if stat == "player_id" or stat == "league_id" or stat == "season_id" or stat == "team_id":
            continue
        alter_player_stats_sql += f" {stat} {datatype}"
        count += 1
        if count < length - 4 :
            alter_player_stats_sql += ","
    alter_player_stats_sql += ");"
    try:
        cursor.execute(alter_player_stats_sql)
    except mysql.connector.Error as error:
        print(f"Failed to alter player_stats table. Error: {error}")

# upload data to mysql database ##############################################
def upload_data(all_stats, id_datatype, cursor):
    create_base_tables(cursor, id_datatype)
    
    # insert data into leagues table
    for league, stats in all_stats["leagues"].items():
        league_id = stats["league_id"]
        league_name = league
        try:
            cursor.execute("INSERT INTO leagues (league_id, league) VALUES (%s, %s)", (league_id, league_name))
            cnx.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert data for {league_name} in table leagues - Error: {error}")
    
    # insert data into seasons table           
    for season, stats in all_stats["seasons"].items():
        season_id = stats["season_id"]
        season_name = season
        try:
            cursor.execute("INSERT INTO seasons (season_id, season) VALUES (%s, %s)", (season_id, season_name))
            cnx.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert data for {season_name} in table seasons - Error: {error}")
    
    # insert data into teams table
    for team, stats in all_stats["teams"].items():
        team_id = stats["team_id"]
        team_name = team
        try:
            cursor.execute("INSERT INTO teams  (team_id, team) VALUES (%s, %s)", (team_id, team_name))
            cnx.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert data for {team_name} in table teams - Error: {error}")
    
    # insert data into players and player_stats table
    for player, stats in all_stats["players"].items():
        player_info = stats["player_info"]
        player_id = player_info["player_id"]
        player_name = player_info["player"]
        nationality = player_info["nationality"]
        position = player_info["position"]
        age = player_info["age"]
        birth_year = player_info["birth_year"]
        try:
            cursor.execute("""INSERT INTO players (player_id, player, nationality, position, age, birth_year) 
                            VALUES (%s, %s, %s, %s, %s, %s)""", (player_id, player_name, nationality, position, age, birth_year))
            cnx.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert data for {player_name} in table players - Error: {error}")

    for player, stats in all_stats["players"].items():
        player_stats = stats["player_stats"]
        length = len(player_stats)
        count = 0
        update_player_stats_sql = f"UPDATE player_stats SET "
        player_id = player_stats["player_id"]
        league_id = player_stats["league_id"]
        season_id = player_stats["season_id"]
        team_id = player_stats["team_id"]
        try:
            cursor.execute("""INSERT INTO player_stats (player_id, league_id, season_id, team_id) 
                            VALUES (%s, %s, %s, %s)""", (player_id, league_id, season_id, team_id))
            cnx.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert data for {player} in table player_stats - Error: {error}")
        # generate update sql for player stats
        for stat, value in player_stats.items():
            if stat == "player_id" or stat == "league_id" or stat == "season_id" or stat == "team_id":
                continue
            if stat in id_datatype:
                if value == "None":
                    value = 0
                
                if id_datatype[stat] == "VARCHAR(255)" and value != None:
                    #fixes sql error with Nonetype values
                    # fixes sql error with apostrophes
                    if "'" in value:
                        value = value.replace("'", "''")
                    pass
                    value = f"'{value}'"
                pass
            update_player_stats_sql += f"{stat} = {value}"
            # add comma if not last stat
            if count < length - 5:
                update_player_stats_sql += ", "
                count += 1
            else: 
                continue
        update_player_stats_sql += f" WHERE player_id = {player_id}"
        try:
            cursor.execute(update_player_stats_sql)
            cnx.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert data for {player} in table player_stats - Error: {error}")
    # removes columns from player_stats table > weird bug with the update sql, so removed columns
    cursor.execute("ALTER TABLE player_stats DROP COLUMN league;")
    cursor.execute("ALTER TABLE player_stats DROP COLUMN season;")
    cursor.execute("ALTER TABLE player_stats DROP COLUMN team;")
    cursor.execute("ALTER TABLE player_stats DROP COLUMN player;")
    cursor.execute("ALTER TABLE player_stats DROP COLUMN nationality;")
    cursor.execute("ALTER TABLE player_stats DROP COLUMN position;")

# finds stats table on fbref
def get_stats_table(soup):
    full_table = ""
    for x in soup.select("th"):
        x.decompose()

    # find the table with the player stats 
    for table in get_stats_table:
        table_caption = table.find("caption")
        table_name_text = table_caption.get_text()
        if "Player" in table_name_text:
            full_table = table_caption.parent
    return full_table     

def get_html_content(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            html_content = await response.text()
            html_content = response.text.replace("<!--", "").replace("-->", "")
            return html_content
        else:
            print(f"Failed - League: {url}")
            print(response.reason)
            return None

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# gets player stats from fbref and inserts into mysql database ###############
def get_data(league_urls):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    id_datatype = {"league_id": "INT", "season_id": "INT", "player_id": "INT", "league": "VARCHAR(255)", "season": "VARCHAR(255)","team" : "VARCHAR(255)"}
    league_dict = {}
    team_dict = {}
    season_dict = {}
    all_players = {} 
    league_id = 0
    player_id = 0
    team_id = 0
    season_id = 0
    for url in league_urls:
        stats_dict = {}
        all_urls = []
        url_list = get_stat_urls(url)
        all_urls.extend(url_list.keys())
    html_contents = asyncio.run(fetch_all(all_urls))
    # You'd then parse these HTML contents as needed, similar to your original loop
    for html in html_contents:
        stat_type = {"stats" : "standard_stats", "keepers" : "goal_keeping_stats","keepersadv" : "adv_goal_keeping_stats",
            "shooting" : "shooting_stats","passing" : "passing_stats","passing_types" : "adv_passing_stats",
            "gca" : "goal_shot_creation_stats","defense" : "defensive_actions_stats","possession" : "possession_stats",
            "misc" : "miscellaneous_stats"}        
        for stat_name in stat_type:
            if stat_name in html:
                table_name = stat_type[stat_name]
                stats_dict.update({table_name:{}})
                pass
        if html:     
            soup = BeautifulSoup(html, "html5lib")
        #finds league and season
        league, season, = get_caption(soup)
        league_and_season = f"{league} - {season}"
        #update league and season id and add to dictionary
        if league not in league_dict:
            league_id += 1
            league_dict.update({league :{"league_id": league_id}})
        else:
            league_id = league_dict[league]["league_id"]
        if season not in season_dict:
            season_id += 1
            season_dict.update({season:{"season_id":season_id}})
        else:
            season_id = season_dict[season]["season_id"]
        # finds stats table on fbref
        full_table = get_stats_table(soup)               
        # finds the data-stat ids and create key/value pair for player stats
        stats_table = full_table.find_all("tr")
        for rows in stats_table:
            stat_column = rows.find_all("td")
            for stat in stat_column:
                if stat is not None:
                    stat_tag = stat["data-stat"]
                    # get text from each stat
                    player_stat = stat.get_text()
                    # convert text to int or float
                    player_stat = float_zero_int(player_stat)
                    # convert age to years
                    if stat_tag == "age":
                        player_stat = age_format(player_stat)
                    # convert position code to position name    
                    if stat_tag == "position":
                        player_stat = get_position(player_stat)
                    # convert country code to country name
                    if stat_tag == "nationality":
                        player_stat = get_country_name(player_stat)
                    # update team id
                    if stat_tag == "team":
                        if player_stat not in team_dict:
                            team_id += 1
                            team_dict.update({player_stat:{"team_id": team_id}})
                            pass
                    # skip matches stat
                    if stat_tag == "matches":
                        continue
                    # declare current player    
                    if stat_tag == "player":
                        current_player = player_stat
                        stats_dict[table_name].update({current_player:{}})
                        # update player id
                        player_id += 1
                        stats_dict[table_name][current_player].update({"player_id":player_id})
                        # update league and season id for current player
                        stats_dict[table_name][current_player].update({"league_id":league_id, "season_id":season_id})
                    if stat_tag == "team":
                            if player_stat in team_dict:
                                # update team id for current player
                                current_team_id = team_dict[player_stat]["team_id"]
                                stats_dict[table_name][current_player].update({"team_id":current_team_id})
                                pass
                    stats_dict[table_name][current_player].update({stat_tag:player_stat})
        # get all players creates a dictionary of all players and their stats        
        if table_name == "standard_stats":
            get_all_players(stats_dict, all_players)
        else:
        # match player stats - matches player stats to existing players in all players dictionary
            match_player_stats(table_name, stats_dict, all_players)
                 
    all_stats = {"players": all_players, "leagues": league_dict, "seasons": season_dict, "teams": team_dict}
    get_datatype(all_stats, id_datatype)
    # creeate json file for all stats for each all players
    get_json_data(all_stats, "Top 5 Leagues")
    #upload data to mysql database
    upload_data(all_stats, id_datatype, cursor)

# input urls for each league #################################################
league_urls = [
        "https://fbref.com/en/comps/9/stats/Premier-League-Stats",
      #  "https://fbref.com/en/comps/12/stats/La-Liga-Stats",
      # "https://fbref.com/en/comps/11/stats/Serie-A-Stats",
       # "https://fbref.com/en/comps/20/stats/Bundesliga-Stats",
       # "https://fbref.com/en/comps/13/stats/Ligue-1-Stats"   
    ]
get_data(league_urls)

# close mysql database connection ###########################################
cursor.close()
cnx.close()