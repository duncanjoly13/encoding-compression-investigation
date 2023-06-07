import os, hashlib, nacl.secret, nacl.utils
from cryptography.fernet import Fernet

class NoEnc:
    def __init__(self, data):
        self.key = ''
        self.type = 'NoEnc'
        self.suffix = '.noenc'
        self.data = data

    def encrypt(self):
        if type(self.data) != bytes:
            return str.encode(self.data)
        else:
            return self.data
    
    def decrypt(self):
        if type(self.data) != bytes:
            return str.encode(self.data)
        else:
            return self.data

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
    
class NaCl:
    def __init__(self, data):
        self.key = ''
        self.type = 'NaCl'
        self.suffix = '.nacl'
        self.data = data

    def encrypt(self):
        self.key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        self.box = nacl.secret.SecretBox(self.key)
        if type(self.data) != bytes:
            self.data = str.encode(self.data)
        encMessage = self.box.encrypt(self.data)
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
        self.box = nacl.secret.SecretBox(self.key)
        decMessage = self.box.decrypt(self.data)
        return decMessage

if __name__ == '__main__':
    if os.path.exists(r'./keys/'):
        print('./keys/ exists!')
    else:
        os.makedirs(r'./keys/')

    # test NoEnc
    with open('10_mb.pdf', 'rb') as file:
        testNoEnc = NoEnc(file.read())
        file.close()
        with open('noenc-encrypted.pdf', 'wb') as encrypted:
            encrypted.write(testNoEnc.encrypt())
            encrypted.close()
    with open('noenc-encrypted.pdf', 'rb') as toDecryptFile:
        toDecryptNoEnc = NoEnc(toDecryptFile.read())
        toDecryptFile.close()
        with open('noenc-completed.pdf', 'wb') as finalFile:
            decryptedData = toDecryptNoEnc.decrypt()
            finalFile.write(decryptedData)
            finalFile.close()

    # test DJFernet
    with open('10_mb.pdf', 'rb') as file:
        testFernet = DJFernet(file.read())
        file.close()
        with open('Fernet-encrypted.pdf', 'wb') as encrypted:
            encrypted.write(testFernet.encrypt())
            encrypted.close()
    with open('Fernet-encrypted.pdf', 'rb') as toDecryptFile:
        toDecryptFernet = DJFernet(toDecryptFile.read())
        toDecryptFile.close()
        with open('Fernet-completed.pdf', 'wb') as finalFile:
            decryptedData = toDecryptFernet.decrypt()
            finalFile.write(decryptedData)
            finalFile.close()