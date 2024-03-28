# The Champions Project
## PowerBI Dashboard
### [Link to Dashboard](https://app.powerbi.com/groups/me/reports/e4ebd868-41d8-4360-868b-0653656930b7/ReportSection?experience=power-bi)
![image](https://github.com/adam23483/thechampions/assets/63423355/778082ff-388b-454d-9c1d-0273d7f8cfa6)
## Overview
TheChampions is a project focused on collecting data on soccer players, storing it in an SQL database hosted on AWS, and developing a dashboard for data analysis. Additionally, the project aims to integrate a Generative AI (Gen AI) to provide insights based on the dataset.

## Goals
- Collecting data on soccer players
  - Web scraping with Python scrape brief for player data 
  - names, country, positions, league, xg(expected goals), etc...
  - automate the web scraping, ie every day update stats
  - 
- Creating a database to store the data
  -  MySQL database - *currently stored locally but will move to AWS*
  
- Fronted to Display/Filter data for easy analysis
  - Power BI dashboard
    - graphs, tables, in-form players

- Gen AI integration
  - Using dataset to train/fine-tune GPT or similar models for queries
    - Ex - What wingers create a lot of goals aka (shots created per 90 ) and are good at defending(interception/tackles per 90)?
     - Returns - Currently "Bukayo Saka" is the best of both worlds: Here are some other players that fit your request: player, player. player
  
## Progress Updates 
### 11/08/2023
- Began using Github
- Uploaded all work from local to git 
  - Ogrinal script
  - V2 of script
  - MySQL database stat file 

### 12/29/2023
- Python script is working
  - Takes scraped data from the Standard Stats page for any league on Fbref
  - the next goal is to automate collection from the site into MySQL database organizing by league
### 01/11/2024
- Python to MYSQL database is working
  - Solved issues with text, float, and int formatting
  - Now creating a schema for DB
  - Next:
    - automate updating the DB every day or 12 hours 
    - finetune GPT with dataset
    - create a chatbot page with web hosting
### 02/02/2024
- Python to MYSQL database is working 
  - Data from:
    - Premier League = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
    - La Liga - 'https://fbref.com/en/comps/12/stats/La-Liga-Stats'
    - Serie A -'https://fbref.com/en/comps/11/stats/Serie-A-Stats'
    - Bundesliga - 'https://fbref.com/en/comps/20/stats/Bundesliga-Stats'
    - Ligue 1 - 'https://fbref.com/en/comps/13/stats/Ligue-1-Stats'
  - Schema for DB, (FK, PK setup as well)
  - added Excel export from the MySQL database
  - Next: 
    - add previous seasons 
    - create PowerBI dashboard  
    - finetune GPT with dataset
    - create chatbot that can integrate with the dashboard based on training data
    - automate updating the DB every day or 12 hours ***on hold until all other tasks are done***
### 03/19/2024
- Reworking Python to MYSQL database script   
  - Needed more data for player performance 9 more pages per league 
    - New script dynamically scrapes data from each page. 
    - creates json for easy reading and bug fixing  
  - Adding data from Transfermarkt  
    - new data - transfer values, salaries, contract info, player physical stats
  - Power PI dashboard  
    - Created Power PI dashboard
      - reworking after all data is ready for 2023/2024 database
  - Next: 
    - finetune GPT with dataset 
    - create a chatbot that can integrate with the dashboard based on training data for prompts 
    - automate updating the DB every day or 12 hours ***on hold until all other tasks are done***
