#!/usr/bin/python3
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import psycopg2
import json

app = Flask(__name__)  
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a strong, unique secret key

# Database Configuration
DB_NAME = "profiler_users_db"
DB_USER = "profiler"
DB_PASSWORD = "profiler"
DB_HOST = "localhost"

#keys to access various data from the json object
# completeDataKey=['basicDataKey','educationDataKey','workExperienceDataKey','masterThesisDataKey','courseProjectDataKey','certificationsDataKey','achievementsDataKey','technicalSkillsDataKey','extraCurricularDataKey','hobbiesDataKey']
basicDataKey=['name', 'rollNumber', 'departmentName', 'programName', 'gender']
educationDataKey=['exam','univ','insti','yop','cpi']
workExperienceDataKey=["workDesignation","workOrganisation","workRole","workProject","workProjectResponsibilities","workDate"]
masterThesisDataKey=['projectTitle','projectName','projectDescription','projectGuide','projectCurrentWork','projectFutureWork','projectDate']
courseProjectDataKey=['courseProjectTitle','courseProjectNameAndCode','courseProjectInstructorName','courseProjectDescription','courseProjectDate']
certificationsDataKey=['certificationTitle','certifcationOfferedBy','certificationPlatform','certificationDate']
achievementsDataKey=['achievements']
technicalSkillsDataKey=['technicalSkills']
extraCurricularDataKey=['extraCurricular']
hobbiesDataKey=['hobbies']

######### method to get the db connection obj
def connect_to_db():
    return psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

######### method for getting details
@app.route('/details',methods=['GET','POST'])
def details():
    error=None
    if request.method == 'POST':
        # connecting to database
        connection=connect_to_db()
        cursor=connection.cursor()

        # get the current user_id 
        user_id=session['user_id']

        # get details from the html form as JSON object and convert it as Dict
        completeUserData=request.json['completeData']   

        # get the basic data 
        basicData=completeUserData['basicData']
        
        
        # prepare data to be inserted into the table
        data1="nothing here"
        ############# ADD MORE HERE #############
        query=f"INSERT INTO usersdata SET eduDetails='{data1}' WHERE id='{user_id}'"

        # insert and commit the changes in the database
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"status": "success"})

    return render_template('details.html',error="none")


######### method to handle secure logins
@app.route('/login',methods=['GET','POST']) 
def login():
    error=None
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']

        conn = connect_to_db()  #connecting to DB
        cur = conn.cursor()
        query=f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'"
        cur.execute(query)
        user_id = cur.fetchone()   #fetching the query results
        conn.close() #closing the connection

        if  not user_id:
            error='Invalid Credentials'
        else:
            # Store the user's username in the session
            session['user_id'] = user_id
            return render_template('details.html',error="none")
    return render_template('login.html',error=error)


######### method to register new users
@app.route('/register',methods=['GET','POST']) 
def register():
    error=None
    if request.method == 'POST':
        conn=connect_to_db()
        cur = conn.cursor()
        #username and password from the form
        username=request.form['username']    
        upass=request.form['password']

        cur.execute(f"SELECT id FROM users WHERE username = '{username}'")
        user_exist = cur.fetchone()   
        #checking if the entered username is available or not
        if(user_exist): 
            error='username taken'
        elif (upass != request.form['retypepassword']):
            error='password didn\'t match'
        #add the username and password into the users table
        else:
            cur.execute("INSERT INTO users(username,password) VALUES( %s, %s)", (username,upass)) #executing query
            conn.commit()
            cur.close()
            conn.close()
            return render_template('login.html',error="registration successful.")

    return render_template('register.html',error=error)


######### method to logout the current user
@app.route('/logout')  
def logout():  
    if request.method == 'POST':
        # Clear the session to log the user out
        print(session.pop('user_id', None),"has logged out!")
        return render_template('index.html')  


######### root method 
@app.route('/')  
def index():  
    return render_template('index.html')  

######### calling main method
if __name__ == '__main__':  
    app.run(debug=True)  

# def updateDB(id,