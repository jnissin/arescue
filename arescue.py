# ASUS RT series router firmware rescue tool for Linux/OSX
#
# Dependencies: 
#     netifaces -- https://pypi.python.org/pypi/netifaces
#     tftpy -- http://tftpy.sourceforge.net/
#
# Based on instructions from and personal experience:
#     https://chrishardie.com/2013/02/asus-router-firmware-windows-mac-linux/
#
# Created on:
#     26.7.2015 by Joonas Nissinen

import sys
import os
import argparse
import netifaces
import time
from subprocess import call

DEBUG = True

# Prints debug to stdout if debug prints are enabled
def dprint(str):
	if (DEBUG):
		print(str)

# Pings an IP address to test for response
def pingIp(ip):
	dprint("INFO: Pinging address: " + ip)
	response = call(["ping", "-c", "1", ip])

	if (response == 0):
		dprint("INFO: Router responded successfully")
		return True
	else:
		dprint("ERROR: No response from router")
		return False

def printConnectionInfo(hostname, ipaddr, netmask, gateway):
	dprint("INFO: Hostname: " + hostname)
	dprint("INFO: IP: " + ipaddr)
	dprint("INFO: Netmask: " + netmask)
	dprint("INFO: Gateway: " + gateway)	

# Validates the network configuration, if it doesn't work tries to fix it.
# If connection to the router can be established attempts to upload the firmware.
def uploadFirmware(hostname, interface, firmware, timeout):
	dprint("INFO: Validating network configuration")

	info = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
	netmask = info['netmask']
	ipaddr = info['addr']
	gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]

	printConnectionInfo(hostname, ipaddr, netmask, gateway)

	if (pingIp(hostname)):
		dprint("INFO: Network configuration validated")
		uploadBinaryUsingTftp(hostname, firmware, timeout)
	else:
		dprint("ERROR: Invalid network configuration")

		# Prompt the user whether they want to continue
		ans = raw_input("Sometimes the router may respond to different client IP addresses,\nthe application can try a few default IP configurations for the connection,\nwould you like to try? (Y/N)\n")
		ans = str(ans)

		if (ans.lower().strip() != "y"):
			return False

		# Setup a basic configuration and loop through a couple of possible IP addresses
		# as your address, sometimes the ASUS router wants a specific IP address from the
		# conencting machine
		default_hostname = "192.168.1.1"
		default_gateway = "192.168.1.0"
		default_netmask = "255.255.255.0"
		default_ipaddr = "192.168.1."

		# Attempts IP addresses 192.168.1.2 - 192.168.1.25
		for i in range(2,26):
			testip = default_ipaddr + str(i)

			dprint("INFO: Attempting configuration")
			printConnectionInfo(default_hostname, testip, default_netmask, default_gateway)		

			# Setup the network configuration
			call(["ifconfig", interface, "down"])
			call(["ifconfig", interface, testip, "netmask", default_netmask, "up"])

			# Sleep so the network has enough time to get back up
			time.sleep(2)
			call(["route", "add", "default", default_gateway])

			# Attempt to ping the router
			if (pingIp(default_hostname)):
				uploadBinaryUsingTftp(default_hostname, firmware, timeout)
				return True

	dprint("ERROR: Could not upload firmware to the router")
	return False

def validateFirmwareFilePath(fpath):
	dprint("INFO: Validating the firmware file path")
	if (not os.path.isfile(fpath)):
		dprint("ERROR: Invalid firmware file path: " + fpath)
		return False
	return True

def uploadBinaryUsingTftp(hostname, firmware, timeout):
	dprint("INFO: Uploading firmware to router")
	dprint("INFO: Please observer your router LEDs to validate that the upload is in progress")
	client = tftpy.TftpClient(hostname, 69)
	client.upload(firmware.split('/')[-1], firmware, None, timeout)
	dprint("INFO: Upload complete")

def main():
	# Parse the command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("--firmware", help="Path to the firmware file", required=True)
	parser.add_argument("--hostname", help="The IP address of the ASUS router", required=False, type=str, default="192.168.0.1")
	parser.add_argument("--timeout", help="Timeout value for the TFTP upload", required=False, type=int, default=120)
	parser.add_argument("--interface", help="The connection interface", required=False, type=str, default="en0")
	parser.add_argument("--debug", help="Enable debug prints", required=False, type=bool, default=True)
	args = parser.parse_args()

	hostname = args.hostname
	firmware = args.firmware
	timeout = args.timeout
	interface = args.interface
	DEBUG = args.debug

	# Validate the firmware file path
	if (not validateFirmwareFilePath(firmware)):
		sys.exit(1)

	# Attempt to upload the firmware
	if (not uploadFirmware(hostname, interface, firmware, timeout)):
		sys.exit(1)

	dprint("INFO: Firmware upload complete, please restart your router")

if __name__ == "__main__":
	main()
