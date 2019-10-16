# import requests
import json
import requests

from classes import Game, Player

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
header = {'Authorization': 'abc123'}  # ADD the API key here!

# Make the first request.
r = requests.get(api_url, headers=header)

if(r.status_code == 200):

    replay_list_url = 'https://ballchasing.com/api/replays'

    # Download the List of Replays

    # Download all ranks + 1s, 2s and 3s by looping over them
    for mode in game_modes:
        for rank in ranks:

            # Construct an url for download the replay list for a mode and a rank
            rank_mode_url = f'{replay_list_url}?playlist={mode}&min-rank={rank[0]}&max-rank={rank[1]}&count=10'
            print(rank_mode_url)
            # replay_data.append(requests.get(rank_mode_url))

else:
    print('Status code was not 200, please check your api key.')


'''
with open('beispiel.json') as file:
    data = json.load(file)

    for x in data['blue']['players']:
        # Create new player objects
        players.append(Player(x['name'], x['id']['id']))

    for x in data['orange']['players']:
        # Create new player objects
        players.append(Player(x['name'], x['id']['id']))

    # Output the game id
    print(data['id'])
for x in players:
    print(x)
'''
