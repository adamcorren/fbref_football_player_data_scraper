# FBREF Football Player Data Scraper

This Python program scrapes player data from the football data website fbref.com.

This programme can collect data from the following leagues and seasons:
- English Premier League, 2017-18 - 2022-23
- Spanish La Liga, 2017-18 - 2022-23
- Italian Serie A, 2017-18 - 2022-23
- French Ligue 1, 2017-18 - 2022-23
- German Bundesliga, 2017-18 - 2022-23

The programme will produce two csv files, one for fixture data, one for player data

The fixture data csv file contains the following information for each game played in a given league and season:

- Game week
- Week day
- Date
- Time
- Home and away teams
- Score
- XG score
- Season
- Game id

The player data csv file contains the following information for every player that plays in each game played in a given leauge/season:

ALL PLAYERS

- Name
- Shirt number
- Nationality
- Position played
- Age
- Minutes played
- Goals scored
- Assists
- Penalty kicks attempted and scored
- Total shots and shots on target
- Yellow and red cards
- Total touches
- Total tackles
- Total interceptions
- Total blocks
- Expected goals scored (XG)
- Expected goals scored without penalty kicks
- Expected assists
- Total passes attempted, completed
- Progressive passes
- Total carries and progressive carries
- Total attacks and successful attacks

ONLY GOAL KEEPERS

- Total shots saved
- Save percentage
- Post shot expected goals conceded
- Total passes attempted
- Average legnth of pass
- Total goal kicks
- Average length of goal kicks
- Tota crosses faced and stopped
- Total defensive actions outside the penalty box
  
## Prerequisite Software

- [Python 3](https://www.python.org/) (make sure to add Python to PATH/environment variables when installing)
- [pandas 2.0.1](https://pandas.pydata.org/)
- [requests 2.30.0 or newer](https://github.com/psf/requests/releases)

### Windows installation

You can install the prerequisites double-clicking `install_prerequesites.bat` after installing Python 3.

## Program Installation

This programme can either be installed by downloading the repository from
[the GitHub page](https://github.com/adamcorren/fbref_football_player_data_scraper) or by running the following command if git
is installed on your machine:
```commandline
git clone https://github.com/adamcorren/fbref_football_player_data_scraper
```

## Usage
     
Follow the instructions for your operating system below.

### Windows

Once you've installed the [requirements], double click `start_windows.bat`. That's it.

### Using the program

The program will ask which league and season you'd like to get data for. I recommend not collecting mutiple seasons/leagues of data at once as the website may block access if you try to access it too many times in a short period of time. The program will then guide you through the rest of the process.

## To-Dos

There are a few more things I want to do with this project. The current to-do list is below, but if you think of
anything you'd like added, please let me know!

- [ ] Support more leagues
- [ ] Support seasons before XG data available (pre 2017)


## License

Licensed under [MIT]((https://opensource.org/license/mit/)).

The data provided is property of https://fbref.com
I don't own any of the data
