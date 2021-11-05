from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def generatekey(length):
	key = get_random_bytes(length)
	return key
	
	
def encrypt(key, data, file_name):
	cipher = AES.new(key, AES.MODE_CBC)
	ciphered_data = cipher.encrypt(pad(data, AES.block_size))
	with open(file_name, 'wb') as file:
		file.write(cipher.iv)
		file.write(ciphered_data)
		
		
def decrypt(key, file_name):
	with open(file_name, 'rb') as file:
		iv = file.read(16)
		ciphered_data = file.read()
	cipher = AES.new(key, AES.MODE_CBC, iv=iv)
	original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size)
	return original_data