import socket
import sys
import os
import time
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

# catch exceptions related to already bound ports, etc..
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
		#this will block the code execution until one comes in. Returns a new socket to use to communicate with the connected client
		print("Waiting for new client... ")
		client_socket, client_address = server_socket.accept()

		print("Client " + str(client_address) + " connected.")

		
		# receiving a request command
		request_type = client_socket.recv(4).decode().strip() 


		# PUT request_type
		if request_type == "PUT":
			print("request: " +"<"+request_type+">")

			# process the file name
			filename = client_socket.recv(1024).decode().strip()
			print("file name: " + "<"+filename+">")

			if os.path.exists(filename):
				print("File already exists.")
				client_socket.sendall("File already exists.".encode()) 
			else:
				# download file
				recv_file(client_socket, filename)
				print("File downloaded")

				# send SUCCESS
				client_socket.sendall("SUCCESS".encode()) 

			
		# GET request_type
		elif request_type == "GET":
			print("request: " +"<"+request_type+">")
			
			# process the file name
			filename = client_socket.recv(1024).decode().strip()
			print("file requested: " + "<"+filename+">")

			if not os.path.exists(filename):
				print("File not found.")
				client_socket.sendall("File not found.".encode())

			else:
				client_socket.sendall("Uploading".encode())
				time.sleep(0.05)
				send_file(client_socket, filename)
				print("File sent successfully.")
				

		# LIST request_type
		elif request_type == "LIST":
			print("request: " +"<"+request_type+">")
			send_listing(client_socket)
			print(f"posted LIST to {client_address[0]}:{client_address[1]} Successfully")

		if request_type:
			print(f"Finished handling {request_type} request from {str(client_address)}\n")
		else:
			print("Action not completed")


	# socket errors as well as errors related to user input.			
	except Exception as e:
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
