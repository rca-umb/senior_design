# Team 1 UMB Senior Design '23-'24
# Updated code to take data from Arduino and send to a different XBee device.
# AFTER SYSTEM BOOT, UNPLUG ARDUINO AND XBEE. PLUG IN XBEE FIRST, THEN ARDUINO

import serial
import time
import datetime
import re
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress


# Connect to Arduino through Serial communication
arduino_serial = serial.Serial(port="/dev/ttyUSB1", baudrate=57600, timeout=1)

# Instantiate a local XBee node (this is the XBee device connected to this Pi)
xbee = XBeeDevice("/dev/ttyUSB0", 115200)
xbee.open()
this_xbee = xbee.get_64bit_addr().address.hex() # 64bit address object -> bytearray -> string representation of hex value

# Keep record of each XBee's address
registry = {"0013a200420107ce": "Drone 1", "0013a200420107ef": "Drone 2", "0013a20042010691": "Hub"}

# Data to be sent to other XBees
data_packet = {"Time": None, "Temperature": None, "Humidity": None, "Wind Speed": None, "GPS": None}

# Function to read Arduino serial output one line at a time
def read_arduino():
	if(arduino_serial.in_waiting > 0):
		line = arduino_serial.readline().decode('utf-8').rstrip()
		if "Temperature" in line:
			temp_match = re.search(r"Temperature \(F\): ([\d.]+)", line)
			if temp_match:
				data_packet["Temperature"] = float(temp_match.group(1))
		elif "Humidity" in line:
			humi_match = re.search(r"Humidity \(% RH\): ([\d.]+)", line)
			if humi_match:
				data_packet["Humidity"] = float(humi_match.group(1))
		elif "Wind Speed" in line:
			wind_match = re.search(r"Wind Speed \(mph\): ([\d.]+)", line)
			if wind_match:
				data_packet["Wind Speed"] = float(wind_match.group(1))
		return line
	return None

# Function to send data to other XBees in the network
def send_packet():
	string_packet = ''
	data_packet["Time"] = datetime.datetime.now().isoformat(timespec='milliseconds') # Update data packet with current time in ISO format
	for item in data_packet.items(): # XBee cannot send dictionary, so convert it to a string
		try:
			xbee.send_data_broadcast(str(item))
			print(item) # Print to pi terminal for testing
		except:
			print("Transmit Error")

print(registry[this_xbee] + ': Now Running') # Shows in terminal which device is running					  
try:
	while True:
		data = read_arduino()
		if data: # Only send packet when data from the Arduino has been read (ensures no repeats)
			send_packet()
			
except KeyboardInterrupt:
	arduino_serial.close()

        
        
