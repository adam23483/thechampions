###################################################################################
def league_table(cursor, cnx, player_stats):
    cursor.execute("DROP TABLE IF EXISTS league")
    cnx.commit()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS league (
            league_id INT AUTO_INCREMENT PRIMARY KEY,
            league_name VARCHAR(255)
        );
    """)
    cnx.commit()
    
    for stats in player_stats:
        league = stats.get('league', '')
        cursor.execute("INSERT INTO league (league_name) VALUES (%s)", (league,))
    cnx.commit()

###################################################################################
def team_table(cursor, cnx, player_stats):
    cursor.execute("DROP TABLE IF EXISTS team")
    cnx.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team (
            team_id INT AUTO_INCREMENT PRIMARY KEY,
            team_name VARCHAR(255),
            league_id INT,
            FOREIGN KEY (league_id) REFERENCES league(league_id)
        );
    """)
    cnx.commit()

    for stats in player_stats:
        team = stats.get('team', '')
        league = stats.get('league', '')
        cursor.execute("SELECT league_id FROM league WHERE league_name = %s", (league))
        league_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO team (team_name, league_id) VALUES (%s, %s)", (team, league_id))
    cnx.commit()

###################################################################################
def player_table(cursor, cnx, player_stats):
    cursor.execute("DROP TABLE IF EXISTS player")
    cnx.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player (
            player_id INT AUTO_INCREMENT PRIMARY KEY,
            team_id INT,
            player_name VARCHAR(255),
            position VARCHAR(255),
            nationality VARCHAR(255),
            age INT,
            birth_year INT,
            FOREIGN KEY (team_id) REFERENCES team(team_id)
        );
    """)
    cnx.commit()

    for player, stats in player_stats.items():
        player_name = stats.get('player', '')
        position = stats.get('position', '')
        team = stats.get('team', '')
        nationality = stats.get('nationality', '')
        age = stats.get('age', '')
        birth_year = stats.get('birth_year', '')
        cursor.execute("SELECT team_id FROM team WHERE team_name = %s", (team,))
        team_id = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO player (player_name, position, nationality, age, birth_year, team_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (player_name, position, nationality, age, birth_year, team_id))
    cnx.commit()
###################################################################################
def current_stats(cursor, cnx, player_stats):
    cursor.execute("DROP TABLE IF EXISTS current_stats")
    cnx.commit()

    cursor.execute("""
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
            FOREIGN KEY (player_id) REFERENCES player(player_id)
        );
    """)
    cnx.commit()

    for player, stats in player_stats.items():
                
        cursor.execute("SELECT player_id FROM player WHERE player_name = %s", (player,))
        player_id = cursor.fetchone()[0]
        games = stats.get('games', 0), 
        games_starts = stats.get('games_starts', 0)
        minutes = stats.get('minutes', 0)
        minutes_90s = stats.get('minutes_90s', 0.0)
        goals = stats.get('goals', 0)
        assists = stats.get('assists', 0)
        goals_assists = stats.get('goals_assists', 0)
        goals_pens = stats.get('goals_pens', 0)
        pens_made = stats.get('pens_made', 0)
        pens_att = stats.get('pens_att', 0)
        cards_yellow = stats.get('cards_yellow', 0)
        cards_red = stats.get('cards_red', 0)
        progressive_carries = stats.get('progressive_carries', 0)
        progressive_passes = stats.get('progressive_passes', 0)
        progressive_passes_received = stats.get('progressive_passes_received', 0)   

        insert_stats_query = """
            INSERT INTO current_stats 
                (player_id, games, games_starts, minutes, minutes_90s, goals, 
                assists, goals_assists, goals_pens, pens_made, pens_att, cards_yellow, 
                cards_red, progressive_carries, progressive_passes, progressive_passes_received)
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_stats_query, (
            player_id, games, games_starts, minutes, minutes_90s, goals, 
            assists, goals_assists, goals_pens, pens_made, pens_att, cards_yellow, 
            cards_red, progressive_carries, progressive_passes, progressive_passes_received
        ))
        cnx.commit()

###################################################################################
league_table(cursor, cnx, player_stats)
team_table(cursor, cnx, player_stats)
player_table(cursor, cnx, player_stats)
current_stats(cursor, cnx, player_stats)
expected_stats(cursor, cnx, player_stats)

# Close the cursor and connection
cursor.close()
cnx.close()