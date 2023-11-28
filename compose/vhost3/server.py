from flask import Flask, request  
from urllib.request import urlopen  
import json  


  #Admins: Can view and modify all reservations.
  #Secretaries: Can view and modify only certain reservations.

app = Flask(__name__) n.

@app.route('/') 
def index():
    return render_template('index.html', reservations=reservations)  

# Route for admins to view all reservations
@app.route('/admin/reservations')
def admin_reservations():
    # Logic to fetch admin reservations
    admin_reservations = [r for r in reservations if r['role'] == 'admin']     
    return render_template('admin_reservations.html', reservations=admin_reservations)

# Route for secretaries to view and modify certain reservations
@app.route('/secretary/reservations')
def secretary_reservations():
    secretary_reservations=[r for r in reservations if r['role']== 'secretary']
    return render_template('secretary_reservations.html',reservations=secretary_reservations)

#Route for admins and secretaries to modify a reservation
@app.route('/modify/<int:reservation_id>', methods=['GET', 'POST'])
if request.method == 'POST':
        # Handle modification (update database or data structure)


    reservation = next((r for r in reservations if r['id'] == reservation_id), None)
    return render_template('modify_reservation.html', reservation=reservation)

if __name__ == '__main__':  

	app.run(debug=True, host='0.0.0.0', port=80)
