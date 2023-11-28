from flask import Flask, request  #This module allows you to create the Flask application. request: This module provides access to incoming request data such as form data, files, etc., within the Flask application.
from urllib.request import urlopen  #urllib.request: This module allows you to open URLs (web pages or APIs) within your Python code. Here, urlopen is specifically used to make HTTP requests to external resources.
import json  #This module helps in working with JSON data, parsing JSON strings, and encoding Python objects into JSON format.

#Let's assume you want different functionalities for admins and secretaries:

    #Admins: Can view and modify all reservations and modify users' information.
    #Secretaries: Can view and modify only reservations.

app = Flask(__name__) #creates an instance of the Flask application.

@app.route('/') #decorators are a way to add functionality to functions or methods in a concise way. In Flask, @app.route('/') is used to define a route for a web request.
def index():
    return render_template('index.html', reservations=reservations)  #This code specifies that when a user accesses the root URL of your Flask application (e.g., http://yourwebsite.com/), the index() function will be triggered. Inside this function, the render_template() function is used to render the index.html template, passing along the reservations data to that template.

#Admins and secretaries can check reservations
@app.route('/admin_and_secretary/reservations')
def admin_and_secretary_reservations():
    admin_reservations = [r for r in reservations if r['role'] == 'admin']
    secretary_reservations = [r for r in reservations if r['role'] == 'secretary']
    all_reservations = admin_reservations + secretary_reservations
    return render_template('combined_reservations.html', reservations=all_reservations)


#Route for admins and secretaries to modify a reservation
@app.route('/modify/<int:reservation_id>', methods=['GET', 'POST'])
if request.method == 'POST':
        # Handle modification (update database or data structure)

 # Fetch reservation details and render a form for modification
    reservation = next((r for r in reservations if r['id'] == reservation_id), None)
    return render_template('modify_reservation.html', reservation=reservation)

#Admins can modify patients information 
@app.route('/modify_patient/<int:patient_id>', methods=['GET','POST'])  
if request.method == 'POST' :
    # Handle modification (update database or data structure)
    new_name = request.form.get('new_name')
        # Update patient information based on the form data
        
    patient = next((p for p in patients if p['id'] == patient_id), None)
    return render_template('modify_patient.html', patient=patient)

if __name__ == '__main__':   #he purpose of if __name__ == '__main__': is to provide a way to distinguish whether the current script is the main program being executed or if it's being imported as a module into another script. Anything within this block will only execute when the script is run directly.

	app.run(debug=True, host='0.0.0.0', port=80)

