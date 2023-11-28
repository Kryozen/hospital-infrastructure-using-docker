from flask import Flask, request, render_template

app = Flask(__name__)

reservations = [...] 
patients = [...]

@app.route('/')
def index():
    return render_template('index.html', reservations=reservations)

@app.route('/admin_and_secretary/reservations')
def admin_and_secretary_reservations():
    admin_reservations = [r for r in reservations if r['role'] == 'admin']
    secretary_reservations = [r for r in reservations if r['role'] == 'secretary']
    all_reservations = admin_reservations + secretary_reservations
    return render_template('combined_reservations.html', reservations=all_reservations)

@app.route('/modify/<int:reservation_id>', methods=['GET', 'POST'])
def modify_reservation(reservation_id):
    if request.method == 'POST':
        # Handle modification (update database or data structure)
        pass  # Placeholder for the modification logic

    reservation = next((r for r in reservations if r['id'] == reservation_id), None)
    return render_template('modify_reservation.html', reservation=reservation)

@app.route('/modify_patient/<int:patient_id>', methods=['GET', 'POST'])
def modify_patient(patient_id):
    if request.method == 'POST':
        new_name = request.form.get('new_name')
        # Update patient information based on the form data
        pass  # Placeholder for the modification logic

    patient = next((p for p in patients if p['id'] == patient_id), None)
    return render_template('modify_patient.html', patient=patient)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

if __name__ == '__main__':   #he purpose of if __name__ == '__main__': is to provide a way to distinguish whether the current script is the main program being executed or if it's being imported as a module into another script. Anything within this block will only execute when the script is run directly.

	app.run(debug=True, host='0.0.0.0', port=80)

