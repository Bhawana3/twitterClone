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
import flask
from flask import Flask,request,json,render_template,session,redirect,url_for,escape,flash
from flask.ext.mysql import MySQL
import os
app = Flask(__name__)

mysql = MySQL()

#PORT = os.getenv('PORT')

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

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
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
                return redirect(url_for('login'))
            else:
                flash("email already exists!!")
                return render_template('register.html')

        except Exception as e:
            pass
            print "error :",e

    else:
        return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        try:
            print "Session variable is:",session
            if ('uid' in session) and ('email' in session) and ('username' in session):
                print "User:",session['username']," is already logged in. Redirecting to profile page"
                return redirect(url_for('profile'))
            else:
                return render_template('login.html')
        except Exception as e:
            print "Error occurred:",e

    elif request.method == 'POST':
        if ('uid' in session) and ('email' in session) and ('username' in session):
            print "User:",session['username']," is already logged in. Redirecting to profile page"
            return redirect(url_for('profile'))
        else:
            _email = request.form['email']
            _password = request.form['password']

            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                query = "SELECT * FROM users WHERE email=" + "'" + _email + "' and password='" + _password + "'"
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
                        # User credentials are correct

                        # Delete old values from session
                        print "Logging out any user if he's already logged-in."
                        session.clear()

                        # Log the user in.
                        print "Logging in the user:", username
                        session['username'] = username
                        session['uid'] = uid
                        session['email'] = email
                        #flash('Logged in successfully')


                        print "User:",username,"successfully logged-in. Redirecting to profile page."
                        return redirect(url_for('profile'))
                    else:
                        flash('Invalid email/password combination')
                        return render_template('login.html')
                except Exception as e:
                    print "Error:",e
            else:
                flash('Please enter a valid email address')
                return render_template('login.html')

@app.route('/home')
def wall():
    try:
        if 'uid' in session:
            uid = session['uid']
            conn = mysql.connect()
            cursor = conn.cursor()
            query1 = "SELECT * FROM (SELECT user_tweets.uid,users.username,users.profile_pic,user_tweets.tweet,user_tweets.created_at FROM user_tweets INNER JOIN followers ON user_tweets.uid=followers.followed_id INNER JOIN users ON users.uid = user_tweets.uid WHERE followers.follower_id=" + str(uid) + ") AS home_table ORDER BY created_at DESC;"
            cursor.execute(query1)
            data = cursor.fetchall()
            query2 = "SELECT * from users WHERE uid=" + str(uid)
            cursor.execute(query2)
            user_detail = cursor.fetchone()
            conn.commit()
            print user_detail
            return render_template('wall.html',users=data,user_detail=user_detail)
        else:
            return redirect(url_for('login'))
    except Exception as e:
        print "error: ",e

# user profile
@app.route('/profile',methods=['GET'])
def profile():
    try:
        if 'uid' in session:
            uid = session['uid']
            username = session['username']
            print username
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "SELECT * FROM users LEFT OUTER JOIN user_tweets ON users.uid = user_tweets.uid WHERE users.uid = " + str(uid) + " ORDER BY user_tweets.created_at DESC"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.commit()
            return render_template('profile.html',username=username,tweets=data)
        else:
            return redirect(url_for('home'))
    except Exception as e:
        print "error : ",e
        return redirect(url_for('home'))

# For upload profile pic
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif','.JPG']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if 'uid' in session:
        uid = session['uid']
        try:
            if request.method == 'POST':
                file = request.files['photo']
                extension = os.path.splitext(file.filename)[1]
                if extension in ALLOWED_EXTENSIONS:
                    filename = str(uid) + extension                               # filename should be uid + extension
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    print "Image uploaded:",filename
                    photo = 'uploads/'+filename
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "UPDATE users SET profile_pic = '" + photo + "' WHERE uid = " + str(uid) + ";"
                    print query
                    cursor.execute(query)
                    conn.commit()
                    return redirect(url_for('profile'))
                else:
                    print "error: image format should be png,jpg,jpeg,gif"
            else:
                return render_template('index.html')
        except Exception as e:
            print e

#returns list of followers
@app.route('/followers')
def followers():
    following = []
    if 'uid' in session:
        uid = session['uid']
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM users INNER JOIN followers ON users.uid = followers.follower_id WHERE followers.followed_id = " + str(uid)
        cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()
        for result in results:
            if result[5] == uid:
                following.append(int(result[6]))
        return render_template('users.html',users=results,followings=following)

#returns list of followings
@app.route('/following')
def following():
    if 'uid' in session:
        uid = session['uid']
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM users INNER JOIN followers ON users.uid = followers.followed_id WHERE followers.follower_id = " + str(uid)
        cursor.execute(query)
        data = cursor.fetchall()
        conn.commit()
        return render_template("followers.html",users=data)

#shows list of all the registered users on the app
@app.route('/users')
def find_user():
    following = []
    try:
        if 'uid' in session:
            uid = session['uid']
            conn = mysql.connect()
            cursor = conn.cursor()
            query ="SELECT  * FROM users LEFT OUTER JOIN followers ON users.uid = followers.followed_id WHERE users.uid <> " + str(uid) + " GROUP BY users.uid"
            # group by finds unique row in table
            print query
            cursor.execute(query)
            results = cursor.fetchall()
            conn.commit()
            for result in results:
                if result[5] == uid:
                    following.append(result[6])
            print following
            return render_template('users.html',users=results,followings=following)
        else:
            return redirect(url_for('home'))
    except Exception as e:
        print "error :",e
        return redirect(url_for('home'))

@app.route('/follow',methods=['POST'])
def follow():
    uid = request.form['uid']
    try:
        if 'uid' in session:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "INSERT INTO followers(follower_id,followed_id) VALUES('" + str(session['uid']) + "','" + str(uid) + "')"
            cursor.execute(query)
            conn.commit()
            respStr = json.dumps({'message':'success'})
            resp = flask.Response(respStr)
            resp.headers['Content-Type'] = 'application/json'
            return resp
    except Exception as e:
        print e
        respStr = json.dumps({'message':'failure'})
        resp = flask.Response(respStr)
        resp.headers['Content-Type'] = 'application/json'
        return resp

@app.route('/unfollow',methods=['POST'])
def unfollow():
    uid = request.form['uid']
    try:
        if 'uid' in session:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "DELETE FROM followers WHERE followed_id=" + str(uid)
            cursor.execute(query)
            conn.commit()
            respStr = json.dumps({'message':'success'})
            resp = flask.Response(respStr)
            resp.headers['Content-Type'] = 'application/json'
            return resp
    except Exception as e:
        print e
        respStr = json.dumps({'message':'failure'})
        resp = flask.Response(respStr)
        resp.headers['Content-Type'] = 'application/json'
        return resp

#inserting tweets into user table
@app.route('/tweet',methods=["POST"])
def add_tweet():
    _tweet = request.form['input_tweet']
    if 'uid' in session:
        uid = session['uid']
        print uid
        if len(_tweet) == 0:
            return redirect(url_for('profile'))
        else:
            conn = mysql.connect()                                                                  # connecting to mysql
            cursor = conn.cursor()
            query = "INSERT INTO user_tweets(uid,tweet) VALUES('" + str(uid) + "','" + _tweet + "')"
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
    session.pop('uid',None)
    session.pop('email',None)
    session.pop('username',None)
    # Delete any other keys in session, if any
    session.clear()
    print 'deleted session: ', session
    return render_template('logout.html')


#program runs from here
if __name__ == "__main__":
    #print "Starting on port:",PORT
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
    #port=PORT)
