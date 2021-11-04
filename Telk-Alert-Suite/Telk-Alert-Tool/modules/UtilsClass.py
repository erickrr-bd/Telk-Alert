from pwd import getpwnam
from datetime import date
from Crypto import Random
from hashlib import sha256
from Crypto.Cipher import AES
from os import path, chown, mkdir
from yaml import safe_load, safe_dump
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad
from logging import getLogger, INFO, Formatter, FileHandler

"""
Class that allows managing all the utilities that are used for the operation of the application.
"""
class Utils:
	"""
	Property that stores the passphrase for the process of encrypting/decrypting information.
	"""
	passphrase = None

	"""
	Property that stores an object of the FormDialog class.
	"""
	form_dialog = None

	"""
	Constructor for the Utils class.

	Parameters:
	self -- An instantiated object of the Utils class.
	form_dialog -- FormDialog class object.
	"""
	def __init__(self, form_dialog):
		self.form_dialog = form_dialog
		self.passphrase = self.getPassphrase()

	"""
	Method that creates a YAML file.

	Parameters:
	self -- An instantiated object of the Utils class.
	data -- Information that will be stored in the YAML file.
	path_file_yaml -- YAML file path.
	mode -- Mode in which the YAML file will be opened.

	Exceptions:
	IOError -- It is an error raised when an input/output operation fails.
	"""
	def createYamlFile(self, data, path_file_yaml, mode):
		try:
			with open(path_file_yaml, mode) as file_yaml:
				safe_dump(data, file_yaml, default_flow_style = False)
			self.ownerChange(path_file_yaml)
		except IOError as exception:
			self.createTelkAlertToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nError creating YAML file. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

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
	FileNotFoundError -- This is an exception in python and it comes when a file does not exist and we want to use it.
	"""
	def readYamlFile(self, path_file_yaml, mode):
		try:
			with open(path_file_yaml, mode) as file_yaml:
				data_file_yaml = safe_load(file_yaml)
		except (IOError, FileNotFoundError) as exception:
			self.createTelkAlertToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nError opening or reading the YAML file. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return data_file_yaml

	"""
	Method that creates a new directory.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_new_folder -- Path of the new directory that will be created.

	Exceptions:
	OSError -- This exception is raised when a system function returns a system-related error, including I/O failures such as “file not found” or “disk full” (not for illegal argument types or other incidental errors).
	"""
	def createNewFolder(self, path_new_folder):
		try:
			if not path.isdir(path_new_folder):
				mkdir(path_new_folder)
				self.ownerChange(path_new_folder)
		except OSError as exception:
			self.createTelkAlertToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to create directory. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that defines a directory based on the main Telk-Alert directory.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_dir -- Directory that is added to the main Telk-Alert directory.

	Return:
	path_final -- Defined final path.

	Exceptions:
	OSError -- This exception is raised when a system function returns a system-related error, including I/O failures such as “file not found” or “disk full” (not for illegal argument types or other incidental errors).
	TypeError -- Raised when an operation or function is applied to an object of inappropriate type. The associate value is a string giving details about the type mismatch.
	"""
	def getPathTelkAlert(self, path_dir):
		path_main = "/etc/Telk-Alert-Suite/Telk-Alert"
		try:
			path_final = path.join(path_main, path_dir)
		except (OSError, TypeError) as exception:
			self.createTelkAlertToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nAn error has occurred. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return path_final

	"""
	Method that defines a directory based on the main Telk-Alert-Agent directory.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_dir -- Directory that is added to the main Telk-Alert-Agent directory.

	Return:
	path_final -- Defined final path.

	Exceptions:
	OSError -- This exception is raised when a system function returns a system-related error, including I/O failures such as “file not found” or “disk full” (not for illegal argument types or other incidental errors).
	TypeError -- Raised when an operation or function is applied to an object of inappropriate type. The associate value is a string giving details about the type mismatch.
	"""
	def getPathTelkAlertAgent(self, path_dir):
		path_main = "/etc/Telk-Alert-Suite/Telk-Alert-Agent"
		try:
			path_final = path.join(path_main, path_dir)
		except (OSError, TypeError) as exception:
			self.createTelkAlertToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nAn error has occurred. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
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
			self.createTelkAlertToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nError opening or reading the Key file. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return pass_key

	"""
	Method that validates data from a regular expression.

	self -- An instantiated object of the Utils class.
	regular_expression -- Regular expression with which the data will be validated.
	data -- Data to be validated.
	"""
	def validateRegularExpression(self, regular_expression, data):
		if(not regular_expression.match(data)):
			return False
		return True

	"""
	Method that changes an owner path, by telk_alert user and 
	group.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_to_change -- Directory that will change owner.

	Exceptions:
	OSError -- This exception is raised when a system function
	           returns a system-related error, including I/O
	           failures such as “file not found” or “disk full”
	           (not for illegal argument types or other incidental
	           errors).
	"""
	def ownerChange(self, path_to_change):
		try:
			uid = getpwnam('telk_alert').pw_uid
			gid = getpwnam('telk_alert').pw_gid
			chown(path_to_change, uid, gid)
		except OSError as exception:
			self.createTelkAlertToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to change owner path. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that obtains the hash of a file.

	Parameters:
	self -- An instantiated object of the Utils class.
	file -- Path of the file from which the hash function will be obtained.

	Return:
	Hash of the file.

	Exceptions:
	IOError -- It is an error raised when an input/output operation fails.
	"""
	def getHashToFile(self, path_file):
		try:
			hash_sha = sha256()
			with open(path_file, 'rb') as file_to_hash:
				for block in iter(lambda: file_to_hash.read(4096), b""):
					hash_sha.update(block)
		except IOError as exception:
			self.createTelkAlertToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nError getting the file's hash function. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return hash_sha.hexdigest()

	"""
	Method that encrypts a text string.

	Parameters:
	self -- An instantiated object of the Utils class.
	text -- Text to encrypt.

	Return:
	Encrypted text.

	Exceptions:
	Exception -- It is thrown when any exception is found.
	"""
	def encryptAES(self, text):
		try:
			text_bytes = bytes(text, 'utf-8')
			key = sha256(self.passphrase.encode()).digest()
			IV = Random.new().read(AES.block_size)
			aes = AES.new(key, AES.MODE_CBC, IV)
		except Exception as exception:
			self.createTelkAlertToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to encrypt the data. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return b64encode(IV + aes.encrypt(pad(text_bytes, AES.block_size)))

	"""
	Method that decrypts a text string.

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
		except binascii.Error as exception:
			self.createTelkAlertToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to decrypt the data. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return unpad(aes.decrypt(text_encrypt[AES.block_size:]), AES.block_size)

	"""
	Method that writes the logs generated by the application in a file.

	Parameters:
	self -- An instantiated object of the Logger class.
	message -- Message to be shown in the log.
	type_log -- Type of log to write.
	"""
	def createTelkAlertToolLog(self, message, type_log):
		name_log = "/var/log/Telk-Alert/telk-alert-tool-log-" + str(date.today()) + ".log"
		logger = getLogger("Telk_Alert_Tool_Log")
		logger.setLevel(INFO)
		fh = FileHandler(name_log)
		if (logger.hasHandlers()):
   	 		logger.handlers.clear()
		formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		fh.setFormatter(formatter)
		logger.addHandler(fh)
		if type_log == 1:
			logger.info(message)
		elif type_log == 2:
			logger.warning(message)
		elif type_log == 3:
			logger.error(message)
		self.ownerChange(name_log)