# Team 1 UMB Senior Design '23-'24
# Code to initialize and reconfigure drone mesh network as necessary
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import geopy.distance # function for determining accurate gps distance
from rca_hub import registry

# Maximum range for line-of-site communication bewteen two XBee units (m), needs to be measured experimentally
XBEE_RANGE = 100 

# Hub coordinates; there is no way to get this from hardware, but we can infere it from a drone we connect to
HUB_LOC = [0.0,0.0]

# Instantiate a local XBee node (this is the XBee device connected to this Pi
xbee = XBeeDevice("/dev/ttyUSB0", 115200)
xbee.open()

# Class for keeping track of a drone's physical location and relativity in the network for efficient networking
class DroneLocation:
	def __init__(self, address):
		self.addr = address
		self.name = registry[address]
		self.gps = [0.0,0.0]
		self.level = 0
	
	def gps_update(self, x, y):
		self.gps = [x, y]
			
	def set_level(self, coords):
		dist = gps_dist(self.gps, coords)
		if dist < XBEE_RANGE:
			self.level = 1
		elif dist < (XBEE_RANGE * 2):
			self.level = 2
		else:
			self.level = 0
			# missing_drone() 
				# TO DO: Add a function to try to find a missing drone

# Gets the distance between to GPS coordinates
def gps_dist(coords1, coords2):
	return geopy.distance.geodesic(coords1, coords2).m

# Initiates direct communication with a single drone
def init_drone(dl):

	
# The initial setup of the drone swarm
def init_swarm():
	try: 
		xbee.read_data(5)
		drone = xbee_message.remote_device.get_64bit_addr().address.hex() # string representation of byteaddress representation of 64bit address
		d1 = DroneLocation(drone)
		init_drone(d1)

	except:
		print("Could not connect to a drone after 5 seconds.")


