from sys import exit
from pwd import getpwnam
from datetime import date
from os import path, chown
from hashlib import sha256
from binascii import Error
from base64 import b64decode
from Crypto.Cipher import AES
from yaml import safe_load, safe_dump
from Crypto.Util.Padding import unpad
from logging import getLogger, INFO, Formatter, FileHandler, StreamHandler

"""
Class that allows you to manage the utilities that the application will use for its operation.
"""
class Utils:
	"""
	Property that stores the passphrase that will be used for the encryption/decryption process.
	"""
	passphrase = None

	"""
	Constructor for the Utils class.

	Parameters:
	self -- An instantiated object of the Utils class.
	"""
	def __init__(self):
		self.passphrase = self.getPassphrase()

	"""
	Method that obtains and stores the content of a YAML file in a variable.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_file_yaml -- YAML file path.
	mode -- Mode in which the YAML file will be opened.

	Return:
	data_file_yaml -- Variable that stores the content of the YAML file.

	Exceptions:
	IOError -- It is an error raised when an input/output operation fails.
	"""
	def readYamlFile(self, path_file_yaml, mode):
		try:
			with open(path_file_yaml, mode) as file_yaml:
				data_file_yaml = safe_load(file_yaml)
		except IOError as exception:
			self.createTelkAlertLog("Error opening or reading the YAML file. For more information, see the logs.", 3)
			self.createTelkAlertLog(exception, 3)
			exit(1)
		else:
			return data_file_yaml

	"""
	Method that defines a directory based on the main Telk-Alert directory.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_dir -- Directory that is added to the main Telk-Alert directory.

	Return:
	path_final -- Defined final path.

	Exceptions:
	OSError -- This exception is raised when a system function returns a system-related error, including I/O failures such as “file not found” or “disk full” (not for illegal argument types or other incidental errors).
	TypeError -- Raised when an operation or function is applied to an object of inappropriate type. The associated value is a string giving details about the type mismatch.
	"""
	def getPathTelkAlert(self, path_dir):
		path_main = "/etc/Telk-Alert-Suite/Telk-Alert"
		try:
			path_final = path.join(path_main, path_dir)
		except (OSError, TypeError) as exception:
			self.createTelkAlertLog("An error has occurred. For more information, see the logs.", 3)
			self.createTelkAlertLog(exception, 3)
			exit(1)
		else:
			return path_final

	"""
	Method that obtains the passphrase used for the process of encrypting and decrypting a file.

	Parameters:
	self -- An instantiated object of the Utils class.

	Return:
	pass_key -- Passphrase in a character string.

	Exceptions:
	FileNotFoundError -- This is an exception in python and it comes when a file does not exist and we want to use it. 
	"""
	def getPassphrase(self):
		try:
			file_key = open(self.getPathTelkAlert('conf') + '/key','r')
			pass_key = file_key.read()
			file_key.close()
		except FileNotFoundError as exception:
			self.createTelkAlertLog("Error opening or reading the Key file. For more information, see the logs.", 3)
			self.createTelkAlertLog(exception, 3)
			exit(1)
		else:
			return pass_key

	"""
	Method that converts from a number of minutes, hours or days to seconds.

	Parameters:
	self -- An instantiated object of the Utils class.
	unit_time -- Unit of time in which the quantity to be converted is expressed.
	total_time -- Total time to convert.

	Return:
	total_seconds -- Total seconds resulting from the conversion.
	"""
	def convertTimeToSeconds(self, unit_time, total_time):
		if unit_time == "minutes":
			total_seconds = total_time * 60
		elif unit_time == "hours":
			total_seconds = total_time * 3600
		elif unit_time == "days":
			total_seconds = total_time * 86400
		return total_seconds

	"""
	"""
	def convertTimeToStringSearch(self, unit_time, total_time):
		string_search = "now-"
		if unit_time == "minutes":
			string_search += str(total_time) + 'm'
		elif unit_time == "hours":
			string_search += str(total_time) + 'h'
		elif unit_time == "days":
			string_search += str(total_time) + 'd'
		return string_search

	"""
	Method that changes an owner path, by telk_alert user and group.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_to_change -- Directory that will change owner.

	Exceptions:
	OSError -- This exception is raised when a system function returns a system-related error, including I/O failures such as “file not found” or “disk full” (not for illegal argument types or other incidental errors).
	"""
	def ownerChange(self, path_to_change):
		try:
			uid = getpwnam('telk_alert').pw_uid
			gid = getpwnam('telk_alert').pw_gid
			chown(path_to_change, uid, gid)
		except OSError as exception:
			self.createTelkAlertLog("Failed to change owner path. For more information, see the logs.", 3)
			self.createTelkAlertLog(exception, 3)
			exit(1)

	"""
	Method that decrypts a text string.

	Parameters:
	self -- An instantiated object of the Utils class.
	text_encrypt -- Text to decipher.

	Return:
	Character string with decrypted text.

	Exceptions:
	Error -- Is raised if were incorrectly padded or if there are non-alphabet characters present in the string. 
	"""
	def decryptAES(self, text_encrypt):
		try:
			key = sha256(self.passphrase.encode()).digest()
			text_encrypt = b64decode(text_encrypt)
			IV = text_encrypt[:AES.block_size]
			aes = AES.new(key, AES.MODE_CBC, IV)
		except Error as exception:
			self.createTelkAlertLog("Failed to decrypt the data. For more information, see the logs.", 3)
			self.createTelkAlertLog(exception, 3)
			exit(1)
		else:
			return unpad(aes.decrypt(text_encrypt[AES.block_size:]), AES.block_size)

	"""
	Method that writes the logs generated by the application in a file.

	Parameters:
	self -- An instantiated object of the Utils class.
	message -- Message to be shown in the log.
	type_log -- Type of log to write.
	"""
	def createTelkAlertLog(self, message, type_log):
		name_log = '/var/log/Telk-Alert/telk-alert-log-' + str(date.today()) + '.log'
		logger = getLogger('Telk_Alert_Log')
		logger.setLevel(INFO)
		fh = FileHandler(name_log)
		ch = StreamHandler()
		if (logger.hasHandlers()):
   	 		logger.handlers.clear()
		formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		formatter_console = Formatter('%(levelname)s - %(message)s')
		fh.setFormatter(formatter)
		ch.setFormatter(formatter_console)
		logger.addHandler(fh)
		logger.addHandler(ch)
		if type_log == 1:
			logger.info(message)
		if type_log == 2:
			logger.warning(message)
		if type_log == 3:
			logger.error(message)
		self.ownerChange(name_log)