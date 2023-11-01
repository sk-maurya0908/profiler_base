#!/usr/bin/python3
from flask import Flask, render_template, redirect, url_for, request, session
  
app = Flask(__name__)  
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a strong, unique secret key

user_creds={'admin':'admin'}        #users creds. currently stored in dict.

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
    return 'nicly done basicd_etails'


######### method for educational details
@app.route('/edu_details',methods=['GET','POST'])
def edu_details():
    return 'nicly done edu_details'


######### method to handle secure logins
@app.route('/login',methods=['GET','POST']) 
def login():
    error=None
    if request.method == 'POST':
        uname=request.form['username']
        if  uname not in user_creds or request.form['password'] !=user_creds[uname]:
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
        uname=request.form['username']
        upass=request.form['setpassword']
        if  uname in user_creds :                       ########### check is username already present
            error='username taken'
        elif (upass != request.form['retypepassword']): ########### check for username
            error='both passwords should be same'
        else:
            user_creds[uname]=upass
            return render_template('login.html',error=None)
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

