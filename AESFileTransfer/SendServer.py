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
import CompressionDecompression as CD


# key for encryption/ decryption
key = b'\xa2\xe8\xc3?\x0b}\xb6\xd4\xc1ZgN\x9a?zw'
# a variable which will store the data in the encrypted file
enc_data = b""
# finds the Operating System used for the server
platform_num = AppO.find_platform()
default_path = fm.getDefaultDir()
destination_path = fm.MakeNewDirectory(platform_num)
file_list = []
path = os.environ['HOME']
if platform_num != 1:
    path_ = path + r'/Documents/AESFileTransfer'
    files = fm.sendfilelist(path_)
else:
    path_ = path + r'\Documents\AESFileTransfer'
    files = fm.sendfilelist(path_)
for file in files:
    file_list.append(file)
file_list_encoded = pickle.dumps(file_list)
print(file_list_encoded)


# assigning HOST and PORT Number
HOST = "127.0.0.1"
PORT = 65432


# assign buffer_size as 1024 bits per Second
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

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
#files = fm.sendfilelist(r'/Users/macbook/Desktop/AESFileTransfer')
#print("The list of files available to download...")
#file_list_encoded = pickle.dumps(file_list)
client_socket.send(file_list_encoded)
file_list = client_socket.recv(1024)
file_list = pickle.loads(file_list)
path = os.environ['HOME']
if platform_num != 1:
    path_ = path + r'/Desktop/AESFileTransfer/SendFile.zip'
    CD.Compress(path_, file_list, path + r'/Documents/AESFileTransfer')
else:
    path_ = path + r'\Desktop\AESFileTransfer\SendFile.zip'
    CD.Compress(path_, file_list, path + r'\Documents\AESFileTransfer')
file_name = "SendFile.zip"
sender_checksum = CSV.getCheckSum(file_name)
with open(file_name, 'rb') as file:
    data = file.read()
filename = file_name + ".bin"
ED.encrypt(key, data, filename)
filesize = os.path.getsize(filename)
client_socket.send(f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{sender_checksum}".encode())
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, 'rb') as file:
    while True:
        # read the bytes from the file
        bytes_read = file.read(BUFFER_SIZE)
        # join this with the enc_data
        enc_data += bytes_read
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transmission in busy networks
        client_socket.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
print("File transfer completed successfully")
# the data in bytes read in a seprate text file:
with open("Encryption.txt", "wb") as enc:
    enc.write(enc_data)
opt = input("Do you want read the data present in the encrypted file??? ")
if opt == "yes":
    AppO.open_application(platform_num, "Encryption.txt")
else:
    print("If you want to see the encrypted data open the file named encryption.txt")


# remove the files from the current directory
os.remove(filename)
os.remove(file_name)
s.close()
