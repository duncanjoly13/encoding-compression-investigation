#TODO add write and read time
#TODO only write completed files (enc.comp or comp.enc)
#TODO implement output folder, excess file deletion after test is run
#TODO fix source file size

import djcomp, djenc, time, os

class Test:
    def __init__(self, filename):
        self.compressionMethods = [djcomp.Bzip, djcomp.Gzip, djcomp.Zip]
        self.encryptionMethods = [djenc.DJFernet]
        self.results = Sheet()
        self.resultsFolder = r'./results/'
        self.keysFolder = r'./keys/'
        self.basefilename = filename

        os.makedirs(self.resultsFolder)
        os.makedirs(self.keysFolder)
        with open(filename) as sourceFile:
            with open(str(self.resultsFolder + filename), 'w') as newFile:
                newFile.write(sourceFile.read())
                newFile.flush()
                newFile.close()
                sourceFile.close()
        self.basefilename = self.resultsFolder + self.basefilename
        '''else:
            print(resultsFolder, 'exists!')
            self.basefilename = '''''

    def run(self):
        self.compressionFirst(self.basefilename)
        self.encryptionFirst(self.basefilename)

    def compressionFirst(self, filename):
        for compMethod in self.compressionMethods:
            compObj = compMethod(filename)
            compObj.compress()
            for encMethod in self.encryptionMethods:
                encObj = encMethod(filename + compObj.suffix)
                encObj.encrypt()
                deencObj = encMethod(filename + compObj.suffix + encObj.suffix)
                deencObj.decrypt()
                decompObj = compMethod(filename + compObj.suffix + encObj.suffix + '.decrypted')
                decompObj.decompress()
                self.results.addData(str((filename + ',') + (str(compObj.filesize) + ',') +(encObj.type + ',') + (compObj.type + ',') + ('Compression First,') + (str(encObj.encryptionTime) + ',') + (str(compObj.compressionTime) + ',') + (str(encObj.encryptedSize) + ',') + (str(compObj.compressedSize) + ',') + (str(decompObj.decompressionTime) + ',') + (str(deencObj.decryptionTime) + '\n')))

    def encryptionFirst(self, filename):
        for encMethod in self.encryptionMethods:
            encObj = encMethod(filename)
            encObj.encrypt()
            for compMethod in self.compressionMethods:
                compObj = compMethod(filename + encObj.suffix)
                compObj.compress()
                decompObj = compMethod(str(filename + encObj.suffix + compObj.suffix))
                decompObj.decompress()
                deencObj = encMethod(filename + encObj.suffix +  decompObj.suffix + '.decompressed')
                deencObj.decrypt()
                self.results.addData((filename + ',') + (str(compObj.filesize) + ',') +(encObj.type + ',') + (compObj.type + ',') + ('Encryption First,') + (str(encObj.encryptionTime) + ',') + (str(compObj.compressionTime) + ',') + (str(encObj.encryptedSize) + ',') + (str(compObj.compressedSize) + ',') + (str(decompObj.decompressionTime) + ',') + (str(deencObj.decryptionTime) + '\n'))

class Sheet:
    def __init__(self):
        self.filename = str(str(time.strftime("%Y-%m-%d--%H-%M")) + '-results.csv')
        self.header = 'source file, source file size (b), encryption algorithm, compression algorithm, order, encryption time (s), compression time (s), encrypted file size (b), compressed file size (b), decompression time (s), decryption time (s)\n'
        file = open(self.filename, 'w')
        file.write(self.header)
        file.close()

    def addData(self, data):
        file = open(self.filename, 'a')
        file.write(data)
        file.close()

if __name__ == '__main__':
    test = Test('2000-word-text.txt')
    test.run()