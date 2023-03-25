import requests
import argparse
import sys

# List the devices that are attached to the soma connect 
# If you have a U1 Device which I don't the API changed a bit 
# https://support.somasmarthome.com/hc/en-us/articles/360026064234-HTTP-API
def list_devices(host): 
	# Build the URL
	url = f"http://{host}:3000/list_devices"
	# Send the GET to the connect to get the attached devices 
	devices = requests.get(url)
	# Set up variables for the loop to store 
	r_devices = []
	# Stored for later use as I develop the script 
	r_names = []
	# Set the counter to 0 
	x = 0
	# Loop through each device and store the name and mac address 
	for shade in devices.json()['shades']:

		r_devices.append(devices.json()['shades'][x]['mac'])
		r_names.append(devices.json()['shades'][x]['name'])
		x += 1
	# Return the two lists 
	return r_devices, r_names
# Function for opening the shades 
def open_shade(host,mac):

	# If you have a U1 change to match its API 
	# https://support.somasmarthome.com/hc/en-us/articles/360026064234-HTTP-API

	url = f"http://{host}:3000/open_shade/{mac}"
	# Open the device one at a time 
	devices = requests.get(url)
# Function for closing the shades 
def close_shade(host,mac): 
	# If you have a U1 change to match its API 
	# https://support.somasmarthome.com/hc/en-us/articles/360026064234-HTTP-API

	url = f"http://{host}:3000/close_shade/{mac}"
	# Close the device one at a time 
	devices = requests.get(url)
# Function for listing the battery levels of the shades 
def list_battery(host, mac): 
	url = f"http://{host}:3000/get_battery_level/{mac}"
	battery_level = requests.get(url)
	return battery_level.json()['battery_percentage']
# Function for listing the state of the shades 
def shade_state(host,mac): 
	#get_shade_state
	url = f"http://{host}:3000/get_shade_state/{mac}"
	shade_state = requests.get(url)
	return shade_state.json()['position']
# Function for light levels of the shades 
def light_level(host,mac): 
	#get_light_level
	url = f"http://{host}:3000/get_light_level/{mac}"
	shade_state = requests.get(url)
	return shade_state.json()['light_level']

#
# MAIN function 
#
def main():
	# Argparse setup, need two arguments of the host, and action of close or open
	parser = argparse.ArgumentParser(description='Soma Connect Control ALL Shades')
	
	# Set up arguments
	parser.add_argument('host', type=str, help="The host ot connect to e.g.: 127.0.01")
	parser.add_argument('action',type=str, help="The action you want to perform: open, close, \
		battery, state, light")

	# Parse the arguments 
	args = parser.parse_args()
	# set the host to the passed in host and the action
	host = args.host
	action = args.action
	# store the names and mac address for each device 
	macs, names = list_devices(host)
	
	x = 0
	#for each device in the macs list, open or close it based on the action 
	for device in macs: 
		if action == "open": 
			open_shade(host, device)
		elif action == "close":
			close_shade(host, device)
		elif action == "battery":
			print(f"--- {names[x]} is {list_battery(host, device)}%")
			x += 1
		elif action == "state":
			position = shade_state(host, device)
			if position == 0: 
				s_pos = "Open"
			else: 
				s_pos = "Closed"
			print(f"--- {names[x]} is {s_pos}")
			x += 1 
		elif action == "light":
			print(f"--- {names[x]} light level {light_level(host, device)}")
			x += 1

		else:
			print(f"Wrong Option {action}")

if __name__ == "__main__":
    sys.exit(main())
