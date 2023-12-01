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

@app.route('/diagnosis', methods = ['POST'])
def diagnosis():
     if(request.method == 'POST'):
        return render_template("diagnosis_input.html")

@app.route('/visits', methods = ['POST'])
def visits():
    if(request.method == 'POST'):
        # php_script_path = '/var/www/html/templates/show_visits.php'
        # php_script_exec = subprocess.Popen(['php', php_script_path], shell=True, stdout=subprocess.PIPE)

        # print('{} PHP Script ended: {}'.format(log_prefix, php_script_exec))
        # out = php_script_exec.stdout.read()

        # log_msg = '{} PHP Script @{} ended with result {}.'.format(log_prefix, php_script_path, out)
        # print(log_msg)
        # print(type(out))
        
        # Get parameters from input form
        doctor_surname = request.form.get("surname")

        # Start database connection
        con = mysql.connector.connect(db_host, user, password, db_name)
        cursor = con.cursor()

        # Define sql query
        sql_query = 'SELECT * \
            FROM (Visit JOIN Doctor ON Visit.doctor = Doctor.id) \
            WHERE Doctor.last_name = "{}";'.format(doctor_surname)
        
        # Run sql query
        cursor.execute(sql_query)

        # Fetch results
        out = cursor.fetchall()

        if (out is None or len(out) == 0):
            out_html = 'No visits were found made by {}'.format(doctor_surname)
        else:
            log_msg = '{} Showing {} results.'.format(log_prefix, len(out))
            out_html = out

        return render_template('show_visits.html', html_response= out_html, doctor= doctor_surname)

@app.route('/submit-diagnosis', methods = ['POST'])
def submit_diagnosis():
     if(request.method == 'POST'):
        php_script_path = '/var/www/html/templates/diagnosis_input.php'

        out = subprocess.check_output(['php', php_script_path], universal_newlines=True)
        
        log_msg = '{} PHP Script @{} ended with result {}.'.format(log_prefix, php_script_path, out)
        print(log_msg)
        
        return render_template('diagnosis_input.html', result= out)

        return render_template_string("{{ php_output }}", php_output= out)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)

