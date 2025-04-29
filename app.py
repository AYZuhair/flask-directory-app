from flask import Flask, render_template, request, redirect, url_for
import boto3

# 🔐 Insert your credentials here
AWS_ACCESS_KEY_ID = 'ASIAY5ZKYKEZ4K4A74V3'
AWS_SECRET_ACCESS_KEY = 'kjAvks6inCRzJ2o8bkDrW9GcwPyuY8oq+jMv9r2t'
AWS_SESSION_TOKEN = 'IQoJb3JpZ2luX2VjEPj//////////wEaCXVzLXdlc3QtMiJHMEUCIGxNda6C9ipXBTRyAYTHxrKesNEfB1lbpJWKYFxbD8TkAiEAw2wkOKwv4mJ4x2RCeA7AmZduwt4LmrNLeMN/RyP9jkwqvAIIkf//////////ARAAGgw2MTM3MzMxMjY0NTEiDCJ4c01Zy2oNFI9pyiqQAupwuD219qclEsU4B4ZfatYXQdhQ5pcK7y1Ygu1atLBbPCk0OYwLvYCz565v26QoiVrcKmvmkfBsT6KeZ+ZsR//hnJKfShRtMUJp3TUHJ8caFsjX+O3ZIL1oKVko2iZkemyAlVCqQIG0KdTJAHUiytK/WLdTuP4dUjcKkI3IdgaaSUXiYgx1vqLUEGLCa1c3zC9CWs0tIkSX41wksjfQ4K6xvKBTVGKatWKYt6IA0r0HDAA0Pu1Uh/Di3DJ2TajkysK1XeD0PMFQvhEzyhbr8YEw3ctfEK75BbCkIWBwJZeReaOHm4y/s+EiTgTqNlXJBAX8ceikfj7TtWoFZ6oRe+Ov62svIKYRhCWLuKKfHMl2MMnqw8AGOp0BbYf6f6zdE4TVxMtuBOCNmNdhRrhpU5qKkr0TB+GF+3kiromxx4QNtEemorWix6GdP85ANFf9bsTJYN2DGVXP4GkiNhih9+JTOn9dSROTfiNGjZt4clab8JEv2gNefq2fsf4fzDjUL0QE9FGum9BqfFiSWGb/SJUrsWMphWiZ2QOfkEcaqzsjsDuiOpnHr9oHe9Dulo+z9Y/FE2xCig=='
AWS_REGION = 'us-east-1'

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=AWS_REGION
)

dynamodb = session.resource('dynamodb')
table = dynamodb.Table('Employees')

app = Flask(__name__)

@app.route('/')
def index():
    response = table.scan()
    employees = response.get('Items', [])
    return render_template('index.html', employees=employees)

@app.route('/employee/<string:employee_id>')
def employee_detail(employee_id):
    response = table.get_item(Key={'employee_id': employee_id})
    employee = response.get('Item')
    return render_template('employee_detail.html', employee=employee)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employee = {
            'employee_id': request.form['employee_id'],
            'name': request.form['name'],
            'email': request.form['email'],
            'department': request.form['department'],
            'position': request.form['position']
        }
        table.put_item(Item=employee)
        return redirect(url_for('index'))
    return render_template('add_employee.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
