from flask import Flask, request, render_template, render_template_string
import mysql.connector
import subprocess

app = Flask(__name__)

log_prefix = '|LOG MESSAGE|'
db_host, user, password, db_name = 'database', 'root', 'root', 'hospital_db'


@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):
        log_message = '{} New request. Headers: {}'.format(log_prefix, request.headers)
        print(log_message)

        return render_template("main.html")

@app.route('/visits', methods = ['POST'])
def visits():
    if(request.method == 'POST'):
        # Get parameters from input form
        doctor_surname = request.form.get('doctor_surname')

        # Start database connection
        con = mysql.connector.connect(
            host=db_host, 
            user=user, 
            password=password, 
            database=db_name,
            charset='utf8mb4')
        
        cursor = con.cursor()

        # Define sql query
        sql_query = 'SELECT Visit.reservation_date, Patient.code, Patient.last_name, Patient.first_name, Visit.diagnosis, Visit.price, Visit.paid \
            FROM (Visit JOIN Doctor ON Visit.doctor = Doctor.id) JOIN Patient ON Visit.patient = Patient.code\
            WHERE Doctor.last_name = "{}";'.format(doctor_surname)
        
        # Run sql query
        cursor.execute(sql_query)

        # Fetch results
        out = cursor.fetchall()

        # Close cursor
        cursor.close()

        # Close connection
        con.close()

        return render_template('show_visits.html', visits= out, doctor= doctor_surname)

@app.route('/diagnosis', methods = ['POST', 'GET'])
def render_diagnosis_input():
    if (request.method == 'GET'):

        # Start database connection
        con = mysql.connector.connect(
            host=db_host, 
            user=user, 
            password=password, 
            database=db_name,
            charset='utf8mb4')
        
        cursor = con.cursor()

        # Define sql query
        sql_query = 'SELECT Visit.id, Visit.reservation_date, Visit.patient\
            FROM Visit\
            WHERE Visit.diagnosis IS NULL OR Visit.diagnosis = ""'
        
        # Run sql query
        cursor.execute(sql_query)

        # Fetch results
        out = cursor.fetchall()

        # Close connection
        cursor.close()
        con.close()

        # Format output
        output = []

        for row in out:
            output.append((row[0], '|| {} | {} | {} ||'.format(*row)))
        
        return render_template('diagnosis_input.html', options=output)
    else:
        diagnosis = request.form.get('diagnosis')
        price = request.form.get('price')
        doctor = request.form.get('doctor')
        visit_id = request.form.get('visit')

        sql_query = 'UPDATE Visit\
            SET Visit.diagnosis = "{}", Visit.price = "{}", Visit.doctor = "{}"\
            WHERE Visit.id = {}'

@app.route('/submit-diagnosis', methods = ['POST'])
def submit_diagnosis():
     if(request.method == 'POST'):
        # Get parameters from input form
        doctor_surname = request.form.get("surname")

        # Start database connection
        con = mysql.connector.connect(
            host=db_host, 
            user=user, 
            password=password, 
            database=db_name,
            charset='utf8mb4')
        
        cursor = con.cursor()

        # Define sql query
        sql_query = ''
        
        # Run sql query
        cursor.execute(sql_query)

        # Fetch results
        out = cursor.fetchall()

        # Close cursor
        cursor.close()

        # Close connection
        con.close()
        
        log_msg = '{} PHP Script @{} ended with result {}.'.format(log_prefix, php_script_path, out)
        print(log_msg)
        
        return render_template('diagnosis_input.html', result= out)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)

