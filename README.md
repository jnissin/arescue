# Firmware rescue tool for ASUS RT series routers for Linux/OSX

## Purpose

This script is intended to function as the firmware rescue tool for ASUS RT series routers for Linux/OSX as ASUS does not provide one.
The script is based on the instructions from [https://chrishardie.com/2013/02/asus-router-firmware-windows-mac-linux/](https://chrishardie.com/2013/02/asus-router-firmware-windows-mac-linux/) and personal experience with an ASUS RT-N56U router. Keep in mind this script has been tested with one ASUS RT-N56U router so it is imperative that you understand that this script is in no way an official tool provided by ASUS or a well tested piece of software by any means.

## Dependencies

* Python 2.6
* [netifaces](https://pypi.python.org/pypi/netifaces)
* [tftpy](http://tftpy.sourceforge.net/)

## Usage

If you are planning to use this script with your router I assume you know what your are doing. In case the program needs to setup your network settings the program might need sudo rights to use the ´ifconfig´. In this case the program will likely report something like ´ifconfig: down: permission denied´.

0. Make sure you have python and the above dependencies installed in your local environment
1. Download the latest firmware for your router from [https://support.asus.com](https://support.asus.com)
2. Read the following article [https://chrishardie.com/2013/02/asus-router-firmware-windows-mac-linux/](https://chrishardie.com/2013/02/asus-router-firmware-windows-mac-linux/) to understand what you are doing
3. Follow your router's user manual to set your router into rescue mode
4. Preferrably set your network configuration manually to the example network configuration described below
5. Launch the script ./python arescue.py --firmware <path_to_your_firmware_file>

If the default network configuration doesn't work the script attempts a couple of different local IP addresses for your machine. From personal experience I can say that my ASUS RT-N56U router wanted my local machine's IP address to be explicitly ´192.168.1.11´ for some weird reason. I used Wireshark to detect the ARP requests coming from my router asking who is ´192.168.1.11´. Despite my machine answering to the request since the default network mask covered the address for my machine the router didn't accept it. It only accepted the connection when my local IP address was set explicitly to '192.168.1.11'.

## Example network configuration

You need to setup your network configuration manually. Any IP address for the machine from the 192.168.1.0/24 block is good. An example configuration would be:

	IP address: 192.168.1.2
	Netmask: 255.255.255.0
	Gateway: 192.168.1.0

## Contributing

The script is licensed under the GPL license. Feel free to edit it in anyway you want and if you feel like it send a pull request for any improvements.
