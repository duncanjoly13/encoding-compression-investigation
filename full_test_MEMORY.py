#TODO add write and read time
#TODO only write completed files (enc.comp or comp.enc)
#TODO implement output folder, excess file deletion after test is run
#TODO fix source file size

import djcomp_MEMORY, djenc_MEMORY, time, os

class Test:
    def __init__(self, filename):
        self.compressionMethods = [djcomp_MEMORY.Bzip, djcomp_MEMORY.Gzip, djcomp_MEMORY.Zip]
        self.encryptionMethods = [djenc_MEMORY.DJFernet]
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

    def run(self):
        self.compressionFirst(self.basefilename)
        self.encryptionFirst(self.basefilename)

    def compressionFirst(self, filename):
        #TODO take timings
        #TODO take sizings
        for compMethod in self.compressionMethods:
            compObj = compMethod(filename)
            for encMethod in self.encryptionMethods:
                encObj = encMethod(compObj.compress())

                with open(filename + compObj.suffix + encObj.suffix, 'wb') as compEncOut:
                    compEncOut.write(encObj.encrypt())
                    compEncOut.flush()
                    compEncOut.close()

                deencObj = encMethod(self.resultsFolder + filename + compObj.suffix + encObj.suffix)
                decompObj = compMethod(deencObj.decrypt())
                
                with open(self.resultsFolder + filename + compObj.suffix + encObj.suffix + '.decrypted.decompressed', 'wb') as finalObj:
                    finalObj.write(decompObj.decompress())
                    finalObj.flush()
                    finalObj.close()

                self.results.addData(str((filename + ',') + (str(compObj.filesize) + ',') +(encObj.type + ',') + (compObj.type + ',') + ('Compression First,') + (str(encObj.encryptionTime) + ',') + (str(compObj.compressionTime) + ',') + (str(encObj.encryptedSize) + ',') + (str(compObj.compressedSize) + ',') + (str(decompObj.decompressionTime) + ',') + (str(deencObj.decryptionTime) + '\n')))

    def encryptionFirst(self, filename):
        #TODO take timings
        #TODO take sizings
        for encMethod in self.encryptionMethods:
            encObj = encMethod(filename)
            for compMethod in self.compressionMethods:
                compObj = compMethod(encObj.encrypt())
                
                with open(self.resultsFolder + filename + encObj.suffix + compObj.suffix, 'wb') as encCompOut:
                    encCompOut.write(compObj.compress())
                    encCompOut.flush()
                    encCompOut.close()

                decompObj = encMethod(self.resultsFolder + filename + compObj.suffix + encObj.suffix)
                deencObj = encMethod(decompObj.decompress())

                with open(self.resultsFolder + filename + encObj.suffix + compObj.suffix + '.decompressed.decrypted', 'wb') as finalObj:
                    finalObj.write(deencObj.decrypt())
                    finalObj.flush()
                    finalObj.close()

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
