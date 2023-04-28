#TODO fix UnicodeDecodeError
#TODO implement output folder
#TODO finish NaCl class
#TODO fix extra \n
#TODO implement AES or RSA

import os, hashlib, time, nacl.secret, nacl.utils
from cryptography.fernet import Fernet

class DJFernet:
    def __init__(self, filename):
        self.filesize = os.path.getsize(filename)
        self.type = 'Fernet'
        self.filename = filename
        self.encryptionTime = 0
        self.decryptionTime = 0
        self.decryptedSize = 0
        self.encryptedSize = 0
        self.key = ''
        self.hashString = ''
        self.suffix = '.frnt'

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
        encDataFP = open(str(self.filename + self.suffix), 'wb')
        encDataFP.write(encMessage)
        encDataFP.flush()
        encDataFP.close()
        keyFP = open('{}-key'.format(fileHashString), 'wb')
        keyFP.write(key)
        keyFP.flush()
        keyFP.close()
        self.key = key
        self.encryptionTime = time.time() - encryptionStartTime
        self.encryptedSize = str(os.path.getsize(str(self.filename + self.suffix)))
    
    def decrypt(self):
        decryptionStartTime = time.time()
        decryptFP = open(self.filename, 'rb')
        toDecrypt = decryptFP.read()
        decryptFP.close()
        with open(str(hashlib.sha1(toDecrypt).hexdigest()) + '-key', 'rb') as f_in:
            self.key = f_in.read()
            f_in.close()
        decryptKey = Fernet(self.key)
        with open(str(self.filename + '.decrypted'), 'wb') as f_out: #ERROR filename changes
            decryptedData = (decryptKey.decrypt(toDecrypt))
            f_out.write(decryptedData)
            f_out.close()
        self.decryptionTime = time.time() - decryptionStartTime
        self.decryptedSize = str(os.path.getsize(self.filename))

class NaCl:
    def __init__(self, filename, key = ''):
        self.filesize = os.path.getsize(filename)
        self.type = 'NaCl'
        self.filename = filename
        self.encryptionTime = 0
        self.decryptionTime = 0
        self.decryptedSize = 0
        self.encryptedSize = 0
        # self.hashString = ''
        self.suffix = '.nacl'
        if key == '':
            self.key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        else:
            self.key = key
        self.safe = nacl.secret.SecretBox(self.key)

    def encrypt(self):
        encryptionStartTime = time.time()
        with open(self.filename) as f_in:
            with open(str(self.filename + self.suffix), 'wb') as f_out:
                f_out.write(self.safe.encrypt(f_in.read().encode()))
                f_out.close()
                
                with open(self.filename + self.suffix) as encryptedFile:
                    with open(str(hashlib.sha1(str(encryptedFile.read()).encode()).hexdigest()) + '-key', 'wb') as keyfile:
                        keyfile.write(self.key)

                f_out.close()

            f_in.close()
        self.encryptionTime = time.time() - encryptionStartTime
        self.encryptedSize = str(os.path.getsize(str(self.filename + self.suffix)))

    # def decrypt(self):
        
        # self.decryptedSize = str(os.path.getsize(str(self.filename + self.suffix)))


if __name__ == '__main__':
    '''initial = DJFernet('2000-word-text.txt')
    encrypted = initial.encrypt()
    toDecrypt = DJFernet('2000-word-text.txt.frnt')
    decrypted = toDecrypt.decrypt()'''

    '''initial = NaCl('2000-word-text.txt')
    encrypted = initial.encrypt()
    with open('2000-word-text.txt.nacl') as file:
        toDecrypt = NaCl('2000-word-text.txt.nacl', hashlib.sha1(file.read()).hexdigest())
        # decrypted = toDecrypt.decrypt()'''