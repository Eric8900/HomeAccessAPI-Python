from flask import Flask, request, jsonify
from requests_html import HTMLSession
from bs4 import BeautifulSoup

app = Flask(__name__)

def login(username, password):
    session = HTMLSession()
    login_link = 'https://homeaccess.katyisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2fClasses%2fClasswork'
    
    try:
        response = session.get(login_link)
        soup = BeautifulSoup(response.html.html, 'html.parser')
        request_verification_token = soup.select_one('input[name="__RequestVerificationToken"]')['value']
        
        data = {
            '__RequestVerificationToken': request_verification_token,
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

@app.route("/api/home")
def api_home():
    return jsonify({
        'message': 'Welcome to the Home Access Center API!',
        'routes': ['/api/home', '/api/getGrades']
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
        
        for i, assignment_class in enumerate(assignment_classes):
            name = assignment_class.select_one('.sg-header a').text.strip()
            class_names.append(name)
            
            categories = soup.select_one(f'#plnMain_rptAssigmnetsByCourse_lblCategories_{i}')
            class_grades = []
            
            for row in categories.select('.sg-asp-table-data-row'):
                category = [cell.text.strip() for cell in row.select('td')[1:]]
                class_grades.append(category)
            
            grades.append(class_grades)
        
        return jsonify({
            'success': True,
            'names': class_names,
            'grades': grades
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)