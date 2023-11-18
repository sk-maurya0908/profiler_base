from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')
        self.resume = {
            'name': '',
            'rollNumber': '',
            'department': '',
            'program': '',
            'gender': '',
            'education': [],
            'work_experience': [],
            'skills': [],
        }

    def update_resume(self, name, rollNumber, department, program, gender, education, work_experience, skills):
        self.resume['name'] = name
        self.resume['rollNumber'] = rollNumber
        self.resume['department'] = department
        self.resume['program'] = program
        self.resume['gender'] = gender
        self.resume['education'] = education.split('\n')
        self.resume['work_experience'] = work_experience.split('\n')
        self.resume['skills'] = skills.split('\n')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def genResume(uname):
        details = getStudentDetails(uname)

    def getStudentDetails(uname):
        return null