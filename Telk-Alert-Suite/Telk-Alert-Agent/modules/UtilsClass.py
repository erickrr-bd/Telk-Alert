import os
import sys
import yaml
import binascii
from hashlib import sha256
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from modules.LoggerClass import Logger

"""
Class that allows to manage the utilities of the application.
"""
class Utils:

	"""
	Property that saves the passphrase that will be used for the decryption process.
	"""
	passphrase = ""

	"""
	Logger type object.
	"""
	logger = Logger()

	"""
	Constructor for the Utils class.

	Parameters:
	self -- An instantiated object of the Utils class.
	"""
	def __init__(self):
		self.passphrase = self.getPassphrase()

	"""
	Method that obtains the content of a file with the extension yaml.

	Parameters:
	self -- An instantiated object of the Utils class.
	file_yaml -- Yaml file path.

	Return:
	data_yaml -- Contents of the .yaml file stored in a list.

	Exceptions:
	IOError -- It is an error raised when an input/output operation fails.
	"""
	def readFileYaml(self, file_yaml):
		try:
			with open(file_yaml, 'r') as file:
				data_yaml = yaml.safe_load(file)
			return data_yaml
		except IOError as exception:
			print("\nYaml file not found. For more information see the application logs.")
			self.logger.createLogAgent("File Error: " + str(exception), 4)
			sys.exit(1)

	"""
	Method that creates a new route from the root path of Telk-Alert.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_dir -- Folder or directory that will be added to the source path of Telk-Alert.

	Return:
	path_final -- Final directory.
	"""
	def getPathTalert(self, path_dir):
		path_root = "/etc/Telk-Alert-Suite/Telk-Alert"
		path_final = os.path.join(path_root, path_dir)
		return path_final

	"""
	Method that creates a new route from the root path of Telk-Alert-Agent.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_dir -- Folder or directory that will be added to the source path of Telk-Alert-Agent.

	Return:
	path_agent -- Final directory.
	"""
	def getPathTagent(self, path_dir):
		path_root = "/etc/Telk-Alert-Suite/Telk-Alert-Agent"
		path_agent = os.path.join(path_root, path_dir)
		return path_agent

	"""
	Method that obtains the passphrase used for the process of encrypting and decrypting a file.

	Parameters:
	self -- An instantiated object of the Utils class.

	Return:
	pass_key -- Passphrase in a character string.

	Exceptions:
	FileNotFoundError -- his is an exception in python and it comes when a file does not exist and we want to use it. 
	"""
	def getPassphrase(self):
		try:
			file_key = open(self.getPathTalert('conf') + '/key','r')
			pass_key = file_key.read()
			file_key.close()
			return pass_key
		except FileNotFoundError as exceptions:
			print("\nKey File not found. For more information see the application logs.")
			self.logger.createLogAgent("File Error: " + str(exceptions), 4)
			sys.exit(1)

	"""
	Method that encrypts a text string.

	Parameters:
	self -- An instantiated object of the Utils class.
	text_encrypt -- Text to decipher.

	Return:
	Character string with decrypted text.

	Exceptions:
	binascii.Error -- Is raised if were incorrectly padded or if there are non-alphabet characters present in the string. 
	"""
	def decryptAES(self, text_encrypt):
		try:
			key = sha256(self.passphrase.encode()).digest()
			text_encrypt = b64decode(text_encrypt)
			IV = text_encrypt[:AES.block_size]
			aes = AES.new(key, AES.MODE_CBC, IV)
			return unpad(aes.decrypt(text_encrypt[AES.block_size:]), AES.block_size)
		except binascii.Error as exception:
			print("\nDecryption failed. For more information see the application logs.")
			self.logger.createLogAgent("Decrypt Error: " + str(exception), 4)
			sys.exit(1)