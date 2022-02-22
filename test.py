import sqlite3

with sqlite3.connect("netflix.db") as con:
    cur = con.cursor()

    a = "Sports Movies"

    sql = "select `title` from netflix n where n.listed_in LIKE ?"
    cur.execute(sql, (a,))

print(cur.fetchall())
