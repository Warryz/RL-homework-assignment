import json
import sqlite3
import time
from datetime import datetime
from queue import Queue
from threading import Thread

import requests

from functions import get_player_name_and_id, get_player_stats, get_team_stats

# Number of threads
threads = 4
replay_queue = Queue()

# Authorization Header
header = {'Authorization': 'abc123'}

start = datetime.now()


def downloadEnclosures(i, q):
    """This is the worker thread function.
    It processes items in the queue one after
    another.  These daemon threads go into an
    infinite loop, and only exit when
    the main thread ends.
    """
    while True:
        query_start = datetime.now()
        # Example: https://ballchasing.com/replay/7509cebd-e78e-4214-b92f-024fd39171f5

        # API URL for making requests
        print(f'Thread {i}: Getting the next replay')
        replay = q.get()
        api_url = f'https://ballchasing.com/api/replays/{replay}'
        print(f'Thread {i}: Getting replay {replay}')

        # Make the first request.
        r = requests.get(api_url, headers=header)
        json_data = json.loads(r.text)

        # Basic variables like mapname, status, playlist id, duration, season
        # min and max rank
        map_name = json_data['map_name']
        status = json_data['status']
        playlist_id = json_data['playlist_id']
        duration = json_data['duration']
        season = json_data['season']
        min_rank = json_data['min_rank']['name']
        max_rank = json_data['max_rank']['name']

        # Get the team stats
        team_stats_blue = get_team_stats(json_data['blue'])
        team_stats_orange = get_team_stats(json_data['orange'])

        # Extract the players from the data
        players = get_player_name_and_id(
            json_data['blue'], json_data['orange'])

        player_stats = get_player_stats(
            replay, json_data['blue'], json_data['orange'])

        try:
            c.executemany(
                'insert into Players (player_id, player_name) Values (?, ?)', players)

        except sqlite3.Error as error:
            print("Failed to insert player data:", error)
        try:
            # Try to insert replay data
            c.execute(
                'insert into replays (replay_id, map, status, playlist_id, duration, season, min_rank, max_rank, team_stats_orange, team_stats_blue) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (replay, map_name, status, playlist_id, duration, season, min_rank, max_rank, team_stats_orange, team_stats_blue))

        except sqlite3.Error as error:
            print("Failed to insert replay data:", error)

        try:
            c.executemany(
                'insert into stats (fk_player_id, fk_replay_id, team, stats) values (?, ?, ?, ?)', player_stats)
        except sqlite3.Error as error:
            print("Failed to insert player stats data:", error)

        # Make the script sleep for 100ms as we're only allowed to do 10 calls per sec
        query_end = datetime.now()
        print(f'Thread {i}: {query_end-query_start}, {r.status_code}')

        q.task_done()


# Set up some threads to fetch the enclosures
for i in range(threads):
    worker = Thread(target=downloadEnclosures, args=(i, replay_queue,))
    worker.setDaemon(True)
    worker.start()

with open('beispiel_list.json') as file:
    data = json.load(file)

    replay_url = 'https://ballchasing.com/api/replays'

    for x in data['list']:
        # Construct the replay URL and print it, yeah!
        replay_queue.put(x['id'])


# Create a database connection and a cursor for executing commands.
conn = sqlite3.connect('rl.db')
c = conn.cursor()

# Now wait for the queue to be empty, indicating that we have
# processed all of the downloads.
print('*** Main thread waiting')
replay_queue.join()
print('*** Done')

conn.commit()
conn.close()

# End
end = datetime.now()
print(f'{end-start}')

ranks = [['unranked', 'unranked'],
         ['bronze-1', 'bronze-3'],
         ['silver-1', 'silver-3'],
         ['gold-1', 'gold-3'],
         ['platinum-1', 'platinum-3'],
         ['diamond-1', 'diamond-3'],
         ['champion-1', 'champion-3'],
         ['grand-champion', 'grand-champion']]
