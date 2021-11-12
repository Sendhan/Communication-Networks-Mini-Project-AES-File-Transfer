from hashlib import blake2b
import os


def getCheckSum(filename):
	h = blake2b()
	print(os.getcwd())
	with open(filename, "rb") as file:
		for chunk in iter(lambda: file.read(5), b""):
			h.update(chunk)
			return h.hexdigest()


def checkIntegrity(sender_checksum, receiver_checksum):
	if sender_checksum != receiver_checksum:
		return False
	else:
		return True
