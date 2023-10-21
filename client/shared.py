import sys
import os
import socket

def send_file():
    pass

def recv_file():
	pass

def send_listing(socket):
    listing = '\n'.join(os.listdir())
    socket.sendall(listing.encode())

def recv_listing(socket):
    listing = socket.recv(4096).decode()
    print(listing)