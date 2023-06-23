import os, nacl.secret, nacl.utils
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

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

class TestFernet:
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
        with open('./keys/fernet.key', 'wb') as keyFP:
            keyFP.write(self.key)
            keyFP.flush()
            keyFP.close()
        return encMessage
    
    def decrypt(self):
        with open('./keys/fernet.key', 'rb') as f_in:
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
        with open('./keys/nacl.key', 'wb') as keyFP:
            keyFP.write(self.key)
            keyFP.flush()
            keyFP.close()
        return encMessage.__bytes__()

    def decrypt(self):
        with open('./keys/nacl.key', 'rb') as f_in:
            self.key = f_in.read()
            f_in.close()
        self.box = nacl.secret.SecretBox(self.key)
        decMessage = self.box.decrypt(self.data)
        return decMessage
    
class TestAES:
    def __init__(self, data):
        self.key = ''
        self.type = 'AES'
        self.suffix = '.aes'
        self.data = data
    
    def encrypt(self):
        self.key = get_random_bytes(16)
        if type(self.data) != bytes:
            self.data = str.encode(self.data, 'utf-8')
        cipher = AES.new(self.key, AES.MODE_CFB)
        encMessage = cipher.encrypt(self.data) + cipher.iv
        with open('./keys/aes.key', 'wb') as keyFP:
            keyFP.write(self.key)
            keyFP.flush()
            keyFP.close()
        return encMessage

    def decrypt(self):
        with open('./keys/aes.key', 'rb') as f_in:
            self.key = f_in.read()
            f_in.close()
        cipher = AES.new(self.key, AES.MODE_CFB, iv=self.data[-16:])
        return cipher.decrypt(self.data[:-16])

if __name__ == '__main__':
    if os.path.exists(r'./keys/'):
        print('./keys/ exists!')
    else:
        os.makedirs(r'./keys/')

    with open('10_mb.pdf', 'rb') as file:
        testdata = file.read()
        file.close()

    # test NoEnc
    testNoEnc = NoEnc(testdata)
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

    # test Fernet
    testFernet = TestFernet(testdata)
    with open('Fernet-encrypted.pdf', 'wb') as fernetEncrypted:
        fernetEncrypted.write(testFernet.encrypt())
        fernetEncrypted.close()
    with open('Fernet-encrypted.pdf', 'rb') as fernetToDecryptFile:
        toDecryptFernet = TestFernet(fernetToDecryptFile.read())
        fernetToDecryptFile.close()
    with open('Fernet-completed.pdf', 'wb') as fernetFinalFile:
        decryptedFernetData = toDecryptFernet.decrypt()
        fernetFinalFile.write(decryptedFernetData)
        fernetFinalFile.close()

    # test NaCl
    testNaCl = NaCl(testdata)
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

    # test AES
    testAES = TestAES(testdata)
    with open('AES-encrypted.pdf', 'wb') as aesEncrypted:
        aesEncrypted.write(testAES.encrypt())
        aesEncrypted.close()
    with open('AES-encrypted.pdf', 'rb') as aesToDecryptFile:
        toDecryptAES = TestAES(aesToDecryptFile.read())
        aesToDecryptFile.close()
    with open('AES-completed.pdf', 'wb') as aesFinalFile:
        decryptedAESData = toDecryptAES.decrypt()
        aesFinalFile.write(decryptedAESData)
        aesFinalFile.close()
