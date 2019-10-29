import json
import sqlite3
import time
from datetime import datetime
from queue import Queue
from threading import Thread

import requests

from functions import get_player_name_and_id, get_player_stats, get_team_stats, download_replays

# Number of threads
threads = 4
replay_queue = Queue()

# Authorization Header
header = {'Authorization': 'abc123'}

start = datetime.now()


# Create a database connection and a cursor for executing commands.
conn = sqlite3.connect('rl.db', check_same_thread=False)
c = conn.cursor()

# Set up some threads to fetch the enclosures
for i in range(threads):
    worker = Thread(target=download_replays,
                    args=(i, replay_queue, header, c,))
    worker.setDaemon(True)
    worker.start()

with open('beispiel_list.json') as file:
    data = json.load(file)

    replay_url = 'https://ballchasing.com/api/replays'

    for x in data['list']:
        # Construct the replay URL and print it, yeah!
        replay_queue.put(x['id'])


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
