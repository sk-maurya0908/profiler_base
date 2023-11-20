from werkzeug.security import generate_password_hash, check_password_hash
import json, subprocess, os

def convert_latex_to_pdf(latex_content, output_path='temp_resume'):
    # Creating temporary directory
    temp_dir = os.path.join(os.getcwd(), 'temp_latex')  
    os.makedirs(temp_dir, exist_ok=True)

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

class User:
    def __init__(self, username, password, resume):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')
        self.resume = resume

    def update_resume(self, name, rollNumber, department, program, gender, education, work_experience, skills):
        self.resume = resume
        #SQl update in database needs to be done

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_latex_resume(self, template_path, mapping_path):
        with open('data_mapping.json') as mapping_file:
            mapping = json.load(mapping_file)

        with open('SWL_RESUME_TEMPLATE.tex') as template_file:
            latex_template = template_file.read()

        for key, value in mapping.items():
            if key not in resume:
                latex_template = latex_template.replace('%'+key+'STARTS','\\begin{comment}\n%')
                latex_template = latex_template.replace('%'+key+'ENDS','\end{comment}\n%')
                continue
            resData = resume[key]
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