# herbie.py
# Author: Dennis Gieger
import glob
import os
import sys

try:
    sys.path.append(glob.glob('**/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


import carla
#from carla import ColorConverter as cc

import argparse
import collections
import datetime
import logging
import math
import random
import re
import weakref

import random
import time
# Komponenten import
from fahrzeug import Herbie
from komponenten.steuerung import Logitech_F710 as Steuerung
from komponenten.kamera import USB_kamera as Kamera

#from komponenten.pilot import Fahrer
from komponenten.pwm import PWM
from komponenten.datenspeicher import Datenspeicher
#from komponenten.webserver.server import WebServer

print('Herbie startet')


# First of all, we need to create the client that will send the requests
# to the simulator. Here we'll assume the simulator is accepting
# requests in the localhost at port 2000.
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Once we have a client we can retrieve the world that is currently
# running.
world = client.get_world()

# The world contains the list blueprints that we can use for adding new
# actors into the simulation.
blueprint_library = world.get_blueprint_library()

# Now let's filter all the blueprints of type 'vehicle' and choose one
# at random.
bp = random.choice(blueprint_library.filter('vehicle'))

# A blueprint contains the list of attributes that define a vehicle
# instance, we can read them and modify some of them. For instance,
# let's randomize its color.
color = random.choice(bp.get_attribute('color').recommended_values)
bp.set_attribute('color', color)

# Now we need to give an initial transform to the vehicle. We choose a
# random transform from the list of recommended spawn points of the map.
transform = random.choice(world.get_map().get_spawn_points())

# So let's tell the world to spawn the vehicle.
vehicle = world.spawn_actor(bp, transform)

# It is important to note that the actors we create won't be destroyed
# unless we call their "destroy" function. If we fail to call "destroy"
# they will stay in the simulation even after we quit the Python script.
# For that reason, we are storing all the actors we create so we can
# destroy them afterwards.
actor_list.append(vehicle)
print('created %s' % vehicle.type_id)

# Let's put the vehicle to drive around.
vehicle.set_autopilot(True)


# Instanziierung der Kopmponenten
herbie = Herbie()
steuerung = Steuerung()
#kamera = Kamera(airsim)

#fahrer = Fahrer()
pwm = PWM(vehicle)
#datenspeicher = Datenspeicher()
#server = WebServer()

print('Komponenten laden...')

"""
Komponenten werden nach dem fogendem Schema angelegt:
	herbie.hinzufuegen(komponente, eingang=['eingang_name',...], ausgang=['ausgang_name',...], ausfuehren_parallel = True or False)
"""

# Hinzufügen der Komponenten
herbie.hinzufuegen(steuerung, ausgang=['beschleunigung','lenkung','aufnahme','modus','speichern','programm_ende'], ausfuehren_parallel=True)
#herbie.hinzufuegen(kamera, ausgang=['kamera'], ausfuehren_parallel=True)


#herbie.hinzufuegen(fahrer, eingang=['kamera','beschleunigung','lenkung','modus'], ausgang=['lenkung','beschleunigung'], ausfuehren_parallel=True)

herbie.hinzufuegen(pwm, eingang=['beschleunigung','lenkung'], ausfuehren_parallel=True)
#herbie.hinzufuegen(datenspeicher, eingang=['kamera','beschleunigung','lenkung','aufnahme','speichern','besch_x','besch_y','besch_z','gyro_x','gyro_y','gyro_z'], ausfuehren_parallel=True)
#herbie.hinzufuegen(server, eingang=['kamera','beschleunigung','lenkung'],ausfuehren_parallel=True)

# Hauptschleife starten
herbie.starten()