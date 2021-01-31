import os
import pwd
import sys
from hashlib import sha256
from base64 import b64encode, b64decode
from Crypto import Random
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
sys.path.append('./modules')
from LoggerClass import Logger

class Utils:

	passphrase = ""

	def __init__(self):
		self.passphrase = self.getPassphrase()	
	
	def getPathTalert(self, path_dir):
		path_origen = "/etc/Telk-Alert-Suite/Telk-Alert"
		path_final = os.path.join(path_origen, path_dir)
		return path_final

	def getPassphrase(self):
		file_key = open(self.getPathTalert('conf') + '/key','r')
		pass_key = file_key.read()
		file_key.close()
		return pass_key

	def validateRegularExpression(regular_expression, data):
		if(not regular_expression.match(data)):
			return False
		return True

	def changeUidGid(path):
		uid = pwd.getpwnam('telkalert').pw_uid
		gid = pwd.getpwnam('telkalert').pw_gid
		os.chown(path, uid, gid)

	def getSha256File(self, file):
		try:
			hashsha = sha256()
			with open(file, "rb") as file_hash:
				for block in iter(lambda: file_hash.read(4096), b""):
					hashsha.update(block)
			return hashsha.hexdigest()
		except Exception as exception:
			Logger.createLogTool("Error" + str(exception), 4)

	def encryptAES(self, text):
		text_bytes = bytes(text, 'utf-8')
		key = sha256(self.passphrase.encode()).digest()
		IV = Random.new().read(AES.block_size)
		aes = AES.new(key, AES.MODE_CBC, IV)
		return b64encode(IV + aes.encrypt(pad(text_bytes, AES.block_size)))

	def decryptAES(self, text_encrypt):
		key = sha256(self.passphrase.encode()).digest()
		text_encrypt = b64decode(text_encrypt)
		IV = text_encrypt[:AES.block_size]
		aes = AES.new(key, AES.MODE_CBC, IV)
		return unpad(aes.decrypt(text_encrypt[AES.block_size:]), AES.block_size)