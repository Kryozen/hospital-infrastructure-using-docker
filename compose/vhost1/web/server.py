from flask import Flask , render_template, request
from hashlib import sha256
import mysql.connector

app = Flask(__name__)

log_prefix = '|LOG MESSAGE|'
db_host, user, password, db_name = 'database', 'root', 'root', 'hospital_db'

@app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'GET'):
        # Logging
        log_msg = "{} \n{}\n[================]".format(log_prefix, request)
        print(log_msg)

        # Render page
        return render_template('main.html')
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
            WHERE Patient.email == %(email)s AND Patient.pwd == %(pwd)s'
        
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
            return render_template('main.html', login_code=0)
        else:
            return render_template('main.html', login_code=1)
    

@app.route('/register', methods=['POST'])
def register():
    # Reading parameters from form
    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('')
    last_name = request.form.get('')
    birth_date = request.form.get('')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
    