import os

import flask
from flask import Flask,request,json,render_template,session,redirect,url_for,escape,flash
from flask.ext.mysql import MySQL
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename

app = Flask(__name__)

mysql = MySQL()

#MySQL Configurations
try:
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'cutiepie07'
    app.config['MYSQL_DATABASE_DB'] = 'twitter_clone'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
except Exception as e:
    print "Error : ",e

def connect_to_mysql(query):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    return data

@app.route('/')
def home():
    if 'uid' in session:
        logged_in_user_id = session['uid']
        return redirect(url_for('wall'))
    else:
        return render_template('layout.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        _username = request.form['username']
        _email = request.form['email']
        _password = request.form['password']
        hash_password = sha256_crypt.encrypt(_password)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "SELECT email FROM users where email='" + _email + "'"
            cursor.execute(query)
            data = cursor.fetchall()
            print len(data)
            if len(data) == 0:
                insert_query = "INSERT INTO users(username,email,password) VALUES(%s,%s,%s)"
                print insert_query
                cursor.execute(insert_query,(_username,_email,hash_password))
                conn.commit()
                conn.close()
                return redirect(url_for('login'))
            else:
                flash("email already exists!!")
                return render_template('register.html')

        except Exception as e:
            pass
            print "error :",e
            return redirect(url_for('home'))
    else:
        return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        try:
            print "Session variable is:",session
            if ('uid' in session) and ('email' in session) and ('username' in session):
                print "User:",session['username']," is already logged in. Redirecting to profile page"
                uid = session['uid']
                return redirect(url_for('profile',uid=uid))
            else:
                return render_template('login.html')
        except Exception as e:
            print "Error occurred:",e
	    return redirect(url_for('home'))

    elif request.method == 'POST':
        if ('uid' in session) and ('email' in session) and ('username' in session):
            print "User:",session['username']," is already logged in. Redirecting to profile page"
            uid = session['uid']
            return redirect(url_for('profile',uid=uid))
        else:
            _email = request.form['email']
            _password = request.form['password']

            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                print str(_email)
                query = "SELECT * FROM users WHERE email = '" + _email + "'"
                print query
                cursor.execute(query)
                data = cursor.fetchone()
                conn.commit()
                conn.close()

            except Exception as e:
                print "Error entering in table:",e

            print len(data)
            if len(data) > 0:
                uid = data[0]
                username = data[1]
                email = data[2]
                password = data[3]
                print username,email

                try:
                    #verify password hash
                    if sha256_crypt.verify(request.form['password'],password):
                        session['logged_in'] = True
                        # User credentials are correct

                        # Delete old values from session
                        print "Logging out any user if he's already logged-in."
                        session.clear()

                        # Log the user in.
                        print "Logging in the user:", username
                        session['username'] = username
                        session['uid'] = uid
                        session['email'] = email
                        print "User:",username,"successfully logged-in. Redirecting to profile page."

                        return redirect(url_for('profile',uid=uid))
                    else:
                        flash('Invalid credentials, try again.')
                        return render_template('login.html')

                except Exception as e:
                    print "error : ",e
                    if email == _email and password == _password:
                        # Delete old values from session
                        print "Logging out any user if he's already logged-in."
                        session.clear()
                        # Log the user in.
                        print "Logging in the user:", username
                        session['username'] = username
                        session['uid'] = uid
                        session['email'] = email
                        print "User:",username,"successfully logged-in. Redirecting to profile page."
                        return redirect(url_for('profile',uid=uid))
                    else:
                        flash('Invalid credentials, try again.')
                        return render_template('login.html')
            else:
                flash('Please enter a valid email address')
                return render_template('login.html')

#function for opening users profile
@app.route('/profile/<uid>')
def profile(uid):
    followers = []
    followings =[]
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM users LEFT OUTER JOIN user_tweets ON users.uid = user_tweets.uid WHERE users.uid =" + str(uid) + " ORDER BY user_tweets.created_at DESC"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.commit()
        profile_pic = data[0][4]
        logged_in_user_id = session['uid']
        if str(uid) == str(logged_in_user_id):
            user_name = session['username']
            sql_query = "SELECT * FROM followers WHERE follower_id = %s or followed_id = %s " % (logged_in_user_id,logged_in_user_id)
            cursor.execute(sql_query)
            results = cursor.fetchall()
            conn.commit()
            conn.close()
            print results

            for result in results:
                if str(result[0]) == str(logged_in_user_id):
                    followings.append(result[1])
                else:
                    followers.append(result[0])

            return render_template('profile.html',username=user_name,profile_pic=profile_pic,tweets=data,uid=logged_in_user_id,followers_count=len(followers),followings_count=len(followings))
        else:
            conn = mysql.connect()
            cursor = conn.cursor()
            userid = str(data[0][0])
            username = str(data[0][1])
            sql_query = "SELECT * FROM followers WHERE follower_id = %s or followed_id = %s " % (userid,userid)
            cursor.execute(sql_query)
            results = cursor.fetchall()
            conn.commit()
            conn.close()

            for result in results:
                print result
                if str(result[0]) == str(userid):
                    followings.append(result[1])
                else:
                    followers.append(result[0])

            # find if this user is followed by logged_in_user
            if logged_in_user_id in followers:
                is_followed_by_logged_in_user = True
            else:
                is_followed_by_logged_in_user = False

            return render_template('another_profile.html',uid=userid,username=username,profile_pic=profile_pic,tweets=data,user_id=logged_in_user_id,is_followed=is_followed_by_logged_in_user,followers_count=len(followers),followings_count=len(followings))
    except Exception as e:
        print "Error : ",e
	return redirect(url_for('home'))

@app.route('/delete_tweet',methods=['POST'])
def delete_tweet():
    try:
        tid = request.form['tid']
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "DELETE FROM user_tweets WHERE t_id = %s" % str(tid)
        cursor.execute(query)
        conn.commit()
        conn.close()
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

def get_users_followed_by(uid):
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT followed_id FROM followers Where follower_id = %s" % str(uid)
    cursor.execute(query)
    data = cursor.fetchall()
    print "Query is :",query
    print "data from SQL is ",data
    return data

@app.route('/profile/<uid>/followers')
def followers(uid):
    following = []
    try:
        if 'uid' in session:
            logged_in_user_id = session['uid']
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "SELECT * FROM users INNER JOIN followers ON users.uid = followers.follower_id WHERE followers.followed_id = %s" % str(uid)
            print query
            cursor.execute(query)
            results = cursor.fetchall()
            print "results = ", results
            data = get_users_followed_by(logged_in_user_id)        # check followings of logged-in user
            conn.commit()
            conn.close()

            for result in results:
                for entry in data:
                    if entry[0] == result[0]:
                        following.append(entry[0])

            return render_template('followers.html',title= "Followers",uid=uid,users=results,followings=following,user_id=logged_in_user_id)

        else:
            return redirect(url_for('login'))
    except Exception as e:
        print "Error : ",e
        return redirect(url_for('profile',uid=uid))

@app.route('/profile/<uid>/following')
def following(uid):
    following = []
    try:
        if 'uid' in session:
            logged_in_user_id = session['uid']
            conn = mysql.connect()
            cursor = conn.cursor()
            query1 = "SELECT * FROM users INNER JOIN followers ON users.uid = followers.followed_id WHERE followers.follower_id = %s" % str(uid)
            cursor.execute(query1)
            results = cursor.fetchall()

            # These are the users that the Logged_in user is following
            data = get_users_followed_by(logged_in_user_id)

            conn.commit()
            conn.close()

            for result in results:
                for entry in data:
                    if entry[0] == result[0]:
                        following.append(entry[0])

            return render_template('followers.html',title= 'Following',uid=uid,users=results,followings=following,user_id=logged_in_user_id)

        else:
            redirect(url_for('login'))
    except Exception as e:
        print "Error : ",e
        return redirect(url_for('profile',uid=uid))

@app.route('/follow',methods=['POST'])
def follow():
    uid = request.form['uid']
    print uid
    print session['uid']
    try:
        if 'uid' in session:
            if str(uid) != str(session['uid']):
                conn = mysql.connect()
                cursor = conn.cursor()
                query = "INSERT INTO followers(follower_id,followed_id) VALUES(%s,%s)"
                print query
                cursor.execute(query,(str(session['uid']),str(uid)))
                conn.commit()
                conn.close()
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
            query = "DELETE FROM followers WHERE followed_id = %s" % str(uid)
            print query
            cursor.execute(query)
            conn.commit()
            conn.close()
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

@app.route('/home')
def wall():
    try:
        if 'uid' in session:
            logged_in_user_id = session['uid']
            conn = mysql.connect()
            cursor = conn.cursor()
            query1 = "SELECT * FROM (SELECT user_tweets.uid,users.username,users.profile_pic,user_tweets.tweet,user_tweets.created_at FROM user_tweets INNER JOIN followers ON user_tweets.uid=followers.followed_id INNER JOIN users ON users.uid = user_tweets.uid WHERE followers.follower_id=%s) AS home_table ORDER BY created_at DESC;" % str(logged_in_user_id)
            cursor.execute(query1)
            data = cursor.fetchall()
            query2 = "SELECT * from users WHERE uid=%s" % str(logged_in_user_id)
            cursor.execute(query2)
            user_detail = cursor.fetchone()
            conn.commit()
            print user_detail
            conn.close()
            return render_template('wall.html',users=data,user_detail=user_detail,uid=logged_in_user_id)
        else:
            print "redirect url to login"
            return redirect(url_for('home'))
    except Exception as e:
        print "error: ",e
        return redirect(url_for('home'))


# For upload profile pic
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif','.JPG']

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if 'uid' in session:
        logged_in_user_id = session['uid']
        try:
            if request.method == 'POST':
                file = request.files['photo']
                extension = os.path.splitext(file.filename)[1]

                if file and extension in ALLOWED_EXTENSIONS:
                    filename = str(logged_in_user_id) + extension                               # filename should be uid + extension
                    filename = secure_filename(filename)

                    try:
                        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
                        file.save(os.path.join(UPLOAD_FOLDER, filename))
                        print "Image uploaded:", filename
                        photo = 'uploads/' + filename
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        query = "UPDATE users SET profile_pic = %s WHERE uid = %s"
                        cursor.execute(query, (photo, str(logged_in_user_id)))
                        conn.commit()
                        conn.close()

                        respStr = json.dumps({'message': 'success'})
                        resp = flask.Response(respStr)
                        resp.headers['Content-Type'] = 'application/json'
                        return resp
                    except Exception as e:
                        print e

                else:
                    respStr = json.dumps({'message':'failure'})
                    resp = flask.Response(respStr)
                    resp.headers['Content-Type'] = 'application/json'
                    return resp
                    print "error: image format should be png,jpg,jpeg,gif"
            else:
                return redirect(url_for('profile',uid=logged_in_user_id))
        except Exception as e:
            print e

#shows list of all the registered users on the app
@app.route('/users')
def find_user():
    following = []
    try:
        if 'uid' in session:
            logged_in_user_id = session['uid']
            conn = mysql.connect()
            cursor = conn.cursor()
            query1 ="SELECT  * FROM users LEFT OUTER JOIN followers ON users.uid = followers.followed_id WHERE users.uid <> %s" % str(logged_in_user_id)
            # group by finds unique row in table
            cursor.execute(query1)
            results = cursor.fetchall()
            data = get_users_followed_by(logged_in_user_id)
            conn.commit()
            conn.close()

            for result in results:
                for entry in data:
                    if entry[0] == result[0]:
                        following.append(entry[0])
            return render_template('users.html',uid=logged_in_user_id,users=results,followings=following)

        else:
            print "redirecting to login"
            return redirect(url_for('home'))
    except Exception as e:
        print "error :",e
        return redirect(url_for('home'))

#inserting tweets into user table
@app.route('/tweet',methods=["POST"])
def add_tweet():
    _tweet = request.form['input_tweet']
    if 'uid' in session:
        logged_in_user_id = session['uid']
        if len(_tweet) == 0:
            return redirect(url_for('profile',uid=logged_in_user_id))
        else:
            try:
                conn = mysql.connect()                                                                  # connecting to mysql
                cursor = conn.cursor()
                query = "INSERT INTO user_tweets(uid,tweet) VALUES(%s,%s)"
                cursor.execute(query,(str(logged_in_user_id),_tweet))
                data = cursor.fetchall()
                conn.commit()
                conn.close()
                print data

                if len(data) == 0:
                    return redirect(url_for('profile',uid=logged_in_user_id))
                else:
                    return json.dumps({'error':str(data[0])})
            except Exception as e:
                print "Error : ",e
                return redirect(url_for('profile',uid=logged_in_user_id))


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
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
