#!/usr/bin/python3
from flask import Flask, render_template, redirect, url_for, request, session
  
app = Flask(__name__)  
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a strong, unique secret key

user_creds={'admin':'admin'}
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
            return render_template('filldetail.html',error="none")
    return render_template('login.html',error=error)

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

@app.route('/logout')  
def logout():  
    # Clear the session to log the user out
    print(session.pop('username', None),"has logged out!")
    return render_template('index.html')  

@app.route('/')  
def index():  
    return render_template('index.html')  

if __name__ == '__main__':  
    app.run(debug=True)  

