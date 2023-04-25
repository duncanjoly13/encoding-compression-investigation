#TODO fix extra \n
#TODO implement AES-16, AES-32 - pycrypto?
#TODO implement RSA or other method - rsa module

import os, hashlib, time
from cryptography.fernet import Fernet

class DJFernet:
    def __init__(self, filename = '2000-word-text.txt'):
        self.filesize = os.path.getsize(filename)
        self.type = 'Fernet'
        self.filename = filename
        self.encryptionTime = 0
        self.decryptionTime = 0
        self.decryptedSize = 0
        self.encryptedSize = 0
        self.key = ''
        self.hashString = ''

    def encrypt(self):
        encryptionStartTime = time.time()
        dataFileDataFP = open(self.filename, 'rb')
        rawFileData = dataFileDataFP.read()
        dataFileDataFP.close()
        key = Fernet.generate_key()
        f = Fernet(key)
        encMessage = f.encrypt(rawFileData)
        fileHash = hashlib.sha1(encMessage)
        self.hashString = fileHashString = fileHash.hexdigest()
        encDataFP = open(str(self.filename + '.frnt'), 'wb')
        encDataFP.write(encMessage)
        encDataFP.flush()
        encDataFP.close()
        keyFP = open('{}-key'.format(fileHashString), 'wb')
        keyFP.write(key)
        keyFP.flush()
        keyFP.close()
        self.key = key
        self.encryptionTime = time.time() - encryptionStartTime
    
    def decrypt(self):
        decryptionStartTime = time.time()
        decryptFP = open(self.filename, 'rb')
        decryptData = decryptFP.read()
        decryptFP.close()
        with open(str(hashlib.sha1(decryptData).hexdigest()) + '-key', 'rb') as f_in:
            self.key = f_in.read()
            f_in.close()
        decryptKey = Fernet(self.key)
        with open(str(self.filename[:-5] + '.decrypted'), 'w') as f_out:
            f_out.write(decryptKey.decrypt(decryptData).decode('ascii'))
            f_out.close()
        self.decryptionTime = time.time() - decryptionStartTime

if __name__ == '__main__':
    '''initial = DJFernet('2000-word-text.txt')
    encrypted = initial.encrypt()
    toDecrypt = DJFernet('2000-word-text.txt.frnt')
    decrypted = toDecrypt.decrypt()'''