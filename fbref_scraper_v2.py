import requests
from bs4 import BeautifulSoup
import array as arr
import json
import pandas as pd

url = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
response = requests.get(url)

if response.ok:
# .replace() removes player data comment out   
  html_content = response.text.replace('<!--', '').replace('-->', '')
  soup = BeautifulSoup(html_content, 'lxml')
# Error trapping site response
  print("Retrieved HTML content.   "
        )
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
"npxg_xg_assist_per90",

]
#player_stats dict creation
player_stats = {}

# finds standard stats table on fbref
full_table = soup.find(id= 'stats_standard')
stat_table = full_table.find('tbody').select("tr", class_="data-row=")

# removes standard stats: header, mid row headers, and match colomn
def decompose_items():
  for x in soup.select('tr.thead'):
    x.decompose()
  for x in full_table.find_all("tr"):
    x.th.decompose()
  for x in full_table.find("tbody").find_all('td',string='Matches'):
    x.decompose()
decompose_items()

def get_country_name(country_code):
    # Mapping of country codes to country names
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
    }

    # Get the country name from the mapping using the provided country code
    country_name = country_mapping.get(country_code.lower())
    
    if country_name:
        return country_name
    else:
        return "Unknown Country:" + country_code

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
    print(name_text)
    yield all_stats

# finds and adds stats to player_stats dict
def get_stats():
  for stat_group in get_player_parents():
    for stat_id in data_stats_ids:
      selected_id = 'td[data-stat="' + stat_id + '"]'     
      stat = stat_group.select_one(selected_id)
      stat_text = stat.get_text() if stat else print("None")
      
      if stat_id == "player":
        this_player = stat_text
        # update() adds player to player_stats dict
        player_stats.update({this_player:{}})
      if stat_id == "nationality":
        stat_text = stat_text[0:2]
        stat_text = get_country_name(stat_text)
      
# update() adds stats to player name in dict
      player_stats[this_player].update({stat_id:stat_text})

# runs stat_search() function 
get_stats()

# prints dict in readable format
print(json.dumps(player_stats, indent = 4, ensure_ascii=False))
