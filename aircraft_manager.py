from enum import Enum
from datetime import datetime
import queue
import threading

class AircraftStatus(Enum):
    EMERGENCY = 0
    LANDING = 1
    TAKEOFF = 2

class Aircraft:
    def __init__(self, flight_number, status):
        self.flight_number = flight_number
        self.status = status
        self.timestamp = datetime.now()
        
    def to_dict(self):
        return {
            'flight_number': self.flight_number,
            'status': self.status.name,
            'timestamp': self.timestamp.strftime('%H:%M:%S')
        }

class AircraftManager:
    def __init__(self):
        self.runway_in_use = False
        self.emergency_queue = []
        self.landing_queue = []
        self.takeoff_queue = []
        self.airborne_aircraft = []
        self.current_aircraft = None
        self.runway_occupation_time = 2  # Time in seconds for runway operation
        
    def process_runway(self):
        """Process the next aircraft based on priority"""
        if self.runway_in_use:
            return
            
        # Check queues in priority order
        if self.emergency_queue:
            self.current_aircraft = self.emergency_queue.pop(0)
        elif self.landing_queue:
            self.current_aircraft = self.landing_queue.pop(0)
        elif self.takeoff_queue:
            self.current_aircraft = self.takeoff_queue.pop(0)
        else:
            return
            
        self.runway_in_use = True
        # Schedule runway release
        threading.Timer(self.runway_occupation_time, self.release_runway).start()
        
    def release_runway(self):
        """Release the runway after operation is complete"""
        self.runway_in_use = False
        self.current_aircraft = None
        self.process_runway()  # Process next aircraft if any
        
    def add_aircraft(self, flight_number, status):
        aircraft = Aircraft(flight_number, status)
        
        if status == AircraftStatus.EMERGENCY:
            self.emergency_queue.append(aircraft)
        elif status == AircraftStatus.LANDING:
            self.landing_queue.append(aircraft)
        elif status == AircraftStatus.TAKEOFF:
            self.takeoff_queue.append(aircraft)
            
        # Try to process new aircraft
        self.process_runway()
            
    def get_runway_status(self):
        return {
            'in_use': self.runway_in_use,
            'current_aircraft': self.current_aircraft.to_dict() if self.current_aircraft else None
        }
        
    def get_airborne_aircraft(self):
        return [aircraft.to_dict() for aircraft in self.landing_queue + self.emergency_queue]
        
    def get_waiting_aircraft(self):
        return [aircraft.to_dict() for aircraft in self.takeoff_queue] 