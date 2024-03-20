import requests
from bs4 import BeautifulSoup
import mysql.connector
import json

                         
# finds datatype for each stat ################################################
def get_datatype(player_stat, stat_tag, id_datatype):
    if stat_tag not in id_datatype:
        try:
            player_stat = int(player_stat)
            id_datatype.update({stat_tag: "INT"})
        except ValueError:
            try:
                player_stat = float(player_stat)
                id_datatype.update({stat_tag: "FLOAT"})
            except ValueError:
                id_datatype.update({stat_tag: "VARCHAR(255)"})

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
def get_player_ids(current_player, table_name, stats_dict):
    if current_player in stats_dict:
        total_matches = 0
        for key in stats_dict[current_player]["standard_stats"]:
            if key in stats_dict[current_player][table_name]:
                if stats_dict[current_player]["standard_stats"][key] == stats_dict[current_player][table_name][key]:
                        total_matches += 1
                        if total_matches >= 5:
                            player_id = stats_dict[current_player]["standard_stats"]["player_id"]
                            return player_id

# creates player table ########################################################                    


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

# gets player stats from fbref and inserts into mysql database ###############
def get_data(league_urls):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    all_data = {"players":{}, "leagues":{}, "teams":{}, "seasons":{}}
    player_list = []
    league_list = []
    team_list = []
    id_datatype = {}
    player_id = 0
    league_id = 0
    team_id = 0
    season_id = 1
    for url in league_urls:
        league_id += 1 
        url_list = get_stat_urls(url)
        stats_dict = {}
        league_dict = {}
        team_dict = {}
        for url, table_name in url_list.items():
            response = requests.get(url,headers=headers)
            if response.ok:
                # .replace() removes player data comment out to see player data
                html_content = response.text.replace("<!--", "").replace("-->", "")
                soup = BeautifulSoup(html_content, "html5lib")
                league, season = get_caption(soup)
                league_and_season = f"{league} - {season}"
                if league not in league_dict:
                    league_dict.update({"league_id": league_id, "league": league})
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
                table_dict = {table_name:{}}
                stat_column = rows.find_all("td")
                for stat in stat_column:
                    table_dict = {table_name:{}}
                    if stat is not None:
                        stat_tag = stat["data-stat"]
                        player_stat = stat.get_text()
                        if stat_tag == "player":
                            current_player = player_stat
                            pass
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
                                team_dict.update({"team_id": team_id, "team": player_stat})
                        if stat_tag == "matches" or stat_tag == "ranker":
                                pass
                        else:
                            if stat_tag == "player":
                                current_player = player_stat
                                if current_player not in stats_dict:
                                    player_id += 1
                                    stats_dict.update({current_player:{"player_id":player_id}})
                                    stats_dict[current_player].update({"league":league})
                                    stats_dict[current_player].update({"season":season})
                                elif stat_tag not in stats_dict[current_player]:
                                    stats_dict[current_player].update({stat_tag:player_stat})
                                get_datatype(player_stat, stat_tag, id_datatype)
                           # if table_name != "standard_stats":
                           #     matched_player_id = get_player_ids(current_player, table_name, stats_dict)
                            #    stats_dict[current_player][table_name].update({"player_id":matched_player_id})
                            #if stat_tag not in stats_dict[current_player]:
        # creates json file for each league       
        get_json_data(stats_dict,league)
                             
# input urls for each league #################################################
league_urls = [
        "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
        #"https://fbref.com/en/comps/12/stats/La-Liga-Stats",
       # "https://fbref.com/en/comps/11/stats/Serie-A-Stats",
      # "https://fbref.com/en/comps/20/stats/Bundesliga-Stats",
       # "https://fbref.com/en/comps/13/stats/Ligue-1-Stats"   
    ]
get_data(league_urls)
