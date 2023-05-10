#TODO FIX KEYS
#TODO fix UnicodeDecodeError
#TODO implement output folder
#TODO implement NaCl, AES or RSA

import os, hashlib, nacl.secret, nacl.utils
from cryptography.fernet import Fernet

class DJFernet:
    def __init__(self, data):
        self.key = ''
        self.type = 'Fernet'
        self.suffix = '.frnt'
        self.data = data
        
    def encrypt(self):
        self.key = Fernet.generate_key()
        f = Fernet(self.key)
        if type(self.data) != bytes:
            self.data = str.encode(self.data)
        encMessage = f.encrypt(self.data)
        with open('./keys/' + encMessage.decode("utf-8")[:10] + '.key', 'wb') as keyFP:
            keyFP.write(self.key)
            keyFP.flush()
            keyFP.close()
        return encMessage
    
    def decrypt(self):
        keyprefix = self.data[:10]
        if type(self.data) == bytes:
            keyprefix = self.data[:10].decode()
        with open('./keys/' + keyprefix + '.key', 'rb') as f_in:
            self.key = f_in.read()
            f_in.close()
        decryptKey = Fernet(self.key)
        return decryptKey.decrypt(self.data)

if __name__ == '__main__':
    initial = DJFernet('2000-word-text.txt')
    encrypted = initial.encrypt()
    toDecrypt = DJFernet('2000-word-text.txt.frnt')
    decrypted = toDecrypt.decrypt()