# Team 1 UMB Senior Design '23-'24
# Updated code to take data from Arduino and send to a different XBee device.
# AFTER SYSTEM BOOT, UNPLUG ARDUINO AND XBEE. PLUG IN XBEE FIRST, THEN ARDUINO

import serial
import re
import numpy as np
import tflite_runtime.interpreter as tflite
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
data_packet = {"Target": "Hub", "GPS": [0.0,0.0], "Prediction": None}
drone_data = np.array([1,3],np.float32)

# Load TensorFlow Lite model
interpreter = tflite.Interpreter(model_path="/home/drone1/senior_design/converted_model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# Function to read Arduino serial output one line at a time
def read_arduino():
	if(arduino_serial.in_waiting > 0):
		line = arduino_serial.readline().decode('utf-8').rstrip()
		if "Temperature" in line:
			temp_match = re.search(r"Temperature \(F\): ([\d.]+)", line)
			if temp_match:
				drone_data[0] = float(temp_match.group(1))
		elif "Humidity" in line:
			humi_match = re.search(r"Humidity \(% RH\): ([\d.]+)", line)
			if humi_match:
				drone_data[1] = float(humi_match.group(1))
		elif "Wind Speed" in line:
			wind_match = re.search(r"Wind Speed \(mph\): ([\d.]+)", line)
			if wind_match:
				drone_data[2] = float(wind_match.group(1))
		return line
	return None

# Function to make prediction based on model
def make_prediction(data):
	# Reshape data
	data = np.reshape(data, (1, -1))
	
	# Set input tensor
	interpreter.set_tensor(input_details[0]['index'], data)

	# Run inference
	interpreter.invoke()

	# Get the output tensor if needed
	prediction = interpreter.get_tensor(output_details[0]['index'])
	return prediction

# Function to send data to other XBees in the network
def send_packet():
	try:
		xbee.send_data_broadcast(data_packet) # transmit just the gps coords
		print("Target:" + data_packet["Target"] + ",GPS:" + data_packet["GPS"] +",Fire:" + data_packet["Prediction"]) # Print to pi terminal for testing
	except:
		print("Transmit Error")

print(registry[this_xbee] + ': Now Running') # Shows in terminal which device is running					  
try:
	while True:
		data = read_arduino()
		if data: # Only send packet when data from the Arduino has been read (ensures no repeats)
			fire = make_prediction(drone_data)
			data_packet["Prediction"] = fire
		send_packet()
			
except KeyboardInterrupt:
	arduino_serial.close()

        
        
