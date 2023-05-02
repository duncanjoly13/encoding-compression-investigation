#TODO FIX KEYS
#TODO fix UnicodeDecodeError
#TODO implement output folder
#TODO fix extra \n
#TODO implement NaCl, AES or RSA

import os, hashlib, time, nacl.secret, nacl.utils
from cryptography.fernet import Fernet

class DJFernet:
    def __init__(self, data):
        self.key = ''
        self.hashString = ''
        self.type = 'Fernet'
        self.suffix = '.frnt'
        self.data = data
        
    def encrypt(self):
        key = Fernet.generate_key()
        f = Fernet(key)
        encMessage = f.encrypt(self.data)
        fileHash = hashlib.sha1(encMessage)
        self.hashString = fileHashString = fileHash.hexdigest()
        keyFP = open('./keys/' + '{}-key'.format(fileHashString), 'wb')
        keyFP.write(key)
        keyFP.flush()
        keyFP.close()
        self.key = key
        return encMessage
    
    def decrypt(self):
        with open(KEYFILE, 'rb') as f_in:
            self.key = f_in.read()
            f_in.close()
        decryptKey = Fernet(self.key)
        return decryptKey.decrypt(self.data)

if __name__ == '__main__':
    '''initial = DJFernet('2000-word-text.txt')
    encrypted = initial.encrypt()
    toDecrypt = DJFernet('2000-word-text.txt.frnt')
    decrypted = toDecrypt.decrypt()'''