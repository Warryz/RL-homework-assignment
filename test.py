import json
import sqlite3
from time import sleep
from functions import get_player_name_and_id

import requests

with open('beispiel_list.json') as file:
    data = json.load(file)

    replay_url = 'https://ballchasing.com/api/replays'
    replay_id_dict = dict()

    for x in data['list']:
        # Construct the replay URL and print it, yeah!
        # print(f'{replay_url}/{x["id"]}')

        replay_id_dict[x['id']] = ''

# Authorization Header
header = {'Authorization': 'abc123'}

# Create a database connection and a cursor for executing commands.
conn = sqlite3.connect('rl.db')
c = conn.cursor()

# List of SQL statements to import the data
sql_insert_satement = list()

# Go through the dictionary and download the replay data.
for replay_id, json_data in replay_id_dict.items():
    # Example: https://ballchasing.com/replay/7509cebd-e78e-4214-b92f-024fd39171f5

    # API URL for making requests
    api_url = f'https://ballchasing.com/api/replays/{replay_id}'

    # Make the first request.
    r = requests.get(api_url, headers=header)
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
    map_name = json_data['map_name']
    status = json_data['status']
    playlist_id = json_data['playlist_id']
    duration = json_data['duration']
    season = json_data['season']
    min_rank = json_data['min_rank']['name']
    max_rank = json_data['max_rank']['name']

    # Extract the players from the data
    players = get_player_name_and_id(json_data['blue'], json_data['orange'])

    try:
        c.executemany(
            'insert into Players (player_id, player_name) Values (?, ?)', players)

    except sqlite3.Error as error:
        print("Failed to insert data:", error)
    try:
        # Try to insert replay data
        c.execute(
            'insert into replays (replay_id, map, status, playlist_id, duration, season, min_rank, max_rank) values (?, ?, ?, ?, ?, ?, ?, ?)', (replay_id, map_name, status, playlist_id, duration, season, min_rank, max_rank))

    except sqlite3.Error as error:
        print("Failed to insert replay data:", error)

    # Make the script sleep for 100ms as we're only allowed to do 10 calls per sec
    sleep(0.1)


# Commit the new data and close the database connection AFTER finished the loop.
conn.commit()
conn.close()

ranks = [['unranked', 'unranked'],
         ['bronze-1', 'bronze-3'],
         ['silver-1', 'silver-3'],
         ['gold-1', 'gold-3'],
         ['platinum-1', 'platinum-3'],
         ['diamond-1', 'diamond-3'],
         ['champion-1', 'champion-3'],
         ['grand-champion', 'grand-champion']]

# for x in ranks:
#     print(x)
