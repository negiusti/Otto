import time
import datetime
import sqlite3 as lite
import sys
from datetime import datetime, date, timedelta
import random
import subprocess

class Song:
    FILE = 0
    TITLE = 1
    ARTIST = 2
    TIME = 3
    GENRE = 4
    TEMPO = 5
    DATE = 6

### returns the value of a tempo to be used for the fitness function ###
def tempo_value(tempo):
    return tempos.index(tempo)

### returns the value of a genre to be used for the fitness function ###
def genre_value(genre):
    return genres.index(genre)

### holds all of the information 
class Choice(object):
    def __init__(self, artist, file, time, genre, tempo):
        self.artist = artist
        self.file = file
        self.time = time
        self.genre = genre
        self.tempo = tempo

    def to_str(self):
        res = ""
        res += (self.artist + "|")
        res += (self.file + "|")
        res += (self.time + "|")
        return res

### determines the compatability between a potential song choice and the previous song ###
def fitness(choice, previousSong):
    return abs((genre_value(choice.genre) + tempo_value(choice.tempo)) 
    - (genre_value(previousSong.genre) + tempo_value(previousSong.tempo)))

### returns a random song from a list of songs ###
def get_random_song(songs):
    random.seed(datetime.now().second)
    song = songs[random.randint(0, len(songs)-1)]
    return Choice(song[Song.ARTIST], song[Song.FILE], str(song[Song.TIME]), song[Song.GENRE], song[Song.TEMPO])

### SCHEDULING ALGORITHM ###

### 20 minute songs blocks ###
SONG_BLOCK_TIME = 1200 
### song blocks have +- 3 min allowed margin ###
FUZZ = 180 

### all tempos/genres currently entered by the user ###
### TO DO: move tempos/genres to database ###
tempos = ['SLO', 'MED SLO', 'MED', 'MED UP', 'UP']
genres = ["french", "pop", "twee", "jangle pop", "tweemo", 
"experimental pop", "indie pop", "indie", "riot grrl", 
"punk", "folk punk", "folk rock", "folk", "emo", "rock", 
"generic indie", "surf rock", "alternative", "experimental", 
"ska", "cabaret punk", "jazz", "hip hop"]

try:
    ### connect to the database ###
    con = lite.connect('songs.db')
    cur = con.cursor()

    ### amount of time that has been scheduled so far in this block ###
    timeSoFar = 0

    ### string of songs currently scheduled so far ###
    songList = ""

    ### song that is currently being scheduled ###
    song = None
    
    while timeSoFar < SONG_BLOCK_TIME:
        fitnessHash = {}

        ### create table of all songs whose artists have not been recently played ###
        cur.execute("DROP TABLE IF EXISTS minimum")
        cur.execute("CREATE TABLE minimum AS SELECT s.Filename, s.Title, s.Artist, s.TimeInSeconds, s.Genre, s.Tempo, s.LastPlay FROM Songs s INNER JOIN Artists a ON a.Artist = s.Artist WHERE a.LastPlayed BETWEEN ? AND ?", ('2006-01-01 10:00:00.1', str(datetime.now() - timedelta(minutes=2))))
        cur.execute("SELECT * FROM minimum")
        songChoices = cur.fetchall()
        
        topScore = sys.maxint
        if (song == None):
            song = get_random_song(songChoices)
        else:
            ### find the song choice with the best score ###
            for songChoice in songChoices:
                choice = Choice(songChoice[Song.ARTIST], songChoice[Song.FILE], str(songChoice[Song.TIME]), songChoice[Song.GENRE], songChoice[Song.TEMPO])
                if fitness(choice, song) < topScore:
                    topScore = fitness(choice, song)
                    if topScore in fitnessHash:
                        fitnessHash[topScore].append(choice)
                    else:
                        fitnessHash[topScore] = [choice]
            ### pick a random song from the list of songs with the best score ###
            random.seed(datetime.now().second)
            song = fitnessHash[topScore][random.randint(0, len(fitnessHash[topScore])-1)]
        
        ### if the song fits in the current time block, schedule it ###
        if ((timeSoFar + float(song.time)) < (SONG_BLOCK_TIME + FUZZ)):
            ### update database ###
            cur.execute("UPDATE Songs SET LastPlay=? WHERE Filename=?", (datetime.now(), song.file))
            cur.execute("UPDATE Artists SET LastPlayed=? WHERE Artist=?", (datetime.now(), song.artist))
            songList += song.to_str()
            timeSoFar += float(song.time)
        
    ### send song list to python script ###
    print songList

    ### save changes to database ###
    con.commit()
    
except lite.Error, e:    
    print "SQLITE Error %s:" % e.args[0]
    sys.exit(1)
    
finally:    
    if con:
        con.close()