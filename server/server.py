from flask import *

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)



	
def user_exists(email):
	users = get_users()
	
	return users.__contains__(email)

	



#Returns bool, true if email belongs to online user
def is_online_by_email(email):
	online_users = get_online_users()
	return online_users.values().__contains__(email)
	

#Returns bool, true if token belongs to online user
def is_online_by_token(token):
	online_users = get_online_users()
	return online_users.__contains__(token)
	
def get_user_data_by_token(token):
	users = get_users()
	
	return users[token_to_email(token)]
	
def get_user_data_by_email(token, email):
	
	if is_online_by_token(token):
		users = get_users()
		return users[email]
	
#Takes token, returns email
def token_to_email(token):
	online_users = get_online_users()
	
	return online_users[token]
	
	
#Takes email, returns token
def email_to_token(email):
	online_users = get_online_users()
	
	return online_users[email]['token']

#Adds user to online users
def set_user_signed_in(email, token):
	db = connect_db()
	cur = db.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS online_users(user_email TEXT, user_token TEXT)")
	cur.execute("INSERT INTO online_users (user_email, user_token) VALUES(?,?)", (email, token))
	db.commit()
	db.close()
	
def valid_password(email, password):
	users = get_users()
	return users[email]['password'] == password
	
#Validates login and sets user online,
#if success returns {status, msg, data}
#if fail returns {status, msg}
def sign_in(email, password):
	users = get_users()
	
	if is_online_by_email(email):
		return {'status' : 'Fail', 'msg' : 'User already signed in.'}
	
	if users.__contains__(email):
		if users[email]['password'] == password:
			set_user_signed_in(email,'1234')
			return {'status' : 'Success', 'msg' : 'Signed in.', 'data' : 'token'}
			
	return {'status' : 'Fail', 'msg' : 'Wrong email or password.'}
	
def set_user_offline(token):
	print('deleting...')
	db = connect_db()
	db.execute('DELETE FROM online_users WHERE user_token=?', (token,))
	db.commit()
	db.close()
	
#Sets user offline, returns {status, msg}
def sign_out(token):

	if not is_online_by_token(token):
		return {'status' : 'Fail', 'msg' : 'Token not valid.'}

	online_users = get_online_users()
	
	if online_users.__contains__(token):
		set_user_offline(token)
		
	return {'status' : 'Success', 'msg' : 'User signed out.'}
	
def create_user(email, password, firstname, lastname, gender, city, country):

	user = (email, password, firstname, lastname, gender, city, country)
	db = connect_db()
	cur = db.cursor()
	cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)", user)
	db.commit()
	db.close()
	
def valid_user_data(email, password, firstname, lastname, gender, city, country):

	#Email pattern, password pattern and string pattern
	ep = "[^@]+@[^@]+\.[^@]+"
	pp = "[A-Za-z0-9!@#$%5&/=?]{9,}"
	sp = "^[a-zA-Z]+$"

	return bool(re.match(ep, email)) and  bool(re.match(pp, password)) and  bool(re.match(sp, firstname)) and  bool(re.match(sp, lastname)) and  bool(re.match(sp, gender)) and  bool(re.match(sp, country))
	
def sign_up(email, password, firstname, lastname, gender, city, country):

	if user_exists(email):
		return {'status' : 'Fail', 'msg' : 'User already exists.'}
		
	if not valid_user_data(email, password, firstname, lastname, gender, city, country):
		return {'status' : 'Fail', 'msg' : 'Invalid user data.'}

	create_user(email, password, firstname, lastname, gender, city, country)
	return {'status' : 'Success', 'msg' : 'User registered.'}

def set_user_password(email, new_password):
	
	print('USER INFO:')
	print(email)
	print(new_password)
	db = connect_db()
	cur = db.cursor()
	cur.execute("UPDATE users SET user_pass=? WHERE user_email=?", (new_password,email))
	#cur.execute("UPDATE users SET user_pass='hej' WHERE user_email='Gustaf@'")
	db.commit()
	db.close()
	
def change_password(token, old_password, new_password):
	
	if not is_online_by_token(token):
		return {'status' : 'Fail', 'msg' : 'User not signed in.'}
	
	if not valid_password(token_to_email(token), old_password):
		return {'status' : 'Fail', 'msg' : 'Wrong password.'}
		
	set_user_password(token_to_email(token), new_password)
	return {'status' : 'Success', 'msg' : 'Password changed.'}
	
def write_message(token, email, msg):

	db = connect_db()	
	cur = db.cursor()	
	cur.execute("CREATE TABLE IF NOT EXISTS user_messages (receiver_email TEXT, msg_index INTEGER, sender_email TEXT, msg_content TEXT)")
	
	cur.execute("SELECT COUNT(*) FROM user_messages WHERE receiver_email=?", (email,))
	cur.execute("INSERT INTO user_messages VALUES(?, ?, ?, ?)", (email, msg_index, token_to_email(token), msg))
	db.commit()
	cur.close()
	
def retrive_messages(email):

	db = connect_db()	
	cur = db.cursor()
	cur.execute("SELECT msg_index, sender_email, msg_content FROM user_messages WHERE receiver_email=?", (email,))
	
	messages = []
	for row in cur.fetchall():
		messages.append({'msg_id' : row[0], 'sender_email' : row[1], 'msg_content' : row[2]})
	
	return messages

def get_user_messages_by_token(token):
	return get_user_messages_by_email(token, token_to_email(token)):
	
def get_user_messages_by_email(token, email):
	
	if not is_online_by_token(token):
		return {'status' : 'Fail', 'msg' : 'User not signed in.'}
		
	return retrive_messages(email)
	
def post_message(token, email, msg):
	
	if not is_online_by_token(token):
		return {'status' : 'Fail', 'msg' : 'User not signed in.'}
		
	write_message(token, email, msg)
	
	return {'status' : 'Success', 'msg' : 'Message posted.'}
		

	
	
#Test method, will run on page refresh	
@app.route('/')	
def test():

	#return str(get_user_data_by_token('1234'))
	#return str(get_user_data_by_email('1234', 'Samuel@'))
	#return str(sign_out('1234'))
	print(str(sign_in('Gustaf@','pass')))
	#return str(sign_up('Guuuuuustaf@', 'pasujs', 'Gusujutaf', 'Svanerujuud', 'Mujuale', 'Linkujuoping', 'Swedujuen'))
	#return str(change_password('1234', 'pass', 'padd'))
	#return str(post_message('1234', 'Gustaf@', 'hej'))
	return str(get_user_messages_by_email('1234', 'Gustaf@'))
	
if __name__ == '__main__':
    app.run()