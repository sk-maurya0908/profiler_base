import json, subprocess, os

def convert_latex_to_pdf(latex_content, output_path='temp_resume'):
    # Create a temporary directory for LaTeX files
    temp_dir = os.path.join(os.getcwd(), 'temp_latex')
    os.makedirs(temp_dir, exist_ok=True)

    # Define paths for LaTeX and PDF files
    latex_file_path = os.path.join(temp_dir, 'resume.tex')
    pdf_file_path = os.path.join(temp_dir, 'resume.pdf')

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
        os.remove(os.path.join(temp_dir, 'resume.log'))
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

resume = {
    'name': 'Shubham Kumar',
    'rollNumber': '23m0836',
    'departmentName': 'Computer Science & Engineering',
    'programName': 'M.Tech',
    'gender': 'Male',
    'education': [{
        "exam":"PG",
        "univ":"IITB",
        "insti":"IITB",
        "yop":"2026",
        "cpi":"9.4"
    },
    {
        "exam":"UG",
        "univ":"SPPU",
        "insti":"DYPCOE",
        "yop":"2020",
        "cpi":"9.2"
    }],
    'workExperience': [{
        "designation":"System Engineer",
        "organisation":"TCS",
        "fromDate-toDate":"Aug 2020 - July 2023",
        "yourRolesAndResponsibilitiesInOrganization":"Developing and deploying web application for inter-bank communication using SEI services"
    },
    {
        "designation":"Intern",
        "organisation":"Virtusa",
        "fromDate-toDate":"May 2019 - July 2019",
        "yourRolesAndResponsibilitiesInOrganization":"Tried implementing digitized management of parking space using computer vision"
    }],
    'technicalSkills': ["C++","C#","Azure","MSSQL"],
    'projectTitle':'Resume Generator Web app',
    "projectGuide":"Prof. Bhaskar Raman",
    "projectDescription":"Generate a resume of a user with provided details in web app",
    "projectDate":"Oct 2023 - Nov 2023",
    "currentWorkDone":"Resume with basic details can be generated",
    "futureWorkToBeDone":"Validation of data inserted in order to prevent attacks on database. Also, verification to maintain the genuinity can be implemented.",
    "seminarTitle":"SQLi Attacks",
    "seminarGuide":"Prof. Kameshwari Chebrolu",
    "seminarDescription":"Attacks using injection still comes under OWASP Top 10.",
    "seminarDate":"Dec 2023 - Mar 2024",
    "courseProjects":[{
        'courseProjectTitle':'Autograding server',
        'associatedCourseNameAndCode':'DECS (CS744)',
        'courseInstructorName':'Prof. Varsha Apte',
        'courseFromDate-courseToDate':'Aug 2023 - Nov 2023',
        'courseProjectDescription':'creating a fully functional multithreaded autograding server to grade programming assignments',
    },
    {
        'courseProjectTitle':'Resume generator web app',
        'associatedCourseNameAndCode':'SWL (CS699)',
        'courseInstructorName':'Prof. Bhaskar Raman',
        'courseFromDate-courseToDate':'Oct 2023 - Nov 2023',
        'courseProjectDescription':'creating a web app to generate resume with provided details'
    },
    {
        'courseProjectTitle':'God knows what',
        'associatedCourseNameAndCode':'PA (CS618)',
        'courseInstructorName':'Prof. Uday Khedkar',
        'courseFromDate-courseToDate':'Aug 2023 - Nov 2023',
        'courseProjectDescription':'I really don\'t know but it was quite interesting :)'
    }],
    "certifications":[{
        'certificationTitle':'Smart Contract using solidity',
        'certifcationOfferedBy':'SUNY',
        'certificationPlatform':'Coursera',
        'certificationDate':'June 2018',
    },
    {
        'certificationTitle':'Learning how to learn',
        'certifcationOfferedBy':'',
        'certificationPlatform':'Coursera',
        'certificationDate':'March 2021',
    }],
    "achievements":["achievement1","achievement2"],
    "extraCurriculars":["extraCurricular1","extraCurricular2","extraCurricular3"],
    "hobbies":["basketball","reading","poetry","bakchodi"]
}
with open('data_mapping.json') as mapping_file:
    mapping = json.load(mapping_file)

with open('SWL_RESUME_TEMPLATE.tex') as template_file:
    latex_template = template_file.read()

for key, value in mapping.items():
    if key not in resume:
        continue
    resData = resume[key]
    texDataToReplace = ''
    if type(resData) is list:
        #print("count",len(resData))
        if bool(resData):
            #print(*resData)
            for obj in resData:
                #print("obj",type(obj))
                #print(resData,obj)
                temp_single = mapping[key+'_single'][0]
                #print(temp_single)
                if type(obj) is dict:
                    for ok in obj:
                        #print(ok, obj[ok])
                        temp_single = temp_single.replace(ok, escape_special_chars(obj[ok]))
                        #print(temp_single)
                else:
                    temp_single = temp_single.replace(key, escape_special_chars(obj))
                    #print(temp_single)
                texDataToReplace += temp_single
            #print("Done list")
    else:
        texDataToReplace = escape_special_chars(resData)
    mapping[key][1] = texDataToReplace
    #print(key, value)
    latex_template = latex_template.replace(value[0], value[1])

#print(mapping)
#print(latex_template)
convert_latex_to_pdf(latex_template)