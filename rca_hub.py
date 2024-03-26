# Team 1 UMB Senior Design '23-'24
# Updated code to take read data from drone XBees.

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import time

# Instantiate a local XBee node (this is the XBee device connected to this Pi
xbee = XBeeDevice("/dev/ttyUSB0", 115200)
xbee.open()
this_xbee = xbee.get_64bit_addr().address.hex() # 64bit address object -> bytearray -> string representation of hex value

# Keep record of each XBee's address
registry = {"0013a200420107ce": "Drone 1", "0013a200420107ef": "Drone 2", "0013a20042010691": "Hub"}

print(registry[this_xbee] + ': Now Running')
t = 1
while True:
	# Read incoming XBee data
	try:
		xbee_message = xbee.read_data(timeout=t)
		that_xbee = xbee_message.remote_device.get_64bit_addr().address.hex()
		print('From ' + registry[that_xbee] + ': ' + xbee_message.data)
	except:
		if (t < 120):
			t = t + 1
		print("No data received after " + str(t) + " seconds")
