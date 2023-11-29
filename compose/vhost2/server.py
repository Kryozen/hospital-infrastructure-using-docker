from flask import Flask, request, render_template, render_template_string
import subprocess

app = Flask(__name__)
log_prefix = '|LOG MESSAGE|'

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
        php_script_path = '/var/www/html/templates/show_visits.php'
        out = subprocess.check_output(['php', php_script_path], universal_newlines=True)
        
        log_msg = '{} PHP Script @{} ended with result {}.'.format(log_prefix, php_script_path, out)
        print(log_msg)
        print(type(out))

        doctor_surname = request.form.get("surname")

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


