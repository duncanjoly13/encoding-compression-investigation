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
    # Test NaCl
    with open('2000-word-text.txt') as file:
        testNaCl = NaCl(file.read())
        with open('encrypted.out', 'wb') as encrypted:
            encrypted.write(testNaCl.encrypt())
            encrypted.close()
        file.close()
    with open('encrypted.out', 'rb') as toDecrypt:
        toDecryptNaCl = NaCl(toDecrypt.read())
        with open('finished.out', 'w') as finalFile:
            finalFile.write(toDecryptNaCl.decrypt().decode())
            finalFile.close()
        toDecrypt.close()