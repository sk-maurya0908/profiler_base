#!/usr/bin/python3
from flask import Flask, render_template, redirect, url_for, request, session
import json
from user_management import User

app = Flask(__name__)  
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a strong, unique secret key
user=User(None,None)
######### route for getting details
@app.route('/details',methods=['GET','POST'])
def details():
    error=None
    if request.method == 'POST':
        # get all details from the html form as JSON object and convert it Dict
        resumeData=request.json['completeData']   
        # get the current user_id 
        user_id=session['user_id']
        # print("user_id=session['user_id']*********************************",user_id)
        #insert into db
        user.resumeDataInit(resumeData)
        user.insert_userdata_in_db(user_id)

        error="success"

    return render_template('details.html',error="none")


######### route to handle secure logins
@app.route('/login',methods=['GET','POST']) 
def login():
    error=None
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        #init the user obj
        user=User(username,password)    
        # validating user's credentials
        # print("fe--tchone*************************")
        
        user_id=user.validate_user()
        # print("fe-----------------------tchone*************************")
        
        if user_id == -1:
            error='Invalid Credentials'
        else:
            # Store the user_id in the session
            session['user_id'] = user_id
            return render_template('details.html',error="none")

    return render_template('login.html',error=error)

######### route to register new users
@app.route('/register',methods=['GET','POST']) 
def register():
    error=None
    if request.method == 'POST':
        #username and password from the form
        username=request.form['username']    
        password=request.form['password']
        if (password != request.form['retypepassword']):
            error='password didn\'t match'
        else:
            user=User(username,password)
            if user.registration():
                error = "registration failed"
            else:
                return render_template('login.html',error="registration successful.")

    return render_template('register.html',error=error)


######### method to logout the current user
@app.route('/logout')  
def logout():  
    if request.method == 'POST':
        # Clear the session to log the user out
        print(session.pop('user_id', None),"has logged out!")
        return render_template('index.html')  


######### Route to download the generated PDF resume
@app.route('/download_resume', methods=['GET'])
def download_resume():
    if 'user' in session:
        #get user data from database
        # user get the users data from the db
        mapping_path = 'data_mapping.json'
        template_path = 'template/SWL_RESUME_TEMPLATE.tex'

        # Generate LaTeX resume
        latex_resume = user.generate_latex_resume(template_path, mapping_path)

        # Convert LaTeX to PDF
        output_path = f'temp_resume_{user.email}'
        convert_latex_to_pdf(latex_resume, output_path)

        # Serve the PDF
        with open(f'{output_path}.pdf', 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        # Set up a response to serve the PDF
        response = Response(pdf_data, content_type='application/pdf')
        response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'
        return response
    return redirect(url_for('login'))


######### root method 
@app.route('/')  
def index():  
    return render_template('index.html')  

######### calling main method
if __name__ == '__main__':  
    app.run(debug=True)  

