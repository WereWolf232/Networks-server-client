import socket
import sys
import os
from shared import *


# input error checking
if len(sys.argv) < 4:
	print("Usage: python client.py <hostname> <port> <put 'filename'|get 'filename'|list>")
	sys.exit(1)

# port number error checking
port = int(sys.argv[2])
if port < 1024 or port > 65535:
	print("port number out of bounds")
	sys.exit(1)


host = sys.argv[1]
server_address = (host,port)
command = sys.argv[3]
filename = sys.argv[4] if command in ["put", "get"] else None


# Create the socket with which we will connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
	print("Connecting to " + str(server_address) + "... ")

	# Connect our socket to the server. This will actually bind our socket to a port on our side. 
	client_socket.connect(server_address)
	print("Connected to server")

except Exception as e:
	print("ina'al haolam" + e)
	exit(1)

# this is where the commands are going to start
# try-except block to account for socket errors as well as errors related to user input.
try:
	# PUT command
	if command == "put":
		client_socket.sendall("PUT".encode())
		print("file uploaded succesfully")
	# GET command
	elif command == "get":
		client_socket.sendall("GET".encode())
		print("file downloaded succesfully")



	# LIST command
	elif command == "list":
		client_socket.sendall("LIST".encode())

		# receiving filename list from server
		recv_listing(client_socket)
		print(f"got LIST from {host}:{port} Successfully")



#If an error occurs or the server closes the connection, call close().
finally:
	client_socket.close()

# Exit with a zero value, to indicate success
exit(0)