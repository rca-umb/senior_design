# Team 1 UMB Senior Design '23-'24
# Updated code to receive data from drones and predict fire. 

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import time
import numpy as np
import re
import tensorflow as tf

# Instantiate a local XBee node (this is the XBee device connected to this Pi
xbee = XBeeDevice("/dev/ttyUSB0", 115200)
xbee.open()
this_xbee = xbee.get_64bit_addr().address.hex() # 64bit address object -> bytearray -> string representation of hex value

# Keep record of each XBee's address
registry = {"0013a200420107ce": "Drone 1", "0013a200420107ef": "Drone 2", "0013a20042010691": "Hub"}

# Array to store values before ML processing
drone_data = np.zeros(shape=[2,3],dtype=np.float32)

# Load TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="/home/hub/Desktop/converted_model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

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

# Function to properly place data from drones into numpy array
def update_array(device, variable, value):
	row = 0
	col = 0
	if device == "Drone 1":
		row = 0
	elif device == "Drone 2":
		row = 1
	if variable == "Temperature":
		col = 0
	elif variable == "Humidity":
		col = 1
	elif variable == "Wind":
		col = 2
	else:
		return
	drone_data[row,col] = value

# Function to properly process data from drones
def read_data(message):
	that_xbee = xbee_message.remote_device.get_64bit_addr().address.hex() # string representation of byteaddress representation of 64bit address
	device = registry[that_xbee] # check which drone sent the data
	print('From ' + device + ': ' + xbee_message.data.decode()) 
	line = xbee_message.data.decode() # convert bytearray data to string
	variable = line.split()[0] # first token in line will be the variable
	variable = variable.translate({ord(i): None for i in ", ' ("}) 
	value = line.split()[-1] # last token in line will be the numerical value
	value = value.translate({ord(i): None for i in ", ' )"})
	update_array(device, variable, value)	

print(registry[this_xbee] + ': Now Running')
t = 5 # wait this many seconds to receive data
while True:
	# Read incoming XBee data
	try:
		xbee_message = xbee.read_data(t)
	except Exception as e:
		print("Timeout after " + str(t) + " seconds. Trying again...")
	read_data(xbee_message)
	pred1 = make_prediction(drone_data[0])
	print("Drone 1: " + str(pred1*100) + "% Chance of Fire")
	pred2 = make_prediction(drone_data[1])
	print("Drone 2: " + str(pred2*100) + "% Chance of Fire")
