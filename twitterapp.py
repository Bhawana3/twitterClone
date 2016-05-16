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

mysql = MySQL()

#MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cutiepie07'
app.config['MYSQL_DATABASE_DB'] = 'twitter_clone'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def home():
    return render_template('write_tweet.html')

@app.route('/#')
def index():
    if session.get('logged_in') == True:
        return 'You are logged in'
    return 'Please login again!!'

@app.route('/signup/')
def sign_up():
    try:
        return render_template('register.html')
    except Exception as e:
        print "error: ",e

@app.route('/login/')
def log_in():
    try:
        return render_template('login.html')
    except Exception as e:
        print "Error: ",e

@app.route('/user/signup',methods=['POST'])
def signUp():
    _username = request.form['username']
    _email = request.form['email']
    _password = request.form['password']

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('register',(_username,_email,_password))              #calls procedure register
        data = cursor.fetchall()
        print data
    except Exception as e:
        print "error :",e

    if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})


@app.route('/user/login',methods=['POST'])
def login():
    _email = request.form['email']
    _password = request.form['password']

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE email=" + "'" + _email + "'"
        cursor.execute(query)
        data = cursor.fetchall()

    except Exception as e:
        print "Error entering in table:",e

    if len(data) == 1:
        username = data[0][1]
        email = data[0][2]
        password = data[0][3]
        print username,email
        try:
            if (email == _email) and (password == _password):
                session['username'] = username
                session['email'] = email
                print 'User Logged in successfully!!'
                return redirect(url_for('profile'))
            else:
                return "Please enter a valid email and password"
        except Exception as e:
            print "Error:",e
    else:
        return json.dumps({'error':str(data[0])})

#inserting tweets into user table
@app.route('/tweet',methods=["POST"])
def insert_into_db():
    _username = request.form['input_user']
    _tweet = request.form['input_tweet']

    try:
        conn = mysql.connect()                                                                  # connecting to mysql
        cursor = conn.cursor()
        query = "INSERT INTO user_tweets(username,tweet) VALUES(" + "'" + _username + "','" + _tweet + "')"              #_username = string containing username of the current user
        cursor.execute(query)
        data = cursor.fetchall()
    except Exception as e:
        print "Error entering in table"

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
        print json.dumps({'tweets:': tweet})
        return render_template('profile.html',username=username)
    else:
        return "You are not logged in!!"

@app.route('/logout',methods=['GET'])
def logout():
    try:
        email = session['email']
        session.pop('email',None)
        return redirect(url_for('index'))
    except Exception as e:
        return "You are not logged in!!"

#program runs from here
if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
