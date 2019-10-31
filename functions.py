import json
from datetime import datetime
import requests
import sqlite3
import logging


def get_player_name_and_id(blue_team, orange_team):
    player_name_id_list = list()
    try:

        for player in blue_team['players']:
            player_name_id_list.append(
                (int(player['id']['id']), player['name']))

        for player in orange_team['players']:
            player_name_id_list.append(
                (int(player['id']['id']), player['name']))
    except (ValueError, KeyError) as err:
        logging.exception(f'Error when getting player names or ids: {err}')

    return player_name_id_list


def get_player_stats(replay_id, blue_team, orange_team):
    'Gets the player stats and returns them as a list'
    player_stats_list = list()
    # fk_player_id, fk_replay_id, team, stats
    # Add blue players
    for player in blue_team['players']:
        player_stats_list.append(
            (player['id']['id'], replay_id,
             blue_team['color'], str(player['stats']))
        )

    # Add orange players
    for player in orange_team['players']:
        player_stats_list.append(
            (player['id']['id'], replay_id,
             orange_team['color'], str(player['stats']))
        )
    return player_stats_list


def get_team_stats(team):
    return str(team['stats'])


def download_replays(i, q, header, c):
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
        replay = q.get()
        api_url = f'https://ballchasing.com/api/replays/{replay}'
        logging.debug(f'Thread {i}: Getting replay {replay}')

        # Make the first request.
        r = requests.get(api_url, headers=header)
        try:
            json_data = json.loads(r.text)
        except ValueError as json_err:
            logging.exception(
                f'Json decoding error when decoding replay {replay}: {json_err}')
        except requests.exceptions.ConnectionError as con_error:
            logging.exception(
                f'Connection has failed when getting replay {replay}: {con_error}')

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
        except KeyError as key_err:
            logging.exception(
                f'Thread {i}: Error when accessing a json key: {key_err}')

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
            logging.exception(f'Failed to insert player data: {error}')
        try:
            # Try to insert replay data
            c.execute(
                'insert into replays (replay_id, map, status, playlist_id, duration, season, min_rank, max_rank, team_stats_orange, team_stats_blue) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (replay, map_name, status, playlist_id, duration, season, min_rank, max_rank, team_stats_orange, team_stats_blue))

        except sqlite3.Error as error:
            logging.exception(
                f'Failed to insert replay {replay} data: {error}')

        try:
            c.executemany(
                'insert into stats (fk_player_id, fk_replay_id, team, stats) values (?, ?, ?, ?)', player_stats)
        except sqlite3.Error as error:
            logging.exception(f'Failed to insert player stats data: {error}')

        # Make the script sleep for 100ms as we're only allowed to do 10 calls per sec
        query_end = datetime.now()
        logging.error(f'Thread {i}: {query_end-query_start}, {r.status_code}')

        logging.info(f'Finished replay id {replay}')
        q.task_done()


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
    player_stats = get_player_stats('7509cebd-e78e-4214-b92f-024fd39171f5',
                                    data['blue']['players'], data['orange']['players'])

    print(player_stats)
