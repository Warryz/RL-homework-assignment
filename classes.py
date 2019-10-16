import sqlite3

class Rocket_League_Object(object):
    pass

class Player(object):
    def __init__(self, player_name, player_id):
        self.player_name = player_name
        self.player_id = player_id

    def get_name(self):
        return str(self.player_name)
    
    def get_player_id(self):
        return self.player_id

    def __str__(self):
        return f'Name: {self.player_name} | ID: {self.player_id}'

class Game(object):
    def __init__(game_id, map_name, status, playlist_id, duration, season, min_rank, max_rank, blue, orange):
        pass

        