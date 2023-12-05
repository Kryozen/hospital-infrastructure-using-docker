from flask import Flask , render_template, request, redirect, url_for, session
from hashlib import sha256
import secrets
import mysql.connector

app = Flask(__name__)

seed = '{}'.format(secrets.randbelow(100))
app.secret_key = sha256(seed.encode()).hexdigest()

log_prefix = '|LOG MESSAGE|'
db_host, user, password, db_name = 'database', 'root', 'root', 'hospital_db'

@app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'GET'):
        # Logging
        log_msg = "{} {}\n[================]".format(log_prefix, request)
        print(log_msg)

        # Read error codes
        sql_message = request.args.getlist('sql_message')
        return render_template("main.html", sql_message=sql_message)
    else:
        # Login attempt
        
        # Reading parameters from form
        email = request.form.get('email')
        pwd = sha256(request.form.get('password').encode()).hexdigest()
        
        # Start database connection
        con = mysql.connector.connect(
            host=db_host, 
            user=user, 
            password=password, 
            database=db_name,
            charset='utf8mb4')
        
        cursor = con.cursor()

        # Define sql query
        sql_query = 'SELECT Patient.first_name\
            FROM Patient\
            WHERE Patient.email = %(email)s AND Patient.pwd = %(pwd)s;'
        
        parameters = {
            'email':email,
            'pwd':pwd
        }
        
        # Run sql query
        cursor.execute(sql_query, parameters)

        # Fetch results
        out = cursor.fetchall()

        # Close cursor
        cursor.close()

        # Close connection
        con.close()

        if len(out) > 0:
            # Logging
            log_msg = "{} Login attempt successful\n[================]".format(log_prefix, 0)
            print(log_msg)

            session['user'] = email
            return render_template('main.html', login_code='0')
        else:
            # Logging
            log_msg = "{} Login attempt unsuccessful\n[================]".format(log_prefix)
            print(log_msg)

            return render_template('main.html', login_code='1')
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # Reading parameters from form
        email = request.form.get('email')
        pwd = sha256(request.form.get('password').encode()).hexdigest()
        first_name = request.form.get('name')
        last_name = request.form.get('surname')
        birth_date = request.form.get('birthday')

        # Start database connection
        con = mysql.connector.connect(
            host=db_host, 
            user=user, 
            password=password, 
            database=db_name,
            charset='utf8mb4')
        
        cursor = con.cursor()

        # Define sql query
        sql_query = 'INSERT INTO Patient(email, pwd, first_name, last_name, birthdate) VALUE \
            (%(email)s, %(pwd)s, %(first_name)s,%(last_name)s,%(birth_date)s);'
        
        parameters = {
            'email':email,
            'pwd':pwd,
            'first_name':first_name,
            'last_name':last_name,
            'birth_date':birth_date
        }
        
        try:
            # Run sql query
            cursor.execute(sql_query, parameters)

            # Commit changes
            con.commit()

            sql_message = ('Registration', 0)
        except Exception:
            # Send error message
            sql_message = ('Registration', 1)

            # Log error
            log_msg = "{} Error while executing query:\n{}\n[============].".format(log_prefix, sql_query)
            print(log_msg)
        finally:
            # Close cursor
            cursor.close()

            # Close connection
            con.close()

            return redirect(url_for('home', sql_message=sql_message))

@app.route('/reservation', methods=['POST'])
def reservation():
    # Reading parameters from form
    email = session.pop('user')
    app_date = request.form.get('app_date')
    app_time = request.form.get('app_time')

    reservation_date = '{} {}'.format(app_date, app_time)

    # Start database connection
    con = mysql.connector.connect(
        host=db_host, 
        user=user, 
        password=password, 
        database=db_name,
        charset='utf8mb4')
    
    cursor = con.cursor()

    # Define sql queries
    sql_query_1 = 'SELECT * FROM Visit WHERE Visit.reservation_date = %(reservation_date)s;'

    sql_query_2 = 'INSERT INTO Visit(reservation_date, diagnosis, price, paid, patient, doctor) \
        VALUE (%(reservation_date)s, NULL, NULL, 0, %(email)s, NULL);'
    
    parameters = {
        'email':email,
        'reservation_date':reservation_date
    }

    # Run first sql query
    cursor.execute(sql_query_1, parameters)

    # Fetch results
    out = cursor.fetchall()

    if len(out) > 0:
        # The date and time is busy
        sql_message = ('Reservation', 1)

        return redirect(url_for('home', sql_message=sql_message))
    else:
        try:
            # Run sql query
            cursor.execute(sql_query_2, parameters)

            # Commit changes
            con.commit()

            sql_message = ('Reservation', 0)
        finally:
            # Close cursor
            cursor.close()

            # Close connection
            con.close()

            return redirect(url_for('home', sql_message=sql_message))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
    