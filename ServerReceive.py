# import necessary modules
import os
import socket
import tqdm
import time
from pathlib import Path


# importing user defined modules
import ApplicationOpener as AppO
import FileManager as fm
import EncryptDecrypt as ED
import CheckSumValidator as CSV


key = b'\xa2\xe8\xc3?\x0b}\xb6\xd4\xc1ZgN\x9a?zw'
# finds the Operating System used for the server
platform_num = AppO.find_platform()
default_path = fm.getDefaultDir()
destination_path = fm.MakeNewDirectory(platform_num)


# assigning HOST and PORT Number
HOST = "127.0.0.1"
PORT = 65432


# assign buffer_size as 1024 bits per Second
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"


# create a tcp server socket as s
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to the local ip address
s.bind((HOST, PORT))
# listen for incoming connections from the client
s.listen(5)
print(f"[+] Listening as {HOST}:{PORT}")
# accept the connection from the client
client_socket, address = s.accept()
# print the address of the connected client
print(f"[+] {address} is connected")
# receive the filename and file size from the client
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize, sender_checksum = received.split(SEPARATOR)
print(f"Received: {received}\n\nwhich can be organized as follows:\nfilename: {filename}, filesize: {filesize}, sender_checksum: {sender_checksum}")
# remove absolute path if there is
filename = os.path.basename(filename)
if platform_num != 1:
	filename = destination_path + r"/" + filename
else:
	filename = destination_path + r"\\" + filename
print("filename: ",filename)
# convert the file-size from strings to integer
filesize = int(filesize)
# start receiving the file from the client
progress = tqdm.tqdm(range(filesize), f"Received {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, 'wb') as file:
	while True:
		# read 1024 bytes from the socket (receive)
		bytes_read = client_socket.recv(BUFFER_SIZE)
		if not bytes_read:
			# nothing is received
			# file transmitting is done
			break
		# write to the file the bytes we just received
		file.write(bytes_read)
		# update the progress bar
		progress.update(len(bytes_read))
receiver_checksum = fm.receivefile(destination_path, filename, key)
print(f"receiver_checksum: {receiver_checksum}")
s.close()
Integrity = CSV.checkIntegrity(sender_checksum, receiver_checksum)
if Integrity != True:
	print("File Transmitted was incorrect o(╥﹏╥)")
	client_socket.sendall("File Transmitted was incorrect o(╥﹏╥)".encode())
else:
	print("File Trasmission was is successful ᕕ( ᐛ )ᕗ")
	client_socket.sendall("File Trasmission was is successful ᕕ( ᐛ )ᕗ".encode())
AppO.open_application(platform_num, filename)
