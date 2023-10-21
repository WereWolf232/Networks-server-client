import socket
import sys
import os
from shared import *


# input error checking
if len(sys.argv) < 4:
	print("Usage: python client.py <hostname> <port> <put 'filename'|get 'filename'|list>")
	sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
server_address = (host,port)
command = sys.argv[3]
filename = sys.argv[4] if command in ["put", "get"] else None

# Create the socket with which we will connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

""" 
 Enclose the connect() call in a try-except block to catch
 exceptions related to invalid/missing command-line arguments, 
 port number out of range, etc. Ideally, these errors should 
 have been handled separately.
"""
try:
	print("Connecting to " + server_address + "... ")

	"""
	 Connect our socket to the server. This will actually bind our socket to
	 a port on our side; the port number will most probably be in the
	 ephemeral port number range and may or may not be chosen at random
	 (depends on the OS). The connect() call will initiate TCP's 3-way
	 handshake procedure. On successful return, said procedure will have
	 finished successfully, and a TCP connection to the server will have been
	 established.
	"""
	client_socket.connect(server_address)
	
	print("Connected. Now chatting...")
except Exception as e:
	# Print the exception message
	print(e)
	# Exit with a non-zero value, to indicate an error condition
	exit(1)

"""
 Surround the following code in a try-except block to account for
 socket errors as well as errors related to user input. Ideally
 these error conditions should be handled separately.
"""
try:
	# Loop until either the server closes the connection or the user requests termination
	while True:
		# First, read data from keyboard and send to server
		bytes_sent = keyboard_to_socket(client_socket)
		if bytes_sent == 0:
			print("User-requested exit.")
			break

		# Then, read data from server and print on screen
		bytes_read = socket_to_screen(client_socket, server_address_str)
		if bytes_read == 0:
			print("Server closed connection.")
			break

finally:
	"""
	 If an error occurs or the server closes the connection, call close() on the
	 connected socket to release the resources allocated to it by the OS.
	"""
	client_socket.close()

# Exit with a zero value, to indicate success
exit(0)
