from flask import Flask, request
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):
        f_html = open("/var/www/html/vhost2_main.html", "r")
        return f_html.read()

if __name__ == '__main__':

	app.run(debug=True, host='0.0.0.0', port=80)


