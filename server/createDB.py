import sqlite3 as lite
import sys

users = {
	('Gustaf', 'pass'),
	('Samuel', 'word')
}

con = lite.connect('users.db')

with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS users")
	cur.execute("DROP TABLE IF EXISTS online_users")
	cur.execute("CREATE TABLE users(user_name TEXT, user_pass TEXT)")
	cur.executemany("INSERT INTO users VALUES(?, ?)", users)
	cur.close()