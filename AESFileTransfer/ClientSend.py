# import necessary modules
import os
import socket
import tqdm
from zipfile import ZipFile
from pathlib import Path
from tkinter.messagebox import showinfo
from rich.progress import Progress
import time


# IMPORT necessary USER defined modules
import FileManager as fm
import EncryptDecrypt as ED
import CheckSumValidator as CSV
import ApplicationOpener as AppO
import GraphicalUserInterface as GUI


# key for encryption/ decryption
key = b'\xa2\xe8\xc3?\x0b}\xb6\xd4\xc1ZgN\x9a?zw'
# a variable which will store the data in the encrypted file
enc_data = b""
# get the name of the os
platform_num = AppO.find_platform()


# assigning HOST and PORT Number of the server
HOST = "127.0.0.1"
PORT = 65432

SERVER_IP = GUI.GetIPGUI()

# assign buffer_size as 1024 bits per Second
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"


# create a TCP client socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
	# connect to the intended server
	print(f"[+] Connecting to {SERVER_IP}")
	client_socket.connect(SERVER_IP)
	print("[+] Connected")
	path = GUI.InputFolderCreator()
	file_name = fm.collectfiles(path, platform_num)
	sender_checksum = CSV.getCheckSum(file_name)
	with open(file_name, 'rb') as file:
		data = file.read()
	filename = file_name + ".bin"
	ED.encrypt(key, data, filename)
	# get the file size
	filesize = os.path.getsize(filename)
	#send the filename and file size to the server
	client_socket.send(f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{sender_checksum}".encode())
	progress = 0
	List = []
	with open(filename, 'rb') as file:
		while True:
			# read the bytes from the file
			bytes_read = file.read(BUFFER_SIZE)
			# join this with the enc_data
			enc_data += bytes_read
			progress += len(bytes_read)
			if not bytes_read:
				# file transmitting is done
				break
			# we use sendall to assure transmission in busy networks
			client_socket.sendall(bytes_read)
			if round((progress/filesize)*100)%10 == 0:
				if round((progress/filesize)*100) not in List:
					print("Download completed =", round((progress/filesize)*100))
					List.append(round((progress/filesize)*100))
print("File transfer completed successfully")
showinfo("Information-AESFileTranfer", "File transfer has been completed successfully 🙌")
# the data in bytes read in a seprate text file:
with open("Encryption.txt", "wb") as enc:
	enc.write(enc_data)
#opt = input("Do you want read the data present in the encrypted file? ")
opt = GUI.OpenEncryptedFile()
if opt == "yes":
	AppO.open_application(platform_num, "Encryption.txt")
	os.remove(filename)
	os.remove(file_name)
else:
	print("If you want to see the encrypted data open the file named encryption.txt")
	os.remove(filename)
	os.remove(file_name)


# remove the files from the current directory
