import sqlite3 as lite

con = lite.connect('songs.db')
cur = con.cursor()

for row in cur.execute('SELECT * FROM Artists'):
    print row

for row in cur.execute('SELECT DISTINCT * FROM Songs'):
    print row

for row in cur.execute('SELECT DISTINCT Genre FROM Songs'):
    print row

for row in cur.execute('SELECT DISTINCT Tempo FROM Songs'):
    print row, " tempo"

#for row in cur.execute('SELECT * FROM TempoConst'):
#    print row

for row in cur.execute('pragma table_info(Songs)'):
	print row

#cur.execute('ALTER TABLE Songs RENAME TO blah')
#cur.execute('CREATE TABLE Songs (Filename TEXT, Title TEXT, Artist TEXT, TimeInSeconds INT, Genre TEXT, Tempo TEXT, LastPlay DATETIME)')
#cur.execute('INSERT INTO Songs(Filename, Title, Artist, TimeInSeconds, Genre, Tempo, LastPlay) SELECT Filename, Title, Artist, TimeInSeconds, Tempo, Genre, LastPlay FROM blah')
#cur.execute('DROP TABLE blah')


for row in cur.execute('SELECT * FROM Artists'):
    print row

#for row in cur.execute('SELECT DISTINCT * FROM Songs'):
    #print row

for row in cur.execute('SELECT DISTINCT Genre FROM Songs'):
    print row, "genre"

for row in cur.execute('SELECT DISTINCT Tempo FROM Songs'):
    print row, " tempo"

for row in cur.execute('SELECT DISTINCT Artist FROM Songs'):
    print row, " artist"

#for row in cur.execute('SELECT * FROM TempoConst'):
#    print row

for row in cur.execute('pragma table_info(Songs)'):
	print row

cur.close()
con.close()


cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED UP', 'Subdebs'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED', 'The Beach Boys'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED UP', 'The Dresden Dolls'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED', 'The Dirty Projectors'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED UP', 'The Front Bottoms'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED SLO', 'The Mountain Goats'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('UP', 'The Pietasters'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('UP', 'The Planet Smashers'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED', 'The Specials'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED SLO', 'Total Babe'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('UP', 'tough stuff'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED', 'Vampire Weekend'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED UP', 'Walter Mitty and his Makeshift Orchestra'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('SLO', 'Waxahatchee'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('UP', 'Wingnut Dishwashers Union'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('SLO', 'Zigtebra'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('UP', 'Wood Spider'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('SLO', 'Widowspeak'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('UP', 'You Me & Us'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('UP', 'Baby Guts'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('UP', 'Be Your Own Pet'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED', 'Animal Collective'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED SLO', 'American Football'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED UP', 'Amanda Palmer'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED', 'All-Time Quarterback'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED UP', 'Allo Darlin'))
cur.execute("UPDATE Songs SET Tempo=? WHERE Artist=?", ('MED UP', 'All Girl Summer Fun Band'))
