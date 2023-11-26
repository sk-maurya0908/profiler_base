import hashlib
import psycopg2
import json, subprocess, os

def convert_latex_to_pdf(latex_content, output_path='temp_resume'):
    # Creating temporary directory
    temp_dir = os.path.join(os.getcwd(), 'temp_latex')  
    os.makedirs(temp_dir, exist_ok=True)

    latex_file_path = os.path.join(temp_dir, 'resumeData.tex')
    pdf_file_path = os.path.join(temp_dir, 'resumeData.pdf')

    try:
        # Write LaTeX content to a file
        with open(latex_file_path, 'w') as latex_file:
            latex_file.write(latex_content)

        # Run pdflatex to convert LaTeX to PDF
        subprocess.run(['pdflatex', '-output-directory', temp_dir, latex_file_path])

        # Move the PDF file to the desired output path
        os.rename(pdf_file_path, f'{output_path}.pdf')

        # Clean up temporary files and directory
        os.remove(latex_file_path)
        os.remove(os.path.join(temp_dir, 'resumeData.log'))
    except Exception as e:
        print(f"Error converting LaTeX to PDF: {e}")
    finally:
        # Remove the temporary directory
        os.rmdir(temp_dir)


escapeDict = {'&':'\&', '%':'\%', '$':'\$', '#':'\#', '_':'\_', '{':'\{', '}':'\}', 
'~':'\\textasciitilde', '^':'\\textasciicircum', '\\':'\\textbackslash'}
def escape_special_chars(dataString):
    escapedString = dataString.translate(str.maketrans(escapeDict))
    return escapedString

######### method to get the db connection obj
def connect_to_db():
    return psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

######### method to get the hash of the plain password
def hash_password(password):
    return password
    # Create a new SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the password encoded as bytes
    sha256.update(password.encode('utf-8'))

    # return the hexadecimal representation of the hash
    return sha256.hexdigest()


# Database Configuration
DB_NAME = "profiler_users_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"

#keys to access various data from the json object
# resumeDataKey=['basicDataKey','educationDataKey','workExperienceDataKey','masterThesisDataKey','courseProjectDataKey','certificationsDataKey','achievementsDataKey','technicalSkillsDataKey','extraCurricularDataKey','hobbiesDataKey']
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

    
class User:
    ######### method to insert user's data into database
    def validate_user(self):
        connection = connect_to_db()  #connecting to DB
        cursor = connection.cursor()
        query=f"SELECT user_id FROM users WHERE username = '{self.username}' AND password = '{self.password}'"
        cursor.execute(query)
        user_id = cursor.fetchone()   #fetching the query results
        # print("fe-----------------------tchone*************************",user_id)
        cursor.close()
        connection.close()               #closing the connection

        if not user_id:
            return -1
        return user_id

    ######### method to insert user's data into database
    def insert_userdata_in_db(self, user_id):
        # connecting to database
        connection=connect_to_db()
        cursor=connection.cursor()

        # get the basic data 
        basicData=self.resumeData['basicData']
        # prepare data to be inserted into the table
        columnName = ','.join([x for x in basicDataKey])
        data = '\',\''.join([basicData[0][x] for x in basicDataKey])
        # print(self.resumeData)
        try:
            # print(user_id)
            # print(data)
            query=f"INSERT INTO basicData(user_id,{columnName}) VALUES({user_id},\'{data}\')"
            # insert and commit the changes in the database
            cursor.execute(query)
            connection.commit()
        except Exception as e:
            # print("error *******************")
            connection.rollback()  # Rollback the changes if an exception occurs
            print(f"error {e} occured")
            return False
        finally:
            cursor.close()
            connection.close()
        return True
        
    ######### method to get user's data from database
    def get_userdata_from_db(self, user_id):
        # connecting to database
        connection=connect_to_db()
        cursor=connection.cursor()
        # to be done
        return True

    def registration(self):
        try:
            connection=connect_to_db()
            cursor = connection.cursor()
            
            query=f"SELECT user_id FROM users WHERE username = '{self.username}'"
            cursor.execute(query)
            user_exist = cursor.fetchone()   

            #checking if the entered username is available or not
            if(user_exist): 
                cursor.close()
                connection.close()
                return False
            else:
                hashed_password=hash_password(self.password)
                #add the username and password into the users table
                print(self.username, self.password)
                query=f"INSERT INTO users(username,password) VALUES('{self.username}','{hashed_password}')"
                cursor.execute(query) #executing query
                connection.commit()
                cursor.close()
                connection.close()

        except Exception as e:
            # print("error *******************")
            connection.rollback()  # Rollback the changes if an exception occurs
            print(f"error {e} occured")
            return False
        finally:
            cursor.close()
            connection.close()
        return True
            

    def resumeDataInit(self, resumeData):
        self.resumeData=resumeData

    def __init__(self, username, password):
        self.username = username
        self.password = hash_password(password)

    # def __init__(self):
    #     self.username = None
    #     self.password = None

    def update_resume(self, resumeData):
        self.resumeData = resumeData
        #SQl update in database needs to be done

    def generate_latex_resume(self, template_path, mapping_path):
        with open(mapping_path) as mapping_file:
            mapping = json.load(mapping_file)

        with open(template_path) as template_file:
            latex_template = template_file.read()

        for key, value in mapping.items():
            if key not in self.resumeData:
                latex_template = latex_template.replace('%'+key+'STARTS','\\begin{comment}\n%')
                latex_template = latex_template.replace('%'+key+'ENDS','\end{comment}\n%')
                continue
            resData = self.resumeData[key]
            texDataToReplace = ''
            if bool(resData):
                print(resData)
                print("count",len(resData))
                if type(resData) is list:
                    for obj in resData:
                        temp_single = mapping[key+'_single'][0]
                        if type(obj) is dict:
                            for ok in obj:
                                temp_single = temp_single.replace(ok, escape_special_chars(obj[ok]))
                        else:
                            temp_single = temp_single.replace(key, escape_special_chars(obj))
                        texDataToReplace += temp_single
                else:
                    texDataToReplace = escape_special_chars(resData)
            else:  #empty field - remove from resumeData
                latex_template = latex_template.replace('%'+key+'STARTS','\\begin{comment}\n%')
                latex_template = latex_template.replace('%'+key+'ENDS','\end{comment}\n%')
            mapping[key][1] = texDataToReplace
            latex_template = latex_template.replace(value[0], value[1])