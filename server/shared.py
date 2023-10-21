import sys
import socket

def socket_to_screen(socket):
	"""Reads data from a passed socket and prints it on screen.

	Returns either when a newline character is found in the stream or the connection is closed.
        
	"""
	data = bytearray(1)

	"""
	 Loop for as long as data is received (0-length data means the connection was closed by the client).
	"""
	while some_condition:
		"""
		 Read up to 4096 bytes at a time; remember, TCP will return as much as there is
		 available to be delivered to the application, up to the user-defined maximum,
		 so it could as well be only a handful of bytes. This is the reason why we do
		 this in a loop; there is no guarantee that the line sent by the other side
		 will be delivered in one recv() call.
		"""
		data = socket.recv(4096)
		print(data.decode())
	
def keyboard_to_socket(socket):
	bytes_sent = socket.sendall(str.encode('kurwa'))
	return bytes_sent
