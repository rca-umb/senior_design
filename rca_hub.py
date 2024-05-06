# Team 1 UMB Senior Design '23-'24
# Updated code to receive data from drones and predict fire. 

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import time
import re
import geopy.distance # function for determining accurate gps distance

# Maximum range for line-of-site communication bewteen two XBee units (m), needs to be measured experimentally
XBEE_RANGE = 100 

# Hub coordinates; there is no way to get this from software, must be determined ahead of time (maybe we could use the old GPS module?) 
target = [0.0,0.0]

# Instantiate a local XBee node (this is the XBee device connected to this Pi
xbee = XBeeDevice("/dev/ttyUSB0", 115200)
xbee.open()
this_xbee = xbee.get_64bit_addr().address.hex() # 64bit address object -> bytearray -> string representation of hex value

# Keep record of each XBee's address
registry = {"0013a200420107ce": "Drone 1", "0013a200420107ef": "Drone 2", "0013a20042010691": "Hub"}

# Drone location objects
d1 = None
d2 = None

# Class for keeping track of a drone's physical location and relativity in the network for efficient networking
class DroneLocation:
	def __init__(self, address):
		self.addr = address
		self.name = registry[address]
		self.gps = [0.0,0.0]
		self.distance2go = 0
	
	def gps_update(self, x, y):
		self.gps = [x, y]
		self.target_update()
			
	def target_update(self):
		dist = gps_dist(self.gps, target)
		self.distance2go = dist

# Gets the distance between to GPS coordinates
def gps_dist(coords1, coords2):
	return geopy.distance.geodesic(coords1, coords2).m
	
# The initial setup of the drone swarm
def init_swarm(time):
	global d1, d2
	config = True
	while config:
		try: 
			xbee_message = xbee.read_data(time)
			drone = xbee_message.remote_device.get_64bit_addr().address.hex() # string representation of byteaddress representation of 64bit address
			if registry[drone] == registry[0]:
				d1 = DroneLocation(drone)
				coords = re.findall(r"[-+]?\d*\.\d+|\d+", xbee_message.data.decode())
				x = coords[0]
				y = coords[1]
				d1.gps_update(float(x),float(y))
			elif registry[drone] == registry[1]:
				d2 = DroneLocation(drone)
				coords = re.findall(r"[-+]?\d*\.\d+|\d+", xbee_message.data.decode())
				x = coords[0]
				y = coords[1]
				d2.gps_update(float(x),float(y))
			else:
				print("Data received from unidentified sender: " + drone)
			print("Established connection to: " + registry[drone])
			if (d1 != None) and (d2 != None): # configuration done
				config = False
		except:
			print("Could not connect to a drone after 5 seconds.")
	print("Successful established inital connections") # test up to here

# Function to properly process data from drones
def read_data(message):
	that_xbee = message.remote_device.get_64bit_addr().address.hex() # string representation of byteaddress representation of 64bit address
	device = registry[that_xbee] # check which drone sent the data
	print('From ' + device + ': ' + message.data.decode()) 

# Function to start a new mission
def new_mission():
	global target
	try:
		waypoint = input("Enter the coordinates of the location to monitor in the form latitude longitude: ")
		target[0] = waypoint.split(" ")[0]
		target[1] = waypoint.split(" ")[1]
	except:
		print("Invalid input. Please enter the coordinates in the form latitude longitude.")
		return
	if (d1.distance2go <= d2.distance2go):
		swarm_takeoff(1)
	else:
		swarm_takeoff(2)

# Function to send instructions to drones
def swarm_takeoff(order):


print(registry[this_xbee] + ': Now Running')
t = 5 # wait this many seconds to receive data
init_swarm(t)
while True:
	try:
		new_mission()
		xbee_message = xbee.read_data(t)
	except:
		print("Received no data after " + str(t) +" seconds.")
	read_data(xbee_message)


	
