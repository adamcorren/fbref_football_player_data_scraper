from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
import time
import re
from functools import reduce
import sys
from urllib.error import HTTPError

'''
This program will get summary player data for each game played in the top 5 
European football leagues from the website fbref.com
'''

def get_data_info():
    # all possible leagues and seasons
    leagues = ['Premier League', 'La Liga', 'Serie A', 'Ligue 1', 'Bundesliga']
    seasons = ['2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
    
    while True:
        # select league [Premier League / La Liga / Serie A / Ligue 1 / Bundesliga]
        league = input('Select League (Premier League / La Liga / Serie A / Ligue 1 / Bundesliga): ')
        
        # check if input valid
        if league not in leagues:
            print('League not valid, try again')
            continue
            
        # assign url names and id's
        if league == 'Premier League':
            league = 'Premier-League'
            league_id = '9'

        if league == 'La Liga':
            league = 'La-Liga'
            league_id = '12'

        if league == 'Serie A':
            league = 'Serie-A'
            league_id = '11'

        if league == 'Ligue 1':
            league = 'Ligue-1'
            league_id = '13'

        if league == 'Bundesliga':
            league = 'Bundesliga'
            league_id = '20'
        break
            
    while True: 
        # select season after 2017 as XG only available from 2017,
        season = input('Select Season (2017-2018, 2018-2019, 2019-2020, 2020-2021, 2021-2022): ')
        
        # check if input valid
        if season not in seasons:
            print('Season not valid, try again')
            continue
        break

    url = f'https://fbref.com/en/comps/{league_id}/{season}/schedule/{season}-{league}-Scores-and-Fixtures'
    return url, league, season


def get_fixture_data(url, league, season):
    print('Getting fixture data...')
    # create empty data frame and access all tables in url
    fixturedata = pd.DataFrame([])
    tables = pd.read_html(url)
    
    # get fixtures
    fixtures = tables[0][['Wk', 'Day', 'Date', 'Time', 'Home', 'Away', 'xG', 'xG.1', 'Score']].dropna()
    fixtures['season'] = url.split('/')[6]
    fixturedata = pd.concat([fixturedata,fixtures])
    
    # assign id for each game
    fixturedata["game_id"] = fixturedata.index
    
    # export to csv file
    fixturedata.reset_index(drop=True).to_csv(f'{league.lower()}_{season.lower()}_fixture_data.csv', 
        header=True, index=False, mode='w')
    print('Fixture data collected...')


def get_match_links(url, league):   
    print('Getting player data...')
    # access and download content from url containing all fixture links    
    match_links = []
    html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    links = soup(html.content, "html.parser").find_all('a')
    
    # filter list to return only needed links
    key_words_good = ['/en/matches/', f'{league}']
    for l in links:
        href = l.get('href', '')
        if all(x in href for x in key_words_good):
            if 'https://fbref.com' + href not in match_links:                 
                match_links.append('https://fbref.com' + href)
    return match_links


def player_data(match_links, league, season):
    # loop through all fixtures
    player_data = pd.DataFrame([])
    for count, link in enumerate(match_links):
        try:
            tables = pd.read_html(link)
            for table in tables:
                try:
                    table.columns = table.columns.droplevel()
                except Exception:
                    continue

            # get player data
            def get_team_1_player_data():
                # outfield and goal keeper data stored in seperate tables 
                data_frames = [tables[3], tables[9]]
                
                # merge outfield and goal keeper data
                df = reduce(lambda left, right: pd.merge(left, right, 
                    on=['Player', 'Nation', 'Age', 'Min'], how='outer'), data_frames).iloc[:-1]
                
                # assign a home or away value
                return df.assign(home=1, game_id=count)

            # get second teams  player data        
            def get_team_2_player_data():
                data_frames = [tables[10], tables[16]]
                df = reduce(lambda left, right: pd.merge(left, right,
                    on=['Player', 'Nation', 'Age', 'Min'], how='outer'), data_frames).iloc[:-1]
                return df.assign(home=0, game_id=count)

            # combine both team data and export all match data to csv
            t1 = get_team_1_player_data()
            t2 = get_team_2_player_data()
            player_data = pd.concat([player_data, pd.concat([t1,t2]).reset_index()])
            
            print(f'{count+1}/{len(match_links)} matches collected')
            player_data.to_csv(f'{league.lower()}_{season.lower()}_player_data.csv', 
                header=True, index=False, mode='w')
        except:
            print(f'{link}: error')
        # sleep for 3 seconds after every game to avoid IP being blocked
        time.sleep(3)


# main function
def main(): 
    url, league, season = get_data_info()
    get_fixture_data(url, league, season)
    match_links = get_match_links(url, league)
    player_data(match_links, league, season)

    # checks if user wants to collect more data
    print('Data collected!')
    while True:
        answer = input('Do you want to collect more data? (yes/no): ')
        if answer == 'yes':
            main()
        if answer == 'no':
            sys.exit()
        else:
            print('Answer not valid')
            continue


if __name__ == '__main__':
    try:
        main()
    except HTTPError:
        print('The website refused access, try again later')
        time.sleep(5)


