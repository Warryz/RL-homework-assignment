import json
import sqlite3
from datetime import datetime
from queue import Queue
from threading import Thread
from time import sleep
import logging

import requests

from functions import (download_replays, get_player_name_and_id,
                       get_player_stats, get_team_stats)

# Configure the logging
logging.basicConfig(level=logging.ERROR, filename='skript.log', format='[%(levelname)s]: %(asctime)s - %(message)s')

# Number of threads
threads = 4
replay_queue = Queue()

# List of all ingame ranks
ranks = [['unranked', 'unranked'],
         ['bronze-1', 'bronze-3'],
         ['silver-1', 'silver-3'],
         ['gold-1', 'gold-3'],
         ['platinum-1', 'platinum-3'],
         ['diamond-1', 'diamond-3'],
         ['champion-1', 'champion-3'],
         ['grand-champion', 'grand-champion']]

# Number of games to download
number_of_games = 20

# Season of the data to get
season_of_games = 12

# List of all interesting game mods
game_modes = ['ranked-duels', 'ranked-doubles', 'ranked-standard']

# List for replay data
replay_data = list()

# API URL for making requests
api_url = 'https://ballchasing.com/api/'

# Authorization Header
header = {'Authorization': 'abc123'}

# Start the time measurement here
start = datetime.now()
logging.info(f'Started script at {start}.')

# Create a database connection and a cursor for executing commands.
conn = sqlite3.connect('rl.db', check_same_thread=False)
c = conn.cursor()

# Make the first request.
r = requests.get(api_url, headers=header)

if(r.status_code == 200):

    replay_list_url = 'https://ballchasing.com/api/replays'
    replay_queue = Queue()

    # Download the List of Replays

    # Download all ranks + 1s, 2s and 3s by looping over them
    for mode in game_modes:
        for rank in ranks:

            # Construct an url for download the replay list for a mode and a rank
            rank_mode_url = f'{replay_list_url}?playlist={mode}&min-rank={rank[0]}&max-rank={rank[1]}&count={number_of_games}&season={season_of_games}'

            try:
                replay_data.append(json.loads(requests.get(
                    rank_mode_url, headers=header).text))
            except ValueError as val_err:
                logging.critical(f'Json decoding error when parsing {rank_mode_url}')
    # Extracting the replay ids
    for x in replay_data:
        for y in x['list']:
            # Construct the replay URL and print it, yeah!
            replay_queue.put(y['id'])
            logging.debug(f"Added {y['id']} to the queue.")

    # Starting the threads
    for i in range(threads):
        worker = Thread(target=download_replays,
                        args=(i, replay_queue, header, c,))
        worker.setDaemon(True)
        worker.start()
        logging.debug(f'Started thread {i}')

    # Now wait for the queue to be empty, indicating that we have
    # processed all of the downloads.
    logging.info('*** Main thread waiting')
    replay_queue.join()
    logging.info('*** Done')

else:
    logging.critical('Status code was not 200, please check your api key.')

# Close the database connection
conn.commit()
conn.close()

logging.info('Database connection closed.')

# Time of End
end = datetime.now()

# Print notification when script has finished
logging.info(f'Script has finished! Time: {end-start}')
