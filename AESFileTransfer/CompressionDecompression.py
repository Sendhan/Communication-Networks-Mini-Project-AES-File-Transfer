# import necessary modules
from zipfile import ZipFile
import os


def Compress(ZipFileName, filelist, path):
	default_dir = os.getcwd()
	os.chdir(path)
	with ZipFile(ZipFileName, 'w') as zf:
		for file in filelist:
			zf.write(file)
	os.chdir(default_dir)

def Decompress(ZipFileName):
	with ZipFile(ZipFileName, 'r') as zf:
		zf.extractall()
