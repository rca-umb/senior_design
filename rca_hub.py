# Team 1 UMB Senior Design '23-'24
# Updated code to take read data from drone XBees.

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import time

# Instantiate a local XBee node (this is the XBee device connected to this Pi
xbee = XBeeDevice("/dev/ttyUSB0", 115200)
xbee.open()

while True:
	# Read incoming XBee data
	try:
		xbee_message = xbee.read_data(timeout=5)
		print(xbee_message.data)
	except:
		print("Do data received")
