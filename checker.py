import sqlite3 as lite

con = lite.connect('songs.db')
cur = con.cursor()

for row in cur.execute('SELECT * FROM Artists'):
    print row, "artist table"

print

for row in cur.execute('SELECT DISTINCT * FROM Songs'):
    print row

print

for row in cur.execute('SELECT DISTINCT Genre FROM Songs'):
    print row, "genre"

print

for row in cur.execute('SELECT DISTINCT Tempo FROM Songs'):
    print row, "tempo"

print

i = 0
for row in cur.execute('SELECT DISTINCT Artist FROM Songs ORDER BY Artist ASC'):
    print row, " artist ", i
    i+=1 

print

for row in cur.execute('pragma table_info(Songs)'):
	print row

print

for row in cur.execute('SELECT COUNT(*) FROM Artists'):
    print row, "num artists"

print

for row in cur.execute('SELECT * FROM GenreConst'):
    print row, "genre con"

print

for row in cur.execute('SELECT * FROM TempoConst'):
    print row, "tempo con"

con.commit()

cur.close()
con.close()