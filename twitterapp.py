"""
DELIMITER $$
CREATE
DEFINER=`root`@`localhost`
PROCEDURE `create_user`(IN _name VARCHAR(50),IN _username VARCHAR(50),IN _password VARCHAR(20))
BEGIN
    if ( select exists (select 1 from user_table where user_username = _username) ) THEN
        select 'Username Already Exists !!';
    ELSE
        insert into user_table (user_name,user_username,user_password) values (_name,_username,_password);
    END IF;
END$$
DELIMITER ;
"""

from flask import Flask,request,json,render_template
from flask.ext.mysql import MySQL

app = Flask(__name__)

@app.route('/')
def writeTweet():
    return render_template('write_tweet.html')

@app.route('/signup/')
def sign_up():
    return render_template('signup.html')

mysql = MySQL()

#MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '****'
app.config['MYSQL_DATABASE_DB'] = 'twitter_clone'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/user/signup',methods=['POST'])
def signUp():
    _username = request.form['input_user']
    _email = request.form['input_email']
    _password = request.form['input_password']

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('create_user',(_username,_email,_password))              #calls procedure createUser
    data = cursor.fetchall()

    if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
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

    if len(data) == 0:
        conn.commit()
        return json.dumps({'message':'Tweet added successfully!'})
    else:
        return json.dumps({'error':str(data[0])})

# user profile
@app.route('/profile',methods=["POST"])
def user_profile():
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT tweet,created_at FROM user_tweets WHERE username ='bhawana' ORDER BY created_at DESC"
    cursor.execute(query)
    tweet = cursor.fetchall()
    return json.dumps({'tweets:': tweet})
    conn.commit()


#program runs from here
if __name__ == "__main__":
    app.run()
