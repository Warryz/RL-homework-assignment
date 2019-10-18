import json


def get_player_name_and_id(blue_team, orange_team):
    player_name_id_list = list()
    try:

        for player in blue_team['players']:
            player_name_id_list.append(
                (int(player['id']['id']), player['name']))

        for player in orange_team['players']:
            player_name_id_list.append(
                (int(player['id']['id']), player['name']))
    except ValueError:
        pass

    return player_name_id_list


if __name__ == "__main__":
    data = ''
    with open('beispiel_game.json') as file:
        data = json.load(file)

    player_dict = get_player_name_and_id(data['blue'], data['orange'])
    print(player_dict)
