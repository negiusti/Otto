import sqlite3 as lite

class Song:
    FILE = 0
    TITLE = 1
    ARTIST = 2
    TIME = 3
    GENRE = 4
    TEMPO = 5
    DATE = 6

#con = lite.connect('songs.db')
#cur = con.cursor()

#cur.execute("SELECT * FROM Songs")

#songChoices = cur.fetchall()

#for songChoice in songChoices:
#    print songChoice

dic = {}

con = lite.connect('songs.db')
cur = con.cursor()

#cur.execute("DROP TABLE Artists")
#cur.execute("CREATE TABLE Artists(Artist TEXT PRIMARY KEY, LastPlayed DATETIME, FOREIGN KEY(Artist) REFERENCES Songs(Artist))")

cur.execute("SELECT * FROM Songs")
songChoices = cur.fetchall()
for song in songChoices:
    print song

#for row in cur.execute('SELECT * FROM Songs'):
for row in songChoices:
    cur.execute("SELECT * FROM Artists WHERE Artist = " + "\"" + row[Song.ARTIST] + "\"")
    data=cur.fetchall()
    if len(data)==0:
        statement = "INSERT INTO Artists VALUES(\"" + row[Song.ARTIST] + "\", \"" + row[Song.DATE] + "\")"
        cur.execute("INSERT INTO Artists VALUES(\"" + row[Song.ARTIST] + "\", \"" + row[Song.DATE] + "\")")
        dic[row[Song.ARTIST]] = str(row[Song.DATE])
    elif row[Song.ARTIST] in dic:
        if str(dic[row[Song.ARTIST]]) < row[Song.DATE]:
            dic[row[Song.ARTIST]] = str(row[Song.DATE])
    
for key in dic:
    statement = "UPDATE Artists SET LastPlayed = \'" + dic[key] + "\' WHERE Artist = \'" + key + "\'"
    print statement
    cur.execute(statement)

for row in cur.execute('SELECT * FROM Artists'):
    print row

con.commit()
cur.close()
con.close()


#web service 
#vs
#python ffi to call the c functions



