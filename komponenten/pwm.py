# pwm.py
# Author: Dennis Gieger

# Bibliotheken import
from __future__ import division
import carla
# Basis Klasse
class BasisPWM:
    programm_laeuft = True
    beschleuniging = 0
    lenkung = 0

	# Methode für die ein und ausgabe 
    def ausfuehren_parallel(self, beschleuniging, lenkung):
        self.beschleuniging = beschleuniging
        self.lenkung = lenkung



	# Thread beenden
    def beenden(self):
        self.programm_laeuft = False
        print('PWM beenden')
        time.sleep(.5)


# Klasse zur Regelung des Motors und Lenkservos für Raspberry Pi
class PWM(BasisPWM):
    name = "PWM"

	# PWM initialisierung
    def __init__(self, vehicle):
        self.vehicle = vehicle
        

	# Endlosschleife für die Regelung
    def aktualisieren(self):
        while self.programm_laeuft:
            
            print(self.beschleuniging,self.lenkung)
            self.vehicle.apply_control(carla.VehicleControl(self.beschleuniging, self.lenkung))
