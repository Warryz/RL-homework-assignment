import json

with open('beispiel_list.json') as file:
    data = json.load(file)

    replay_url = 'https://ballchasing.com/api/replays/id'
    replay_id_dict = dict()

    for x in data['list']:
        # Construct the replay URL and print it, yeah!
        print(f'{replay_url}/{x["id"]}')

        replay_id_dict[x['id']] = ''

    # Output the game id
    # print(data['id'])
    print(replay_id_dict)


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
