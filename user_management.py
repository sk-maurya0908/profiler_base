from werkzeug.security import generate_password_hash, check_password_hash
import json


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

    def update_resume(self, resume):
        self.resume = resume
        #SQl update in database needs to be done

    def check_password(self, password):
        return check_password_hash(self.password, password)


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