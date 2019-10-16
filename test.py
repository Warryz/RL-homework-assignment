import json
from time import sleep

import requests

with open('beispiel_list.json') as file:
    data = json.load(file)

    replay_url = 'https://ballchasing.com/api/replays/'
    replay_id_dict = dict()

    for x in data['list']:
        # Construct the replay URL and print it, yeah!
        print(f'{replay_url}/{x["id"]}')

        replay_id_dict[x['id']] = ''


# Go through the dictionary and download the replay data.
for replay_id, json_data in replay_id_dict.items():
    # Example: https://ballchasing.com/replay/7509cebd-e78e-4214-b92f-024fd39171f5

    # API URL for making requests
    api_url = f'https://ballchasing.com/api/replay/{replay_id}'

    # Authorization Header
    header = {'Authorization': '123abc'}

    # Make the first request.
    r = requests.get(api_url, headers=header)

    # Make the script sleep for 100ms as we're only allowed to do 10 calls per sec
    time.sleep(0.1)

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
