import sqlite3 as lite
import sys
import random
import os
import wave
import contextlib
#from subprocess import Popen, PIPE
import subprocess
#from sys import argv
#python addsongstodb.py /path/to/folder/ artist_name genre tempo
SONG_BLOCK_TIME = 1200
FILENAME = 0
TITLE = 1
FUZZ = 300

con = None
# command to add songs to database
# python addsongstodb.py "/Users/nicolegiusti/Music/iTunes/iTunes Media/Music/Baby Guts/The Kissing Disease" "Baby Guts" "riot grrl" "UP"


def getDuration(fname):
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return str(duration)

def convertToWAV(filename):
    command = "afconvert -f 'WAVE' -d I16@44100 \""+ os.path.join(sys.argv[1], filename) + "\" \"/Users/nicolegiusti/Documents/seniorproject/pls/songs/" + filename[:len(filename)-4] + ".wav\""
    print command
    os.system(command)
    return filename[:len(filename)-4] +".wav"

#afconvert -f 'WAVE' -d I16@44100 05-Michael.m4a 05-Michael.wav

con = lite.connect('songs.db')
#con.row_factory = lambda cursor, row: row[0]
cur = con.cursor()
        
#cur.execute("DROP TABLE IF EXISTS Songs")
#cur.execute("CREATE TABLE Songs(Filename TEXT, Title TEXT, Artist TEXT, TimeInSeconds INT, Genre TEXT, Tempo TEXT, LastPlay DATETIME)")   

# python addsongstodb.py "/Users/nicolegiusti/Music/iTunes/iTunes Media/Music/Baby Guts/The Kissing Disease" "Baby Guts" "riot grrl" "UP"

for filename in os.listdir(sys.argv[1]):
    if filename.endswith(".wav") or filename.endswith(".m4a") or filename.endswith(".mp3"): 
        statement = "INSERT INTO Songs VALUES(\"" + convertToWAV(filename) + "\", \"" + filename[:len(filename)-4] + "\", \'" + sys.argv[2] + "\'," + getDuration(os.path.join("/Users/nicolegiusti/Documents/seniorproject/pls/songs/",filename[:len(filename)-4]+".wav")) + ", \'" + sys.argv[3] + "\', \'" + sys.argv[4] + "\', '2007-01-01 10:00:00')"
        print statement
        cur.execute(statement)
        
        cur.execute("SELECT * FROM Artists WHERE Artist = " + "\"" + sys.argv[2] + "\"")
        data=cur.fetchall()
        if len(data)==0:
            statement = "INSERT INTO Artists VALUES(\"" + sys.argv[2] + "\", '2007-01-01 10:00:00')"
            print statement
            cur.execute(statement)

con.commit()

songChoices = cur.fetchall()
for songChoice in songChoices:
    print songChoices
    

con.close()

