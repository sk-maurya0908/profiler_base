import hashlib
import psycopg2, json

# Database Configuration
DB_NAME = "profiler_users_db"
DB_USER = "profiler"
DB_PASSWORD = "profiler"
DB_HOST = "localhost"

######### method to get the db connection obj
def connect_to_db():
    return psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

escapeDict = {'&':'\&', '%':'\%', '$':'\$', '#':'\#', '_':'\_', '{':'\{', '}':'\}', 
'~':'\\textasciitilde', '^':'\\textasciicircum', '\\':'\\textbackslash'}
def escape_special_chars(dataString):
    escapedString = dataString.translate(str.maketrans(escapeDict))
    return escapedString

class User:
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

    ######### method to insert user's data into database
    def validate_user(username,password):
        connection = connect_to_db()  #connecting to DB
        cursor = connection.cursor()
        hashed_password=hash_password(password)
        query=f"SELECT id FROM users WHERE username = '{username}' AND password = '{hashed_password}'"
        cursor.execute(query)
        user_id = cursor.fetchone()   #fetching the query results
        cursor.close()
        connection.close()               #closing the connection

        if not user_id:
            return -1
        return user_id

    ######### method to insert user's data into database
    def insert_userdata_in_db(user_id,completeUserData):
        # connecting to database
        connection=connect_to_db()
        cursor=connection.cursor()

        # get the basic data 
        basicData=completeUserData['basicData']
        # prepare data to be inserted into the table
        for key in basicDataKey:
            basicData[key]
        actualData
        try:
            query=f"INSERT INTO usersdata basicData='{data}'"
            # insert and commit the changes in the database
            cursor.execute(query)
            connection.commit()
        except Exception as e:
           connection.rollback()  # Rollback the changes if an exception occurs
           return f"error {e} occured"
        finally:
            cursor.close()
            connection.close()
        
            
        
    ######### method to insert user's data into database
    def insert_userdata_in_db(user_id,completeUserData):
        # connecting to database
        connection=connect_to_db()
        cursor=connection.cursor()

        # get the basic data 
        basicData=completeUserData['basicData']
        
        # prepare data to be inserted into the table
        data="nothing here"
        ############# ADD MORE HERE #############
        query=f"INSERT INTO usersdata SET eduDetails='{data1}' WHERE id='{user_id}'"

        # insert and commit the changes in the database
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    
    def registration(username,password):
        connection=connect_to_db()
        cursor = connection.cursor()
        
        query=f"SELECT user_id FROM users WHERE username = '{username}'"
        cursor.execute(query)
        user_exist = cursor.fetchone()   

        #checking if the entered username is available or not
        if(user_exist): 
            cursor.close()
            connection.close()
            return False
        else:
            hashed_password=hash_password(password)
            #add the username and password into the users table
            query=f"INSERT INTO users(username,password) VALUES({username},{hashed_password})"
            cursor.execute(query) #executing query
            connection.commit()
            cursor.close()
            connection.close()

        return True

    def __init__(self, username, password, resume):
        self.username = username
        # self.password = hash_password(password)
        self.resume = resume

    def update_resume(self, resume):
        self.resume = resume
        #SQl update in database needs to be done

    def hash_password(password):
        # Create a new SHA-256 hash object
        sha256 = hashlib.sha256()

        # Update the hash object with the password encoded as bytes
        sha256.update(password.encode('utf-8'))

        # return the hexadecimal representation of the hash
        return sha256.hexdigest()


    def generate_latex_resume(self, template_path, mapping_path):
        with open(mapping_path) as mapping_file:
            mapping = json.load(mapping_file)

        with open(template_path) as template_file:
            latex_template = template_file.read()

        for key, value in mapping.items():
            if key not in self.resume:
                latex_template = latex_template.replace('%'+key+'STARTS','\\begin{comment}\n%')
                latex_template = latex_template.replace('%'+key+'ENDS','\end{comment}\n%')
                continue
            resData = self.resume[key]
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
            else:  #empty field - remove from resume
                latex_template = latex_template.replace('%'+key+'STARTS','\\begin{comment}\n%')
                latex_template = latex_template.replace('%'+key+'ENDS','\end{comment}\n%')
            mapping[key][1] = texDataToReplace
            latex_template = latex_template.replace(value[0], value[1])