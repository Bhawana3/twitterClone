"""
DELIMITER $$
CREATE
DEFINER=`root`@`localhost`
PROCEDURE `register`(IN _username VARCHAR(100),IN _email VARCHAR(100),IN _password VARCHAR(50))
BEGIN
    if ( select exists (select 1 from users where username = _username) ) THEN
        select 'Username Already Exists !!';
    ELSE
        insert into users (username,email,password) values (_username,_email,_password);
    END IF;
END$$
DELIMITER ;
"""

"""
| users | CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 |

"""

from flask import Flask,request,json,render_template,session,redirect,url_for,escape
from flask.ext.mysql import MySQL

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('write_tweet.html')

@app.route('/#')
def index():
    if session.get('logged_in') == True:
        return 'You are logged in'
    return 'You are not logged in'

@app.route('/signup/')
def sign_up():
    return render_template('register.html')

@app.route('/login/')
def log_in():
    return render_template('login.html')

mysql = MySQL()

#MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cutiepie07'
app.config['MYSQL_DATABASE_DB'] = 'twitter_clone'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/user/signup',methods=['POST'])
def signUp():
    _username = request.form['username']
    _email = request.form['email']
    _password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('register',(_username,_email,_password))              #calls procedure register
    data = cursor.fetchall()
    print data
    if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})


@app.route('/user/login',methods=['POST'])
def login():
    _email = request.form['email']
    _password = request.form['password']

    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE email=" + "'" + _email + "'"
    cursor.execute(query)
    data = cursor.fetchall()

    if len(data) == 1:
        username = data[0][1]
        email = data[0][2]
        print username,email
        session['username'] = username
        session['email'] = email
        print 'User Logged in successfully!!'
        return redirect(url_for('profile'))
    else:
        return json.dumps({'error':str(data[0])})

#inserting tweets into user table
@app.route('/tweet',methods=["POST"])
def insert_into_db():
    _username = request.form['input_user']
    _tweet = request.form['input_tweet']

    conn = mysql.connect()                                                                  # connecting to mysql
    cursor = conn.cursor()
    query = "INSERT INTO user_tweets(username,tweet) VALUES(" + "'" + _username + "','" + _tweet + "')"              #_username = string containing username of the current user
    cursor.execute(query)
    data = cursor.fetchall()

    if len(data) == 1:
        conn.commit()
        return json.dumps({'message':'Tweet added successfully!'})
    else:
        return json.dumps({'error':str(data[0])})

# user profile
@app.route('/profile',methods=['GET'])
def profile():
    if 'username' in session:
        username = session['username']
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT tweet,created_at FROM user_tweets WHERE username ='" + username + "'" + "ORDER BY created_at DESC"
        cursor.execute(query)
        tweet = cursor.fetchall()
        conn.commit()
        return json.dumps({'tweets:': tweet})
    else:
        return "You are not looged in!!"

@app.route('/logout',methods=['GET'])
def logout():
    email = session['email']
    session.pop('email',None)
    return redirect(url_for('index'))

#program runs from here
if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
