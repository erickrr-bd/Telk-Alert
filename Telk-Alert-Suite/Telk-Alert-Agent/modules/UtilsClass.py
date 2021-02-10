import os
import sys
import yaml
from hashlib import sha256
from base64 import b64decode
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
sys.path.append('./modules')
from LoggerClass import Logger

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
	Method that allows obtaining the content of a file with extension .yaml

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
			self.logger.createLogAgent("Error" + str(exception), 4)

	"""
	Method that allows creating the path for a Telk-Alert-Agent directory.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_dir -- Folder or directory that will be added to the source path of Telk-Alert-Agent.

	Return:
	path_agent -- Final directory.
	"""
	def getPathTagent(self, path_dir):

		path_origen = "/etc/Telk-Alert-Suite/Telk-Alert-Agent"
		#path_origen = os.getcwd()
		path_agent = os.path.join(path_origen, path_dir)
		return path_agent

	"""
	Method that allows creating the path for a Telk-Alert directory.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_dir -- Folder or directory that will be added to the source path of Telk-Alert.

	Return:
	path_final -- Final directory.
	"""
	def getPathTalert(self, path_dir):
		path_origen = "/etc/Telk-Alert-Suite/Telk-Alert"
		path_final = os.path.join(path_origen, path_dir)
		return path_final

	"""
	Method that allows obtaining the passphrase of a file.

	Parameters:
	self -- An instantiated object of the Utils class.

	Return:
	pass_key -- Passphrase in a character string.
	"""
	def getPassphrase(self):
		file_key = open(self.getPathTalert('conf') + '/key','r')
		pass_key = file_key.read()
		file_key.close()
		return pass_key

	"""
	Method that allows deciphering a text.

	Parameters:
	self -- An instantiated object of the Utils class.
	text_encrypt -- Text to decipher.

	Return:
	Character string with decrypted text.
	"""
	def decryptAES(self, text_encrypt):
		key = sha256(self.passphrase.encode()).digest()
		text_encrypt = b64decode(text_encrypt)
		IV = text_encrypt[:AES.block_size]
		aes = AES.new(key, AES.MODE_CBC, IV)
		return unpad(aes.decrypt(text_encrypt[AES.block_size:]), AES.block_size)