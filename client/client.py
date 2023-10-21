import socket
import sys
import os
import time
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
	print(e)
	sys.exit(1)


# try-except block to account for socket errors as well as errors related to user input.
try:
	print("request: " +"<"+command+">")

	# PUT command
	if command == "put":

		# error checking that file exists
		if not os.path.exists(filename):
			print(f"Local filename <{filename}> not found.")
			sys.exit(1)

		# sending PUT command to server
		client_socket.sendall("PUT".encode())

		# delay so the command and filename sending don't go to the same stream
		# this is the simplest and easiest solution for our purposes
		time.sleep(0.05) 

		client_socket.sendall(filename.encode())

		time.sleep(0.05) 

		# send the actual file contents
		send_file(client_socket,filename)

		# I finished sending, no need for outgoing data anymore
		client_socket.shutdown(socket.SHUT_WR)

		response = client_socket.recv(1024).decode().strip()
		if response == "File already exists.":
			print(f"File <{filename}> already exists.")
		else:
			print(f"File <{filename}> sent successfully")
			

	# GET command
	elif command == "get":
		# check if file already exists in current folder
		if os.path.exists(filename):
			print("Local filename <{filename}> already exists.")
			sys.exit(1)

		# sending command to server
		client_socket.sendall("GET".encode())

		time.sleep(0.05) 

		# sending filename name to server
		client_socket.sendall(filename.encode())

		client_socket.shutdown(socket.SHUT_WR)


		response = client_socket.recv(1024).decode().strip()
		if response == "File not found.":
			print("File <{filename}> not found.")
			sys.exit(1)
		else:
			recv_file(client_socket,filename)
			print("File <{filename}> received successfully")


	# LIST command
	elif command == "list":
		client_socket.sendall("LIST".encode())

		# receiving filename list from server
		recv_listing(client_socket)
		print(f"got LIST from {host}:{port} Successfully")


#If an error occurs or the server closes the connection, call close().
finally:
	print("Connection Closed")
	client_socket.close()

# Exit with a zero value, to indicate success
sys.exit(0)