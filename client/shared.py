import sys
import os
import socket

def send_file(socket,filename):
    with open(filename, 'rb') as f:
    	socket.sendfile(f)

def recv_file(socket,filename):
	with open(filename, 'wb') as f:
		while True:
			data = socket.recv(4096)  # receive data in chunks
			if not data:  # no more data to receive
				break
			f.write(data)

def send_listing(socket):
    listing = '\n'.join(os.listdir())
    socket.sendall(listing.encode())

def recv_listing(socket):
    listing = socket.recv(4096).decode()
    print("\nFiles on server: ")
    print(listing + "\n")