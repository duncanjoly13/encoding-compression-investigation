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
        ### FOR TESTING
        print(encMessage)
        print(type(encMessage))
        ###
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

    '''# test NoEnc
    with open('10_mb.pdf', 'rb') as noEncFile:
        testNoEnc = NoEnc(noEncFile.read())
        noEncFile.close()
    with open('noenc-encrypted.pdf', 'wb') as noEncEncrypted:
        noEncEncrypted.write(testNoEnc.encrypt())
        noEncEncrypted.close()
    with open('noenc-encrypted.pdf', 'rb') as noEncToDecryptFile:
        toDecryptNoEnc = NoEnc(noEncToDecryptFile.read())
        noEncToDecryptFile.close()
    with open('noenc-completed.pdf', 'wb') as noEncFinalFile:
        decryptedNoEncData = toDecryptNoEnc.decrypt()
        noEncFinalFile.write(decryptedNoEncData)
        noEncFinalFile.close()

    # test DJFernet
    with open('10_mb.pdf', 'rb') as fernetfile:
        testFernet = DJFernet(fernetfile.read())
        fernetfile.close()
    with open('Fernet-encrypted.pdf', 'wb') as fernetEncrypted:
        fernetEncrypted.write(testFernet.encrypt())
        fernetEncrypted.close()
    with open('Fernet-encrypted.pdf', 'rb') as fernetToDecryptFile:
        toDecryptFernet = DJFernet(fernetToDecryptFile.read())
        fernetToDecryptFile.close()
    with open('Fernet-completed.pdf', 'wb') as fernetFinalFile:
        decryptedFernetData = toDecryptFernet.decrypt()
        fernetFinalFile.write(decryptedFernetData)
        fernetFinalFile.close()'''

    # test NaCl
    with open('10_mb.pdf', 'rb') as naclFile:
        testNaCl = NaCl(naclFile.read())
        naclFile.close()
    with open('NaCl-encrypted.pdf', 'wb') as naclEncrypted:
        naclEncrypted.write(testNaCl.encrypt())
        naclEncrypted.close()
    with open('NaCl-encrypted.pdf', 'rb') as naclToDecryptFile:
        toDecryptNaCl = NaCl(naclToDecryptFile.read())
        naclToDecryptFile.close()
    with open('NaCl-completed.pdf', 'wb') as naclFinalFile:
        decryptedNaclData = toDecryptNaCl.decrypt()
        naclFinalFile.write(decryptedNaclData)
        naclFinalFile.close()
