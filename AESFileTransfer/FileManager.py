# import necessary modules
import os
import subprocess
import shutil
from pathlib import Path


# import necessary user defined modules
import CompressionDecompression as CD
import EncryptDecrypt as ED
import CheckSumValidator as CSV
import GraphicalUserInterface as GUI


def getDefaultDir():
	return os.getcwd()


def getHometDir():
	homedir = Path.home()
	return homedir


def MakeNewDirectory(platform_num):
	path = os.path.expanduser('~')
	if platform_num == 1:
		path = path + r'\Documents\AESFileTransfer'
		if os.path.exists(path):
			return path
		else:
			os.mkdir(path)
			return path
	else:
		path = path + r'/Documents/AESFileTransfer'
		if os.path.exists(path):
			return path
		else:
			os.mkdir(path)
			return path


def downloadDir(platform_num):
	path = os.path.expanduser('~')
	if platform_num == 1:
		path = path + r'\Downloads\AESFileTransfer'
		if os.path.exists(path):
			return path
		else:
			os.mkdir(path)
			return path
	else:
		path = path + r'/Downloads/AESFileTransfer'
		if os.path.exists(path):
			return path
		else:
			os.mkdir(path)
			return path


def changeDirectory(path):
	os.chdir(path)


def collectfiles(path, platform_num):
	file_names = os.listdir(path)
	path_ = os.path.expanduser('~')
	if platform_num != 1:
		target = path_ + r'/Desktop/AESFileTransfer'
	else:
		target = path_ + r'\Desktop\AESFileTranfer'
	filelist = []
	print("Printing the files present the directory...\n")
	for file_name in file_names:
		print(f"file_name: {file_name}")
		filelist.append(file_name)
	ZipFileName = os.path.basename(path) + '.zip'
	if platform_num != 1:
		ZipFileNamepath = target+r'/'+ZipFileName
	else:
		ZipFileNamepath = target+r'\\'+ZipFileName
	print(f"ZipFile path: {ZipFileNamepath}")
	CD.Compress(ZipFileNamepath, filelist, path)
	print(f"ZipFileName: {ZipFileName}")
	return ZipFileName


def sendfilelist(path):
	file_names = os.listdir(path)
	return file_names


def receivefile(path, filename, key):
	changeDirectory(path)
	data = ED.decrypt(key, filename)
	filename = filename[:len(filename)-4]
	with open(filename, 'wb') as file:
		file.write(data)
	CD.Decompress(filename)
	receiver_checksum = CSV.getCheckSum(filename)
	print("receivefile :", filename)
	return receiver_checksum
