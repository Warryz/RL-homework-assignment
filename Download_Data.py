# import requests
import json
import sqlite3
from time import sleep

import requests

from functions import get_player_name_and_id, get_player_stats, get_team_stats

# Create a list for the players
players = list()

# List of all ingame ranks
ranks = [['unranked', 'unranked'],
         ['bronze-1', 'bronze-3'],
         ['silver-1', 'silver-3'],
         ['gold-1', 'gold-3'],
         ['platinum-1', 'platinum-3'],
         ['diamond-1', 'diamond-3'],
         ['champion-1', 'champion-3'],
         ['grand-champion', 'grand-champion']]

# List of all interesting game mods
game_modes = ['ranked-duels', 'ranked-doubles', 'ranked-standard']

# List for replay data
replay_data = list()

# API URL for making requests
api_url = 'https://ballchasing.com/api/'
# Authorization Header
# ADD the API key here!
header = {'Authorization': 'abc123'}

# Create a database connection and a cursor for executing commands.
conn = sqlite3.connect('rl.db')
c = conn.cursor()

# Make the first request.
r = requests.get(api_url, headers=header)

if(r.status_code == 200):

    replay_list_url = 'https://ballchasing.com/api/replays'
    replay_id_dict = dict()

    # Download the List of Replays

    # Download all ranks + 1s, 2s and 3s by looping over them
    for mode in game_modes:
        for rank in ranks:

            # Construct an url for download the replay list for a mode and a rank
            rank_mode_url = f'{replay_list_url}?playlist={mode}&min-rank={rank[0]}&max-rank={rank[1]}&count=20'

            replay_data.append(json.loads(requests.get(
                rank_mode_url, headers=header).text))

    # Extracting the replay ids
    for x in replay_data:
        for y in x['list']:
            # Construct the replay URL and print it, yeah!
            replay_id_dict[y['id']] = ''

    for replay_id, json_data in replay_id_dict.items():
        # Example: https://ballchasing.com/replay/7509cebd-e78e-4214-b92f-024fd39171f5

        # API URL for making requests
        api_url = f'https://ballchasing.com/api/replays/{replay_id}'

        # Make the first request.
        r = requests.get(api_url, headers=header)
        if r.status_code == 200:
            json_data = json.loads(r.text)

            # SQL Statements
            '''
            INSERT into Players (player_id, player_name)
            VALUES ('0123', 'tester1');
            
            insert into replays (replay_id, map, status, playlist_id, duration, season, min_rank, max_rank)
            values ()

            insert into stats (fk_player_id, fk_replay_id, team, stats)
            values ()
            '''

            # Basic variables like mapname, status, playlist id, duration, season
            # min and max rank
            try:
                map_name = json_data['map_name']
                status = json_data['status']
                playlist_id = json_data['playlist_id']
                duration = json_data['duration']
                season = json_data['season']
                min_rank = json_data['min_rank']['name']
                max_rank = json_data['max_rank']['name']

            except KeyError as err:
                print(
                    f'Could not find key {err} in json_data, replay_id: {replay_id}')

            # Get the team stats
            team_stats_blue = get_team_stats(json_data['blue'])
            team_stats_orange = get_team_stats(json_data['orange'])

            # Extract the players from the data
            players = get_player_name_and_id(
                json_data['blue'], json_data['orange'])

            player_stats = get_player_stats(
                replay_id, json_data['blue'], json_data['orange'])

            try:
                c.executemany(
                    'insert into Players (player_id, player_name) Values (?, ?)', players)

            except sqlite3.Error as error:
                print("Failed to insert player data:", error)
            try:
                # Try to insert replay data
                c.execute(
                    'insert into replays (replay_id, map, status, playlist_id, duration, season, min_rank, max_rank, team_stats_orange, team_stats_blue) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (replay_id, map_name, status, playlist_id, duration, season, min_rank, max_rank, team_stats_orange, team_stats_blue))

            except sqlite3.Error as error:
                print("Failed to insert replay data:", error)

            try:
                c.executemany(
                    'insert into stats (fk_player_id, fk_replay_id, team, stats) values (?, ?, ?, ?)', player_stats)
            except sqlite3.Error as error:
                print("Failed to insert player stats data:", error)

            # Make the script sleep for 100ms as we're only allowed to do 10 calls per sec
            sleep(0.1)

        else:
            print(
                f'Request of {replay_id} was not succesful, status: {r.status_code}')
else:
    print('Status code was not 200, please check your api key.')

# Close the database connection
conn.commit()
conn.close()
