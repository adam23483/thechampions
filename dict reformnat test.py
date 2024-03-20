import requests
from bs4 import BeautifulSoup
import mysql.connector
import json

# mysql database connection ###################################################
cnx = mysql.connector.connect(
host="localhost",
user="root",
password="6597916n",
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
      "ci": "Côte d'Ivoire",
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
def get_all_players(stats_dict, all_players, table_name):
    info = ["player","team", "position", "age", "birth_year","nationality", "player_name"]
    for table_name, current_player in stats_dict.items():
        if table_name == "standard_stats" and current_player not in all_players:    
            all_players.update({current_player:{"player_id":{}}})
            all_players[current_player].update({"player_info":{}})
            all_players[current_player].update({"player_stats":{}})

            for key in stats_dict["standard_stats"][current_player]:
                if key in info:
                    all_players[current_player]["player_info"].update({key:stats_dict["standard_stats"][current_player][key]})
                else:
                    all_players[current_player]["player_stats"].update({key:stats_dict["standard_stats"][current_player][key]})
        else:
            total_matches = 0
            if current_player in all_players:
                for key in all_players[current_player]["player_stats"]: 
                    if key in stats_dict[table_name][current_player]:
                        if all_players[current_player]["player_stats"][key] == stats_dict[table_name][current_player][key]:
                                total_matches += 1
                                if total_matches >= 5:
                                    for key in stats_dict[table_name][current_player]:
                                        if key not in all_players[current_player]["player_stats"]:
                                            all_players[current_player]["player_stats"].update({key:stats_dict[table_name][current_player][key]})

# creates player table ########################################################                    
def get_player_table(stats_dict):
    player_info = {"player_info":{}}
    info = ["player_id", "player","team", "position", "age", "birth_year","nationality"]
    standard_stats = stats_dict["standard_stats"]
    for player, stats in standard_stats.items():
        player_info["player_info"].update({player:{}})
        for key in stats:
            if key in info:
                player_info["player_info"][player].update({key:stats[key]})
    return player_info

# convert the dictionary to a JSON string ####################################
def get_json_data(stats_dict,league):
    json_data = json.dumps(stats_dict, indent = 4, ensure_ascii=False) 
    # create text file for json data
    with open(f'{league} json.txt', 'w', encoding="utf-8") as file:
        file.write(json_data)
        
# creates urls for each stat type in a league ################################
def get_stat_urls(league_url):
    # stat_type structure: {"name of page in league url" : "table in db"} 
    stat_type = {"stats" : "standard_stats", "keepers" : "goal_keeping_stats","keepersadv" : "adv_goal_keeping_stats",
                "shooting" : "shooting_stats","passing" : "passing_stats","passing_types" : "adv_passing_stats",
                "gca" : "goal_shot_creation_stats","defense" : "defensive_actions_stats","possession" : "possession_stats",
                "misc" : "miscellaneous_stats"}
    urls_list = {}
    for stat, table in stat_type.items():
        current_stat_type = league_url.replace("/stats/", f"/{stat}/")
        urls_list.update({current_stat_type:table})
    return urls_list

    # create tables  ###############################################################

# removes keys from dictionary ################################################
def remove_keys(all_players, keys_to_remove):
    for player in all_players:
        current_player_stats = all_players[player]["player_stats"]
        for key in list(current_player_stats.keys()):
            if key in keys_to_remove:
                del current_player_stats[key]
            else:
                continue

# reformat stats_dict ######################################################### 
def reformat_stats(stats_dict, league_dict, season_dict, team_dict):
    all_players = {}
    info = ["player","team", "position", "age", "birth_year","nationality", "player_name"]
    for player, stats in stats_dict["player_info"].items():
        if player not in all_players:
            all_players.update({player:{}})
            if stats["player_id"] not in all_players[player]:
                all_players[player].update({"player_id": stats["player_id"]})
                all_players[player].update({"player_info":{}})
                all_players[player].update({"player_stats":{}})
    
    for table, players in stats_dict.items():        
        for player, stats in players.items():
            if player in all_players and stats["player_id"] == all_players[player]["player_id"]:
                all_players[player].update({"player_info":stats})
                all_players[player]["player_info"].update({"player_name":player})
                for key in stats:
                    if key not in all_players[player]["player_stats"] and key not in info:
                        all_players[player]["player_stats"].update({key:stats[key]})
                all_players[player]["player_stats"].update()
    remove_keys(all_players, info)                    
    all_stats = {"players": all_players, "leagues": league_dict, "seasons": season_dict, "teams": team_dict}      
    get_json_data( all_stats, "all_stats")
    return all_stats

# create base tables ##########################################################
def create_base_tables(cursor):
    player_table_sql = """
    CREATE TABLE IF NOT EXISTS players (
        player_id INT PRIMARY KEY,
        player_name VARCHAR(255),
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

# upload data to mysql database ##############################################
def upload_data(all_stats, id_datatype, cursor):
    create_base_tables(cursor)
    for league, stats in all_stats["leagues"].items():
        league_id = stats["league_id"]
        league_name = league
        try:
            cursor.execute("INSERT INTO leagues (league_id, league) VALUES (%s, %s)", (league_id, league_name))
            cnx.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert data for {league_name} in table leagues - Error: {error}")
               
    for season, stats in all_stats["seasons"].items():
        season_id = stats["season_id"]
        season_name = season
        try:
            cursor.execute("INSERT INTO seasons (season_id, season) VALUES (%s, %s)", (season_id, season_name))
            cnx.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert data for {season_name} in table seasons - Error: {error}")
    
    for team, stats in all_stats["teams"].items():
        team_id = stats["team_id"]
        team_name = team
        try:
            cursor.execute("INSERT INTO teams  (team_id, team) VALUES (%s, %s)", (team_id, team_name))
            cnx.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert data for {team_name} in table teams - Error: {error}")
            
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
    
    for player, stats in all_stats["players"].items():
        player_info = stats["player_info"]
        player_id = player_info["player_id"]
        player_name = player_info["player_name"]
        nationality = player_info["nationality"]
        position = player_info["position"]
        age = player_info["age"]
        birth_year = player_info["birth_year"]
        try:
            cursor.execute("""INSERT INTO players (player_id, player_name, nationality, position, age, birth_year) 
                            VALUES (%s, %s, %s, %s, %s, %s)""", (player_id, player_name, nationality, position, age, birth_year))
            cnx.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert data for {player_name} in table players - Error: {error}")

    for player, stats in all_stats["players"].items():
        player_stats = stats["player_stats"]
        length = len(player_stats)
        count = 0
        update_player_stats_sql = f"UPDATE player_stats SET "
        for stat, value in player_stats.items():
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
            if stat == "player_id" or stat == "league_id" or stat == "season_id" or stat == "team_id":
                continue
            update_player_stats_sql += f"{stat} = {value}"
            count += 1
            if count < length - 4 :
                update_player_stats_sql += ", "
        update_player_stats_sql += f" WHERE player_id = {player_id}"
        try:
            cursor.execute(update_player_stats_sql)
            cnx.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert data for {player} in table player_stats - Error: {error}")
            
    update_player_stats_sql = f"UPDATE player_stats SET"
    length = len(id_datatype)
    count = 0 
    update_player_stats_sql += f"WHERE player_id = {player_id}"

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
        url_list = get_stat_urls(url)
        for url, table_name in url_list.items():
            stats_dict.update({table_name:{}})
            response = requests.get(url,headers=headers)
            if response.ok:
                # .replace() removes player data comment out to see player data
                html_content = response.text.replace("<!--", "").replace("-->", "")
                soup = BeautifulSoup(html_content, "html5lib")
                league, season, = get_caption(soup)
                league_and_season = f"{league} - {season}"
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
            else:
                print(f"Failed - League: {url}")
                print(response.reason)

            # finds stats table on fbref
            get_stats_table = soup.find_all("table")
            full_table = ""
            for x in soup.select("th"):
                x.decompose()

            # find the table with the player stats 
            for table in get_stats_table:
                table_caption = table.find("caption")
                table_name_text = table_caption.get_text()
                if "Player" in table_name_text:
                    full_table = table_caption.parent
                            
            # finds the data-stat ids and create key/value pair for player stats
            stats_table = full_table.find_all("tr")
            for rows in stats_table:
                stat_column = rows.find_all("td")
                for stat in stat_column:
                    if stat is not None:
                        stat_tag = stat["data-stat"]
                        player_stat = stat.get_text()
                        player_stat = float_zero_int(player_stat)
                        if stat_tag == "age":
                            player_stat = age_format(player_stat)
                        if stat_tag == "position":
                            player_stat = get_position(player_stat)
                        if stat_tag == "nationality":
                            player_stat = get_country_name(player_stat)
                        if stat_tag == "team":
                            if player_stat not in team_dict:
                                team_id += 1
                                team_dict.update({player_stat:{"team_id": team_id}})
                        if stat_tag == "matches" or stat_tag == "ranker":
                            pass
                        else:
                            if stat_tag == "player":
                                current_player = player_stat
                                stats_dict[table_name].update({current_player:{}})
                                player_id += 1
                                stats_dict[table_name][current_player].update({"player_id":player_id})
                                stats_dict[table_name][current_player].update({"league_id":league_id, "season_id":season_id})
                            else:
                                if stat_tag == "team":
                                    if player_stat in team_dict:
                                        current_team_id = team_dict[player_stat]["team_id"]
                                        stats_dict[table_name][current_player].update({"team_id":current_team_id})
                                stats_dict[table_name][current_player].update({stat_tag:player_stat})
    get_all_players(stats_dict, all_players, table_name)
    get_json_data(all_players, "reformat_test")
            
# input urls for each league #################################################
league_urls = [
        "https://fbref.com/en/comps/9/stats/Premier-League-Stats",
        #"https://fbref.com/en/comps/12/stats/La-Liga-Stats",
        #"https://fbref.com/en/comps/11/stats/Serie-A-Stats",
        #"https://fbref.com/en/comps/20/stats/Bundesliga-Stats",
        #"https://fbref.com/en/comps/13/stats/Ligue-1-Stats"   
    ]
get_data(league_urls)




