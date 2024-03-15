from flask import Flask, request, jsonify
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def login(username, password):
    session = HTMLSession()
    login_link = 'https://homeaccess.katyisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2fClasses%2fClasswork'
    
    try:
        response = session.get(login_link)
        soup = BeautifulSoup(response.html.html, 'html.parser')
        request_verification_token = soup.select_one('input[name="__RequestVerificationToken"]')
        
        if request_verification_token is None:
            raise Exception('Request verification token not found')
        
        data = {
            '__RequestVerificationToken': request_verification_token['value'],
            'LogOnDetails.UserName': username,
            'LogOnDetails.Password': password,
            'SCKTY00328510CustomEnabled': 'True',
            'SCKTY00436568CustomEnabled': 'True',
            'Database': '10',
            'VerificationOption': 'UsernamePassword'
        }
        
        response = session.post(login_link, data=data)
        
        if 'LogOn' in response.url:
            raise Exception('Invalid username or password')
        
        response = session.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/Assignments.aspx')
        return response.html.html
    except Exception as e:
        raise e
    finally:
        session.close()

@app.route("/")
def home():
    return "Flask API on Vercel"

@app.route("/api")
def api_home():
    return jsonify({
        'message': 'Home Access Center API',
        'routes': ['/api', '/api/getGrades']
    })

@app.route("/api/getGrades")
def get_grades():
    username = request.args.get('username')
    password = request.args.get('password')
    
    try:
        page_content = login(username, password)
        soup = BeautifulSoup(page_content, 'html.parser')
        
        class_names = []
        grades = []
        
        assignment_classes = soup.select('.AssignmentClass')
        
        if not assignment_classes:
            raise Exception('No assignment classes found')
        
        for i, assignment_class in enumerate(assignment_classes):
            name_element = assignment_class.select_one('.sg-header a')
            if name_element is None:
                raise Exception(f'Class name not found for assignment class {i+1}')
            name = name_element.text.strip()
            class_names.append(name)
            class_grades = []
            categories_id = f'#plnMain_rptAssigmnetsByCourse_lblCategories_{i}'
            categories = soup.select_one(categories_id)
            if categories is None:
                grades.append(class_grades)
                continue
            
            for row in categories.select('.sg-asp-table-data-row'):
                cells = row.select('td')
                if len(cells) < 2:
                    raise Exception(f'Invalid category row for assignment class {i+1}')
                category = [cell.text.strip() for cell in cells[1:]]
                class_grades.append(category)
            
            grades.append(class_grades)
        
        return jsonify({
            'success': True,
            'names': class_names,
            'grades': grades
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

if __name__ == "__main__":
    app.run(debug=True)