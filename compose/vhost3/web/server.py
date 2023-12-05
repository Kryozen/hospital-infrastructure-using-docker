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

@app.route('/', methods = ['GET'])
def home():
    # Log request
    log(request)

    # Show main page with query execution
    sql_message = request.args.getlist('sql_message')
    if len(sql_message) == 0:
        return render_template('main.html')
    return render_template("main.html", sql_message=sql_message)

@app.route('/add_doctor', methods = ['GET', 'POST'])
def add_doctor():
    # Log request
    log(request)

    if request.method == 'GET':
        return render_template('add_doctor.html')
    else:
        id = request.form.get('doc_id')
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        specialization = request.form.get('specialization')

        # Start database connection
        con = mysql.connector.connect(
            host=db_host, 
            user=user, 
            password=password, 
            database=db_name,
            charset='utf8mb4')
        
        cursor = con.cursor()

        # Define sql query
        sql_query = 'INSERT INTO Doctor(id, last_name, first_name, specialization) VALUE \
            (%(id)s, %(last_name)s, %(first_name)s, %(specialization)s)'
        
        parameters = {
            'id':id,
            'last_name':last_name,
            'first_name':first_name,
            'specialization':specialization
        }
        
        try: 
            # Run sql query
            cursor.execute(sql_query, parameters)

            # Commit changes
            con.commit()

            # Update successfull
            sql_message = (id, 0)

            # Log update
            log('{} added {} in the database'.format(request.remote_addr, id))
        except:
            # Update failed
            sql_message = (id, 1)
        finally:
            # Close cursor
            cursor.close()

            # Close connection
            con.close()

            return redirect(url_for('home', sql_message=sql_message))   
        
@app.route('/edit_doctor', methods=['GET', 'POST'])
def edit_doctor():
    # Log request
    log(request)

    if request.method == 'GET':
        # Start database connection
        con = mysql.connector.connect(
            host=db_host, 
            user=user, 
            password=password, 
            database=db_name,
            charset='utf8mb4')
        
        cursor = con.cursor()

        # Define sql query
        sql_query = 'SELECT Doctor.id, Doctor.last_name, Doctor.first_name, Doctor.specialization\
            FROM Doctor'
        
        # Run sql query
        cursor.execute(sql_query)

        # Fetch results
        out = cursor.fetchall()

        # Close connection
        cursor.close()
        con.close()

        # Format output
        doctors = []

        for row in out:
            doctors.append((row[0], '|| {} | {} | {} | {} ||'.format(*row)))
        
        return render_template('edit_doctor.html', doctors=doctors)
    else:
        id = request.form.get('doc_id')
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        specialization = request.form.get('specialization')

        # Find altered fields in order to create a dynamical sql query
        changes = []
        if last_name != '':
            changes.append('last_name')
        if first_name != '':
            changes.append('first_name')
        if specialization != '':
            changes.append('specialization')
        
        if len(changes) == 0:
            # No fields were altered
            return redirect(url_for('home'))

        # Start database connection
        con = mysql.connector.connect(
            host=db_host, 
            user=user, 
            password=password, 
            database=db_name,
            charset='utf8mb4')
        
        cursor = con.cursor()

        # Define sql query dynamically
        sql_query = 'UPDATE Doctor SET {} WHERE Doctor.id = %(id)s;'
        
        to_set = ''
        for i in range(len(changes) - 1):
            to_set += '{} = %({})s, '.format(changes[i], changes[i])
        to_set += '{} = %({})s'.format(changes[-1], changes[-1])

        sql_query = sql_query.format(to_set)

        parameters = {
            'id':id,
            'last_name':last_name,
            'first_name':first_name,
            'specialization':specialization
        }
        
        try: 
            # Run sql query
            cursor.execute(sql_query, parameters)

            # Commit changes
            con.commit()

            # Update successfull
            sql_message = (id, 0)

            # Log update
            log('{} updated {} in the database'.format(request.remote_addr, id))
        except Exception as er:
            print(er)
            # Update failed
            sql_message = (id, 1)
        finally:
            # Close cursor
            cursor.close()

            # Close connection
            con.close()

            return redirect(url_for('home', sql_message=sql_message))
        
@app.route('/edit_visit', methods=['GET', 'POST'])
def edit_visit():
    # Log request
    log(request)

    if request.method == 'GET':
        # Start database connection
        con = mysql.connector.connect(
            host=db_host, 
            user=user, 
            password=password, 
            database=db_name,
            charset='utf8mb4')
        
        cursor = con.cursor()

        # Define sql query
        sql_query = 'SELECT Visit.id, Visit.reservation_date, Visit.price, Visit.paid, Visit.doctor, Visit.patient \
            FROM Visit'
        
        # Run sql query
        cursor.execute(sql_query)

        # Fetch results
        out = cursor.fetchall()

        # Close connection
        cursor.close()
        con.close()

        # Format output
        visits = []

        for row in out:
            visits.append((row[0], '|| {} | {} | {} | {} | {} ||'.format(*row)))
        
        return render_template('edit_visit.html', visits=visits)
    else:
        id = request.form.get('visit_id')
        date = request.form.get('date')
        paid = request.form.get('paid')
        price = request.form.get('price')
        doctor = request.form.get('doctor')

        # Find altered fields in order to create a dynamical sql query
        changes = []
        if date != '':
            changes.append('reservation_date')
        if paid != '':
            changes.append('paid')
        if price != '':
            changes.append('price')
        if doctor != '':
            changes.append('doctor')
        
        if len(changes) == 0:
            # No fields were altered
            return redirect(url_for('home'))

        # Start database connection
        con = mysql.connector.connect(
            host=db_host, 
            user=user, 
            password=password, 
            database=db_name,
            charset='utf8mb4')
        
        cursor = con.cursor()

        # Define sql query dynamically
        sql_query = 'UPDATE Visit SET {} WHERE Visit.id = %(id)s;'
        
        to_set = ''
        for i in range(len(changes) - 1):
            to_set += '{} = %({})s, '.format(changes[i], changes[i])
        to_set += '{} = %({})s'.format(changes[-1], changes[-1])

        sql_query = sql_query.format(to_set)

        parameters = {
            'id':id,
            'reservation_date':date,
            'paid':paid,
            'price':price,
            'doctor':doctor
        }
        
        try: 
            # Run sql query
            cursor.execute(sql_query, parameters)

            # Commit changes
            con.commit()

            # Update successfull
            sql_message = (id, 0)

            # Log update
            log('{} edited {} in the database'.format(request.remote_addr, id))

        except Exception as er:
            print(er)
            # Update failed
            sql_message = (id, 1)
        finally:
            # Close cursor
            cursor.close()

            # Close connection
            con.close()

            return redirect(url_for('home', sql_message=sql_message))

if __name__ == '__main__':
    # Log startup
    log('Application started', 'start')

    # Run app
    app.run(debug=True, host='0.0.0.0', port=80)

    # Log shutdown
    log('Application shutdown', 'shutdown')
