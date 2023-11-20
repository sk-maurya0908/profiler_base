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

######### method to get the db connection obj
def connect_to_db():
    return psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

######### method for basic details
@app.route('/basic_details',methods=['GET','POST'])
def basic_details():
    error=None
    if request.method == 'POST':
        # connecting to database
        connection=connect_to_db()
        cursor=connection.cursor()

        # get the current username 
        username=session['username']

        # get details from the html form
        name=request.form['name']
        roll=request.form['roll']
        department=request.form['department']
        program=request.form['program']
        year=request.form['year']

        # prepare data to be inserted into the table
        data=name+"#"+roll+"#"+department+"#"+program+"#"+year
        query=f"INSERT INTO usersdata(username,basicDetails) VALUES('{username}','{data}') ON CONFLICT (username) DO UPDATE SET basicDetails='{data}'"

        # insert and commit the changes in the database
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

        return render_template('edu_details.html',error="none")

    return render_template('basic_details.html',error=error)


######### method for educational details
@app.route('/edu_details',methods=['GET','POST'])
def edu_details():
    error=None
    if request.method == 'POST':
        # connecting to database
        connection=connect_to_db()
        cursor=connection.cursor()

        # get the current username 
        username=session['username']

        # get details from the html form
        highschool_name=request.form['highschool_name']
        highschool_start_year =request.form['highschool_start_year']
        highschool_finish_year=request.form['highschool_finish_year']
        highschool_percentage =request.form['highschool_percentage']
        seniorsecondary_name  =request.form['seniorsecondary_name']
        seniorsecondary_start_year=request.form['seniorsecondary_start_year']
        seniorsecondary_finish_year=request.form['seniorsecondary_finish_year']
        seniorsecondary_percentage=request.form['seniorsecondary_percentage']
        higher_education_name=request.form['higher_education_name']
        higher_education_program=request.form['higher_education_program']
        higher_education_start_year=request.form['higher_education_start_year']
        higher_education_finish_year=request.form['higher_education_finish_year']
        higher_education_department=request.form['higher_education_department']
        higher_education_percentage=request.form['higher_education_percentage']

        # prepare data to be inserted into the table
        data="#"+highschool_name+"#"+highschool_start_year+"#"+highschool_finish_year+"#"+highschool_percentage+"#"+seniorsecondary_name+"#"+seniorsecondary_start_year+"#"+seniorsecondary_finish_year+"#"+seniorsecondary_percentage
        data1=data+"#"+higher_education_name+"#"+higher_education_program+"#"+higher_education_start_year+"#"+higher_education_finish_year+"#"+higher_education_department+"#"+higher_education_percentage
        query=f"UPDATE usersdata SET eduDetails='{data1}' WHERE username='{username}'"

        # insert and commit the changes in the database
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        return "educational details added."

    return render_template('edu_details.html',error="none")


######### method to handle secure logins
@app.route('/login',methods=['GET','POST']) 
def login():
    error=None
    if request.method == 'POST':
        uname=request.form['username']
        upassword=request.form['password']

        conn = connect_to_db()  #connecting to DB
        cur = conn.cursor()
        query=f"SELECT id FROM users WHERE username = '{uname}' AND password = '{upassword}'"
        cur.execute(query)
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

