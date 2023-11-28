from flask import Flask, request, render_template
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):
        return render_template("vhost2_main.html")

@app.route('/diagnosis', methods = ['POST'])
def diagnosis():
     if(request.method == 'POST'):
        return render_template("vhost2_diagnosis_input.html")

@app.route('/visits', methods = ['POST'])
def visits():
     if(request.method == 'POST'):
        return render_template("vhost2_show_visits.html")

@app.route('/submit-diagnosis', methods = ['POST'])
def submit_diagnosis():
     if(request.method == 'POST'):
        return render_template("vhost2_diagnosis_input.php")

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)


