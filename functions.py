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


def get_player_stats(blue_team, orange_team):
    'Gets the player stats and returns them as a list'
    player_stats_list = list()

    # Add blue players
    for player in blue_team:
        player_stats_list.append(
            {player['id']['id']: player['stats']}
        )

    # Add orange players
    for player in orange_team:
        player_stats_list.append(
            {player['id']['id']: player['stats']}
        )
    return player_stats_list


def get_team_stats(team):
    return team['stats']


if __name__ == "__main__":
    data = ''
    with open('beispiel_game.json') as file:
        data = json.load(file)

    player_dict = get_player_name_and_id(data['blue'], data['orange'])
    # print(player_dict)

    # Get the team stats
    team_stats_blue = get_team_stats(data['blue'])
    team_stats_orange = get_team_stats(data['orange'])

    # Get the player specific stats
    player_stats = get_player_stats(
        data['blue']['players'], data['orange']['players'])

    print(player_stats)
