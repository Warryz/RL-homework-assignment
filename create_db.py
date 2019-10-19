import sqlite3


if __name__ == "__main__":

    # Create a database connection and a cursor for executing commands.
    conn = sqlite3.connect('rl.db')
    c = conn.cursor()

    # Create database with tables
    c.executescript('''
    CREATE TABLE "Players" (
	"player_id"	INTEGER,
	"player_name"	TEXT,
	PRIMARY KEY("player_id"));
    
    CREATE TABLE "Replays" (
	"replay_id"	TEXT,
	"map"	TEXT,
	"status"	TEXT,
	"playlist_id"	TEXT,
	"duration"	INTEGER,
	"season"	INTEGER,
	"min_rank"	TEXT,
	"max_rank"	TEXT,
	"team_stats_orange"	TEXT,
	"team_stats_blue"	TEXT,
	PRIMARY KEY("replay_id"));

    CREATE TABLE "Stats" (
	"fk_player_id"	TEXT,
	"fk_replay_id"	TEXT,
	"team"	INTEGER,
	"Stats"	TEXT,
	FOREIGN KEY("fk_player_id") REFERENCES "Players"("player_id"),
	PRIMARY KEY("fk_player_id","fk_replay_id"),
	FOREIGN KEY("fk_replay_id") REFERENCES "Replays"("replay_id"));  
    ''')

    # close the database connection
    conn.commit()
    conn.close()
