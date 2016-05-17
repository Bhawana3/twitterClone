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

from flask import Flask,request,json,render_template,session,redirect,url_for,escape,flash
from flask.ext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

#MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cutiepie07'
app.config['MYSQL_DATABASE_DB'] = 'twitter_clone'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def convert_date(date_string):          #input date in 09-07-2013 returns date in July 09,2013
    import datetime
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    return date.strftime('%b %d,%Y')

@app.route('/')
def home():
    return render_template('layout.html')

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
def signup():
    _username = request.form['username']
    _email = request.form['email']
    _password = request.form['password']

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT email FROM users where email='" + _email + "'"
        cursor.execute(query)
        data = cursor.fetchall()
        print len(data)
        if len(data) == 0:
            insert_query = "INSERT INTO users(username,email,password) VALUES('" + _username + "','" + _email + "','" + _password  + "')"
            print insert_query
            cursor.execute(insert_query)
            conn.commit()
            return redirect(url_for('log_in'))
        else:
            flash("email already exists!!")
            return redirect(url_for('sign_up'))

    except Exception as e:
        pass
        print "error :",e

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
        uid = data[0][0]
        username = data[0][1]
        email = data[0][2]
        password = data[0][3]
        print username,email
        try:
            if (email == _email) and (password == _password):
                session['username'] = username
                session['email'] = email
                session['uid'] = uid
                flash('Logged in successfully')
                return redirect(url_for('profile'))
            else:
                flash('Invalid email/password combination')
                return redirect(url_for('log_in'))
        except Exception as e:
            print "Error:",e
    else:
        flash('Please enter a valid email address')
        return redirect(url_for('log_in'))

# user profile
@app.route('/profile',methods=['GET'])
def profile():
    if 'uid' in session:
        uid = session['uid']
        username = session['username']
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT tweet,created_at FROM tweets WHERE uid ='" + str(uid) + "'" + "ORDER BY created_at DESC"
        cursor.execute(query)
        tweets = cursor.fetchall()
        conn.commit()

        return render_template('profile.html',username=username,tweets=tweets)
    else:
        return redirect(url_for('home'))

#inserting tweets into user table
@app.route('/tweet',methods=["POST"])
def add_tweet():
    _tweet = request.form['input_tweet']
    if 'uid' in session:
        uid = session['uid']
        email = session['email']
        print uid,email
        if len(_tweet) == 0:
            return redirect(url_for('profile'))
        else:
            conn = mysql.connect()                                                                  # connecting to mysql
            cursor = conn.cursor()
            query = "INSERT INTO tweets(uid,user_email,tweet) VALUES('" + str(uid) + "','" + email + "','" + _tweet + "')"
            cursor.execute(query)
            data = cursor.fetchall()
            print data

            if len(data) == 0:
                conn.commit()
                return redirect(url_for('profile'))
            else:
                return json.dumps({'error':str(data[0])})

@app.route('/logout',methods=['GET'])
def logout():
    try:
        email = session['email']
        session.pop('email',None)
        return redirect(url_for('home'))
    except Exception as e:
        pass

#program runs from here
if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
