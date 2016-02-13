import time
import datetime
import sqlite3 as lite
import sys
from datetime import datetime, date, timedelta
import random
import subprocess

SONG_BLOCK_TIME = 1200
FILENAME = 0
TITLE = 1
FUZZ = 300

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

con = None

class Song:
    FILE = 0
    TITLE = 1
    ARTIST = 2
    TIME = 3
    GENRE = 4
    TEMPO = 5
    DATE = 6

def get_random_song(songs):
    return songs[random.randint(0, len(songs)-1)]

try:
    con = lite.connect('songs.db')
    cur = con.cursor()
    timeSoFar = 0
    songList = ""
    
    while timeSoFar < SONG_BLOCK_TIME:
        day = datetime.today().weekday()
        time = datetime.now().hour

        cur.execute("DROP TABLE IF EXISTS minimum")
        cur.execute("DROP TABLE IF EXISTS best")
        cur.execute("DROP TABLE IF EXISTS genreOnly")
        cur.execute("DROP TABLE IF EXISTS tempoOnly")
        
        cur.execute("CREATE TABLE minimum AS SELECT s.Filename, s.Title, s.Artist, s.TimeInSeconds, s.Genre, s.Tempo, s.LastPlay FROM Songs s INNER JOIN Artists a ON a.Artist = s.Artist WHERE a.LastPlayed BETWEEN ? AND ?", ('2006-01-01 10:00:00.1', str(datetime.now() - timedelta(minutes=1))))
        cur.execute("CREATE TABLE genreOnly AS SELECT m.Filename, m.Title, m.Artist, m.TimeInSeconds, m.Genre, m.Tempo, m.LastPlay FROM GenreConst g INNER JOIN minimum m ON g.Genre = m.Genre WHERE Day = ? AND ? BETWEEN Start AND End", (day, time))
        cur.execute("CREATE TABLE tempoOnly AS SELECT m.Filename, m.Title, m.Artist, m.TimeInSeconds, m.Genre, m.Tempo, m.LastPlay FROM TempoConst t INNER JOIN minimum m ON t.Tempo = m.Tempo WHERE Day = ? AND ? BETWEEN Start AND End", (day, time))
        cur.execute("CREATE TABLE best AS SELECT m.Filename, m.Title, m.Artist, m.TimeInSeconds, m.Genre, m.Tempo, m.LastPlay FROM minimum m NATURAL JOIN (genreOnly g INNER JOIN tempoOnly t ON g.Filename = t.Filename)")
        #print day
        cur.execute("SELECT * FROM best")
        songChoices = cur.fetchall()
        #for row in songChoices:
                #print row + "bes"
        if len(songChoices) == 0:
            cur.execute("SELECT * FROM genreOnly")
            songChoices = cur.fetchall()
            #for row in songChoices:
                #print row + "gen"
        if len(songChoices) == 0:
            cur.execute("SELECT * FROM tempoOnly")
            songChoices = cur.fetchall()
            #for row in songChoices:
                #print row + "tem"
        if len(songChoices) == 0:
            cur.execute("SELECT * FROM minimum")
            songChoices = cur.fetchall()

        #for row in cur.execute("SELECT * FROM minimum"):
            #print row, " minimum\n"
            #songChoices = cur.fetchall()
        #for row in cur.execute("SELECT * FROM genreOnly"):
            #print row, "genre\n"
            #songChoices = cur.fetchall()
        #for row in cur.execute("SELECT * FROM tempoOnly"):
            #print row, "tempo\n"
            #songChoices = cur.fetchall()
        #for row in cur.execute("SELECT * FROM best"):
            #print row, "best\n"
            #songChoices = cur.fetchall()

        song = get_random_song(songChoices)
        #print song
        
        if ((timeSoFar + song[Song.TIME]) < (SONG_BLOCK_TIME + FUZZ)):
            cur.execute("UPDATE Songs SET LastPlay=? WHERE Filename=?", (datetime.now(), song[Song.FILE]))
            cur.execute("UPDATE Artists SET LastPlayed=? WHERE Artist=?", (datetime.now(), song[Song.ARTIST]))
            songList += (song[Song.ARTIST] + "|")
            songList += (song[Song.FILE] + "|")
            songList += (str(song[Song.TIME]) + "|")
            timeSoFar += song[Song.TIME]

            ### debugging print statements ###
            #print "last played " + str((datetime.strptime(song[Song.DATE], "%Y-%m-%d %H:%M:%S.%f")))
            #print "time two minutes ago " + str(datetime.now() - timedelta(minutes=2))
        
    ### send song list to python script ###
    print songList

    con.commit()
    
except lite.Error, e:    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:    
    if con:
        con.close()

