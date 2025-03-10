from flask import Flask, render_template, jsonify
from aircraft_manager import AircraftManager
import random
from aircraft_manager import AircraftStatus

app = Flask(__name__)
aircraft_manager = AircraftManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_status')
def get_status():
    return jsonify({
        'runway_status': aircraft_manager.get_runway_status(),
        'airborne_aircraft': aircraft_manager.get_airborne_aircraft(),
        'waiting_aircraft': aircraft_manager.get_waiting_aircraft()
    })

@app.route('/add_test_aircraft')
def add_test_aircraft():
    status_options = [AircraftStatus.EMERGENCY, AircraftStatus.LANDING, AircraftStatus.TAKEOFF]
    flight_number = f"FL{random.randint(100, 999)}"
    status = random.choice(status_options)
    aircraft_manager.add_aircraft(flight_number, status)
    return jsonify({'status': 'success', 'message': f'Added aircraft {flight_number} with status {status.name}'})

if __name__ == '__main__':
    app.run(debug=True)




