#!/usr/bin/python3
from flask import Flask, render_template, redirect, url_for, request, session
import psycopg2

app = Flask(__name__)  
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a strong, unique secret key

# Database Configuration
DB_NAME = "profiler_users_db"
DB_USER = "profiler"
DB_PASSWORD = "profiler"
DB_HOST = "localhost"

def connect_to_db():
    return psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

#user_creds={'admin':'admin'}        #users creds. currently stored in dict.

######### method for basic details
@app.route('/basic_details',methods=['GET','POST'])
def basic_details():
    error=None
    if request.method == 'POST':
        name=request.form['name']
        roll=request.form['roll']
        department=request.form['department']
        program=request.form['program']
        year=request.form['year']

        print(name,roll,department,program,year)
    return 'nicely done basicd_etails'


######### method for educational details
@app.route('/edu_details',methods=['GET','POST'])
def edu_details():
    return 'nicely done edu_details'


######### method to handle secure logins
@app.route('/login',methods=['GET','POST']) 
def login():
    error=None
    if request.method == 'POST':
        uname=request.form['username']
        upassword=request.form['password']

        conn = connect_to_db()  #connecting to DB
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM users WHERE username = '{uname}' AND password = '{upassword}'")
        user_id = cur.fetchone()   #fetching the query results
        conn.close() #closing the connection

        if  not user_id:
            error='Invalid Credentials'
        else:
            # Store the user's username in the session
            session['username'] = uname
            return render_template('basic_details.html',error="none")
    return render_template('login.html',error=error)


######### method to register new users
@app.route('/register',methods=['GET','POST']) 
def register():
    error=None
    if request.method == 'POST':
        conn=connect_to_db()
        cur = conn.cursor()
        #username and password from the form
        uname=request.form['username']    
        upass=request.form['password']

        cur.execute(f"SELECT id FROM users WHERE username = '{uname}'")
        user_exist = cur.fetchone()   
        #checking if the entered username is available or not
        if(user_exist): 
            error='username taken'
        elif (upass != request.form['retypepassword']):
            error='password didn\'t match'
        #add the username and password into the users table
        else:
            cur.execute("INSERT INTO users(username,password) VALUES( %s, %s)", (uname,upass)) #executing query
            conn.commit()
            cur.close()
            conn.close()
            return render_template('login.html',error="registration successful.")

    return render_template('register.html',error=error)


######### method to logout the current user
@app.route('/logout')  
def logout():  
    # Clear the session to log the user out
    print(session.pop('username', None),"has logged out!")
    return render_template('index.html')  


######### root method 
@app.route('/')  
def index():  
    return render_template('index.html')  

######### calling main method
if __name__ == '__main__':  
    app.run(debug=True)  

