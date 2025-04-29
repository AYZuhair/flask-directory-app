from flask import Flask, render_template, request, redirect, url_for
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
    region_name=os.getenv('AWS_REGION')
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
