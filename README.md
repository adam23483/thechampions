# The Champions Project
#### Note:
- This project is free-flowing and my end goals might change over time. 
- Working on this between school and work so updates will be infrequent 


## Overview
TheChampions is a project focused on collecting data on soccer players, storing it in a MySQL database, creating a Rest API hosted on AWS, and developing a frontend for data analysis. Additionally, the project aims to integrate a Generative AI (Gen AI) to provide insights based on the collected dataset.

## Goals
- Collecting data on soccer players
  - Web scraping with Python scrape brief for player data 
  - names, country, positions, league, xg(expected goals), etc...
  - automate the web scraping, ie every day update stats
  - 
- Creating a database to store the data
  -  MySQL database
  -  Create Rest API: to be hosted on AWS
    
- Fronted to Display/Filter data for easy analysis
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
  - Now creating a schema for DB (should have done that before uploading data)
  - Next:
    - automate updating the DB every day or 12 hours 
    - finetune GPT with dataset
    - create a chatbot page with web hosting
  

