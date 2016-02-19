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

def t_enum_pls(s):
    SLO = 0
    MEDSLO = 10
    MED = 20
    MEDUP = 30
    UP = 40
    if s == "SLO":
        return SLO
    elif s == "MED SLO":
        return MEDSLO
    elif s == "MED":
        return MED
    elif s == "MED UP":
        return MEDUP
    elif s == "UP":
        return UP


def g_enum_pls(s):
    french = 0
    pop = 10
    twee = 20
    jangle = 30
    indie = 40
    riot_grrl = 50
    punk = 60
    folk = 70
    emo = 80
    rock = 90
    generic = 100
    surf = 110
    alternative = 120
    experimental = 130
    ska = 140
    cabaret = 150
    jazz = 160
    hip_hop = 170
    count = 0
    total = 0
    if "french" in s:
        count +=1
        total += french
    elif "pop" in s:
        count +=1
        total += pop
    elif "twee" in s:
        count +=1
        total += twee
    elif "jangle" in s:
        count +=1
        total += jangle
    elif "indie" in s:
        count +=1
        total += indie
    elif "riot grrl" in s:
        count +=1
        total += riot_grrl
    elif "punk" in s:
        count +=1
        total += punk
    elif "folk" in s:
        count +=1
        total += folk
    elif "emo" in s:
        count +=1
        total += emo
    elif "rock" in s:
        count +=1
        total += rock
    elif "generic" in s:
        count +=1
        total += generic
    elif "surf" in s:
        count +=1
        total += surf
    elif "alternative" in s:
        count +=1
        total += alternative
    elif "experimental" in s:
        count +=1
        total += experimental
    elif "ska" in s:
        count +=1
        total += ska
    elif "cabaret" in s:
        count +=1
        total += cabaret
    elif "jazz" in s:
        count +=1
        total += jazz
    elif "hip hop" in s:
        count +=1
        total += hip_hop
    return total/count

class Choice(object):
    def __init__(self, artist, file, time, genre, tempo):
        self.artist = artist
        self.file = file
        self.time = time
        self.genre = genre
        self.tempo = tempo

    def toStr(self):
        res = ""
        res += (self.artist + "|")
        res += (self.file + "|")
        res += (self.time + "|")
        return res

def fitness(choice, previousSong):
    return abs((g_enum_pls(choice.genre) + t_enum_pls(choice.tempo)) 
    - (g_enum_pls(previousSong.genre) + t_enum_pls(previousSong.tempo)))

def get_random_song(songs):
    song = songs[random.randint(0, len(songs)-1)]
    return Choice(song[Song.ARTIST], song[Song.FILE], str(song[Song.TIME]), song[Song.GENRE], song[Song.TEMPO])

try:
    con = lite.connect('songs.db')
    cur = con.cursor()
    timeSoFar = 0
    songList = ""
    song = None
    
    while timeSoFar < SONG_BLOCK_TIME:
        day = datetime.today().weekday()
        time = datetime.now().hour
        fitnessHash = {}

        cur.execute("DROP TABLE IF EXISTS minimum")
        cur.execute("DROP TABLE IF EXISTS best")
        cur.execute("DROP TABLE IF EXISTS genreOnly")
        cur.execute("DROP TABLE IF EXISTS tempoOnly")
        
        cur.execute("CREATE TABLE minimum AS SELECT s.Filename, s.Title, s.Artist, s.TimeInSeconds, s.Genre, s.Tempo, s.LastPlay FROM Songs s INNER JOIN Artists a ON a.Artist = s.Artist WHERE a.LastPlayed BETWEEN ? AND ?", ('2006-01-01 10:00:00.1', str(datetime.now() - timedelta(minutes=2))))

        #cur.execute("CREATE TABLE genreOnly AS SELECT m.Filename, m.Title, m.Artist, m.TimeInSeconds, m.Genre, m.Tempo, m.LastPlay FROM GenreConst g INNER JOIN minimum m ON g.Genre = m.Genre WHERE Day = ? AND ? BETWEEN Start AND End", (day, time))
        #cur.execute("CREATE TABLE tempoOnly AS SELECT m.Filename, m.Title, m.Artist, m.TimeInSeconds, m.Genre, m.Tempo, m.LastPlay FROM TempoConst t INNER JOIN minimum m ON t.Tempo = m.Tempo WHERE Day = ? AND ? BETWEEN Start AND End", (day, time))
        #cur.execute("CREATE TABLE best AS SELECT m.Filename, m.Title, m.Artist, m.TimeInSeconds, m.Genre, m.Tempo, m.LastPlay FROM minimum m NATURAL JOIN (genreOnly g INNER JOIN tempoOnly t ON g.Filename = t.Filename)")
        #print day
        cur.execute("SELECT * FROM minimum")
        songChoices = cur.fetchall()
        topScore = 1000
        for row in songChoices:
            if (song == None):
                song = get_random_song(songChoices)
                break
            else:
                choice = Choice(row[Song.ARTIST], row[Song.FILE], str(row[Song.TIME]), row[Song.GENRE], row[Song.TEMPO])
                if fitness(choice, song) < topScore:
                    topScore = fitness(choice, song)
                    if topScore in fitnessHash:
                        fitnessHash[topScore].append(choice)
                    else:
                        fitnessHash[topScore] = [choice]
            song = fitnessHash[topScore][random.randint(0, len(fitnessHash[topScore])-1)]
    

        """if len(songChoices) == 0:
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
            songChoices = cur.fetchall()"""

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

        
        #print song
        
        if ((timeSoFar + float(song.time)) < (SONG_BLOCK_TIME + FUZZ)):
            cur.execute("UPDATE Songs SET LastPlay=? WHERE Filename=?", (datetime.now(), song.file))
            cur.execute("UPDATE Artists SET LastPlayed=? WHERE Artist=?", (datetime.now(), song.artist))
            #c = Choice (song[Song.ARTIST], song[Song.FILE], str(song[Song.TIME]))
            songList += song.toStr()
            timeSoFar += float(song.time)

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