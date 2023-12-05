from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import mysql.connector

app = Flask(__name__)

# Database connection data
db_host, user, password, db_name = 'database', 'root', 'root', 'hospital_db'

# Logging utility
def log(data, log_code = 'log'):
    now = datetime.now()
    current_date, current_time = now.strftime('%Y%m%d'), now.strftime('%H:%M:%S')

    log_prefix = '> [{} {}]:'.format(current_time, log_code.upper())

    with open('/var/www/html/{}.log'.format(current_date), 'a') as logfile:
        log_msg = '{} {}\n'.format(log_prefix, data)
        logfile.write(log_msg)

@app.route('/', methods = ['GET', 'POST'])
def home():
    # Log request
    log(request)
    if(request.method == 'GET'):
        # Just show main page        
        return render_template("main.html")
    else:
        # Show main page with query execution
        sql_message = request.args.getlist('sql_message')
        return render_template("main.html", sql_message=sql_message)

@app.route('/visits', methods = ['POST'])
def visits():
    # Log request
    log(request)

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
        sql_query = 'SELECT Visit.reservation_date, Patient.email, Patient.last_name, Patient.first_name, Visit.diagnosis, Visit.price, Visit.paid \
            FROM (Visit JOIN Doctor ON Visit.doctor = Doctor.id) JOIN Patient ON Visit.patient = Patient.email\
            WHERE Doctor.last_name = %s;'
        
        # Run sql query
        cursor.execute(sql_query, (doctor_surname,))

        # Fetch results
        out = cursor.fetchall()

        # Close cursor
        cursor.close()

        # Close connection
        con.close()

        return render_template('show_visits.html', visits= out, doctor= doctor_surname)

@app.route('/diagnosis', methods = ['POST', 'GET'])
def render_diagnosis_input():
    # Log request
    log(request)
    
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

        sql_query2 = 'SELECT Doctor.id, Doctor.last_name, Doctor.first_name\
            FROM Doctor'
        
        # Run sql query
        cursor.execute(sql_query)

        # Fetch results
        out = cursor.fetchall()

        # Run sql query 2
        cursor.execute(sql_query2)

        # Fetch results
        out2 = cursor.fetchall()

        # Close connection
        cursor.close()
        con.close()

        # Format output
        visits = []
        doctors = []

        for row in out:
            visits.append((row[0], '|| {} | {} | {} ||'.format(*row)))

        for row in out2:
            doctors.append((row[0], '|| {} | {} | {} ||'.format(*row)))
        
        return render_template('diagnosis_input.html', options=visits, doctors=doctors)
    else:
        # Get form parameters
        diagnosis = request.form.get('diagnosis')
        price = request.form.get('price')
        doctor = request.form.get('doctor')
        visit_id = request.form.get('visit')

        # Start database connection
        con = mysql.connector.connect(
            host=db_host, 
            user=user, 
            password=password, 
            database=db_name,
            charset='utf8mb4')
        
        cursor = con.cursor()

        # Define sql query
        sql_query = 'UPDATE Visit\
            SET Visit.diagnosis = %(diagnosis)s, Visit.price = %(price)s, Visit.doctor = %(doctor)s\
            WHERE Visit.id = %(visit_id)s'
        
        parameters = {
            'diagnosis': diagnosis,
            'price': price,
            'doctor': doctor,
            'visit_id': visit_id
        }

        try:
            # Run sql query
            cursor.execute(sql_query, parameters)

            # Commit changes
            con.commit()

            # Send success message
            sql_message = ('Update', 0)

            # Log update
            log('{} updated {} as {}'.format(request.remote_addr, visit_id, doctor))
        except Exception:
            # Send error message
            sql_message = ('Update', 1)

        finally:
            # Close connection
            cursor.close()
            con.close()

            return redirect(url_for('home', sql_message= sql_message), code=307)
        

if __name__ == '__main__':
	# Log startup
    log('Application started', 'start')

    # Run app
    app.run(debug=True, host='0.0.0.0', port=80)

    # Log shutdown
    log('Application shutdown', 'shutdown')
