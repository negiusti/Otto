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

con = lite.connect('songs.db')
#con.row_factory = lambda cursor, row: row[0]
cur = con.cursor()

# python addrest.py "2" 12 13 -g "emo"
# python addrest.py "1" 13 15 -t "MED UP"
# python addrest.py "6" 7 9 -g "emo"

#cur.execute("DROP TABLE IF EXISTS TempoConst")
#cur.execute("CREATE TABLE TempoConst(Day INT, Start INT, End INT, Tempo TXT, PRIMARY KEY (Day, Start))")
#cur.execute("DROP TABLE IF EXISTS GenreConst")
#cur.execute("CREATE TABLE GenreConst(Day INT, Start INT, End INT, Genre TXT, PRIMARY KEY (Day, Start))")

if (sys.argv[4] == "-g"):
    cur.execute("INSERT INTO GenreConst VALUES(" + sys.argv[1] + ", " + sys.argv[2] + ", " + sys.argv[3] + ", \'" + sys.argv[5] + "\')")    
elif (sys.argv[4] == "-t"):
    cur.execute("INSERT INTO TempoConst VALUES(" + sys.argv[1] + ", " + sys.argv[2] + ", " + sys.argv[3] + ", \'" + sys.argv[5] + "\')")    

for row in cur.execute('SELECT * FROM GenreConst'):
    print row

for row in cur.execute('SELECT * FROM TempoConst'):
    print row

con.commit()
cur.close()
con.close()

