from flask import Flask, request, render_template, render_template_string
import subprocess

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):
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

        return render_template('show_visits.html', result= out)

@app.route('/submit-diagnosis', methods = ['POST'])
def submit_diagnosis():
     if(request.method == 'POST'):
        php_script_path = '/var/www/html/templates/diagnosis_input.php'

        out = subprocess.check_output(['php', php_script_path], universal_newlines=True)

        return render_template('diagnosis_input.html', result= out)

        return render_template_string("{{ php_output }}", php_output= out)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)


