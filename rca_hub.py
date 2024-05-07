# Team 1 UMB Senior Design '23-'24
# Updated code to receive data from , determine takeoff order, and send instructions to the drones.

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import time
import re
import geopy.distance # function for determining accurate gps distance

# Maximum range for line-of-site communication bewteen two XBee units (m). From manual, maximum is 1200
XBEE_RANGE = 1000 

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

# Data to be sent to other XBees
data_packet = {"Target": None, "Action": 0, "GPS": [0.0,0.0]}

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
	config = True
	while config:
		try: 
			xbee_message = xbee.read_data(time)
			drone = xbee_message.remote_device.get_64bit_addr().address.hex() # string representation of byteaddress representation of 64bit address
		except Exception as e:
			print("Could not connect to a drone after 5 seconds: " + str(e))
		update_location(xbee_message, drone)
		print("Established connection to: " + registry[drone])
		if (d1 != None) and (d2 != None): # configuration done
			config = False
	print("Successful established inital connections") # test up to here


# Function to update DroneLocation object with new coordinates
def update_location(message, device):
	global d1, d2
	if registry[device] == "Drone 1":
		d1 = DroneLocation(device)
		packet = message.data.decode()
		x = packet.split(":")[1]
		y = packet.split(":")[2]
		d1.gps_update(float(x),float(y))
	elif registry[device] == "Drone 2":
		d2 = DroneLocation(device)
		packet = message.data.decode()
		x = packet.split(":")[1]
		y = packet.split(":")[2]
		d2.gps_update(float(x),float(y))
	else:
		print("Data received from unidentified sender: " + device)

# Function to properly process data from drones
def read_data(message):
	drone = message.remote_device.get_64bit_addr().address.hex() # string representation of byteaddress representation of 64bit address
	update_location(message, drone)
	fire = 100.0*float((message.data.decode()).split(":")[3])
	if (fire > 75):
		for addr in registry:
			if addr == drone:
				continue
			elif registry[addr] == "Hub":
				continue
			else:
				packet = registry[addr] + ":" + str(fire) + "% chance of fire at " + registry[drone]
				xbee.send_data_broadcast(packet)
				print(packet) 
	else:
		print('From ' + registry[drone] + ': ' + message.data.decode()) 


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
	if order == 1:
		data_packet["Target"] = "Drone 1"
		data_packet["Action"] = 1
		data_packet["GPS"] = target
		send_packet()
		time.sleep(5)
		data_packet["Target"] = "Drone 2"
		data_packet["Action"] = 1
		data_packet["GPS"] = target #todo: change target GPS
		send_packet()
	elif order == 2:
		data_packet["Target"] = "Drone 2"
		data_packet["Action"] = 1
		data_packet["GPS"] = target
		send_packet()
		time.sleep(5)
		data_packet["Target"] = "Drone 1"
		data_packet["Action"] = 1
		data_packet["GPS"] = target #todo: change target GPS
		send_packet()
	else:
		print("Invalid argument given for takeoff order.")

# Function to transmit data to drones
def send_packet():
	transmit = True
	while (transmit):
		try:
			xbee.send_data_broadcast(data_packet["Target"] + ":" + str(data_packet["Action"]) + ":" + str(data_packet["GPS"][0]) + ":" + str(data_packet["GPS"][1]))
			transmit = False
		except Exception as e:
			print("Transmit Error due to: " + str(e))


print(registry[this_xbee] + ': Now Running')
t = 60 # wait this many seconds to receive data
init_swarm(t)
new_mission()
while True:
	try:
		xbee_message = xbee.read_data(t)
		read_data(xbee_message)
	except Exception:
		print("Received no data after " + str(t) +" seconds.")
		print(e)
	


	
