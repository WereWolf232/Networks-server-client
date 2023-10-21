import socket
import sys
import os
from shared import *


# input error checking
if len(sys.argv) != 2:
	print("Usage: python server.py <port>")
	sys.exit(1)

# port number error checking
port = int(sys.argv[1])
if port < 1024 or port > 65535:
	print("port number out of bounds")
	sys.exit(1)


# Create the socket on which the server will receive new connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# catch  exceptions related to already bound ports, etc..
try:
	server_socket.bind(("0.0.0.0", int(sys.argv[1])))
	server_socket.listen(5)

except Exception as e:
	print(e)
	sys.exit(1)

print(f"Server up and running on {socket.gethostbyname(socket.gethostname())}:{port}")

# Loop forever (or at least for as long as no fatal errors occur)
while True:
	try:
		print("Waiting for new client... ")
		
		"""
		 Dequeue a connection request from the queue created by listen() earlier.
		 If no such request is in the queue yet, this will block the code execution until one comes
		 in. Returns a new socket to use to communicate with the connected client
		 plus the client-side socket's address (IP and port number).
		"""
		client_socket, client_address = server_socket.accept()
		client_address_str = str(client_address) # Translate the client address to a string (to be used shortly)

		print("Client " + client_address_str + " connected.")

		# Loop until either the client closes the connection or the user requests termination
		while True:
			# First, read data from client and print on screen
			bytes_read = socket_to_screen(client_socket, client_address_str)
			if bytes_read == 0:
				print("Client closed connection.")
				break

			# Then, read data from user and send to client
			bytes_sent = keyboard_to_socket(client_socket)
			if bytes_sent == 0:
				print("User-requested exit.")
				break


	# socket errors as well as errors related to user input.			
	except(e):
		print(e)
		sys.exit(1)
		
	finally:
		"""
		 If an error occurs or the client closes the connection, call close() on the
		 connected socket to release the resources allocated to it by the OS.
		"""
		client_socket.close()

# Close the server socket as well to release its resources back to the OS
server_socket.close()

# Exit with a zero value, to indicate success
exit(0)
