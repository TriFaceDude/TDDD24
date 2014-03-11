import sqlite3 as lite
import sys

users = {
	('Gustaf@', 'pass', 'Gustaf', 'Svanerud', 'Male', 'Linkoping', 'Sweden'),
	('Samuel@', 'word', 'Samuel', 'Lindgren', 'Male', 'Linkoping', 'Sweden')
}

con = lite.connect('users.db')

with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS users")
	cur.execute("DROP TABLE IF EXISTS online_users")
	cur.execute("DROP TABLE IF EXISTS user_messages")
	cur.execute("CREATE TABLE users(user_email TEXT, user_pass TEXT, user_firstname TEXT, user_lastname TEXT, user_gender TEXT, user_city TEXT, user_country TEXT)")
	cur.executemany("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)", users)
	cur.close()