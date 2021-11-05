# import necessary modules
import os
import socket
import tqdm
import time
import pickle


# importing user defined modules
import ApplicationOpener as AppO
import FileManager as fm
import EncryptDecrypt as ED
import CheckSumValidator as CSV


key = b'\xa2\xe8\xc3?\x0b}\xb6\xd4\xc1ZgN\x9a?zw'
platform_num = AppO.find_platform()
default_path = fm.getDefaultDir()
destination_path = fm.downloadDir(platform_num)
file_list = []


# assigning HOST and PORT Number
HOST = "127.0.0.1"
PORT = 65432


# assign buffer_size as 1024 bits per Second
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[+] Connecting to {HOST}:{PORT}")
client_socket.connect((HOST, PORT))
print("[+] Connected")
list_file = client_socket.recv(1024)
list_file = pickle.loads(list_file)
for file in list_file:
    print(file)
while True:
    opt = input("Enter the name of the file to be downloaded(Enter stop to end): ")
    if opt == "stop":
        break
    else:
        file_list.append(opt)
file_list = pickle.dumps(file_list)
client_socket.send(file_list)
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
Integrity = CSV.checkIntegrity(sender_checksum, receiver_checksum)
if Integrity != True:
    print("File Transmitted was incorrect o(╥﹏╥)")
    client_socket.sendall("File Transmitted was incorrect o(╥﹏╥)".encode())
else:
    print("File Trasmission was is successful ᕕ( ᐛ )ᕗ")
    client_socket.sendall("File Trasmission was is successful ᕕ( ᐛ )ᕗ".encode())
AppO.open_application(platform_num, filename)
