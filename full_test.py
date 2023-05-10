#TODO fix times
#TODO implement output folder, excess file deletion after test is run
#TODO fix source file size
#TODO add FileExists and FileNotFound error handing

import djcomp, djenc, time, os, shutil

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

    def run(self):
        self.compressionFirst(self.basefilename)
        self.encryptionFirst(self.basefilename)

    def compressionFirst(self, filename):
        with open(filename) as file:
            for compMethod in self.compressionMethods:
                compObj = compMethod(file.read())
                for encMethod in self.encryptionMethods:
                    compressionStartTime = time.time()
                    encObj = encMethod(compObj.compress())
                    compressionTime = time.time() - compressionStartTime

                    encryptionStartTime = time.time()
                    with open(filename + compObj.suffix + encObj.suffix, 'wb') as compEncOut:
                        compEncOut.write(encObj.encrypt())
                        compEncOut.flush()
                        compEncOut.close()
                    encryptionAndWriteTime = time.time() - encryptionStartTime

                    decryptionStartTime = time.time()
                    with open(filename + compObj.suffix + encObj.suffix) as deencFile:
                        deencObj = encMethod(deencFile.read())
                        decompObj = compMethod(deencObj.decrypt())
                        deencFile.close()
                        decryptionTime = time.time() - decryptionStartTime

                        decompressionStartTime = time.time()
                        with open(filename + compObj.suffix + encObj.suffix + '.decrypted.decompressed', 'wb') as finalObj:
                            finalObj.write(decompObj.decompress())
                            finalObj.flush()
                            finalObj.close()
                            decompressionAndWriteTime = time.time() - decompressionStartTime

                            self.results.addData((filename + ',') + (str(os.path.getsize(filename)) + ',') +(encObj.type + ',') + (compObj.type + ',') + ('Compression First,') + (str(encryptionAndWriteTime) + ',') + 
                                                 (str(compressionTime) + ',') + (str(os.path.getsize(filename + compObj.suffix + encObj.suffix)) + ',') + (str(decompressionAndWriteTime) + ',') + 
                                                 (str(decryptionTime) + ',') + (str(encryptionAndWriteTime + decryptionTime + compressionTime + decompressionAndWriteTime)) + '\n')
        file.close()

    def encryptionFirst(self, filename):
        with open(filename) as file:
            for encMethod in self.encryptionMethods:
                encObj = encMethod(file.read())
                for compMethod in self.compressionMethods:
                    encryptionStartTime = time.time()
                    compObj = compMethod(encObj.encrypt())
                    encryptionTime = time.time() - encryptionStartTime
                    
                    compressionStartTime = time.time()
                    with open(filename + encObj.suffix + compObj.suffix, 'wb') as encCompOut:
                        encCompOut.write(compObj.compress())
                        encCompOut.flush()
                        encCompOut.close()
                    compressionAndWriteTime = time.time() - compressionStartTime

                    decompressionStartTime = time.time()
                    with open(filename + encObj.suffix + compObj.suffix, 'rb') as decompFile:
                        decompObj = compMethod(decompFile.read())
                        deencObj = encMethod(decompObj.decompress())
                        decompressionTime = time.time() - decompressionStartTime

                        decryptionStartTime = time.time()
                        with open(filename + encObj.suffix + compObj.suffix + '.decompressed.decrypted', 'wb') as finalObj:
                            finalObj.write(deencObj.decrypt())
                            finalObj.flush()
                            finalObj.close()
                            decryptionAndWriteTime = time.time() - decryptionStartTime

                        self.results.addData((filename + ',') + (str(os.path.getsize(filename)) + ',') +(encObj.type + ',') + (compObj.type + ',') + ('Encryption First,') + (str(encryptionTime) + ',') + 
                                             (str(compressionAndWriteTime) + ',') + (str(os.path.getsize(filename + compObj.suffix + encObj.suffix)) + ',') + (str(decompressionTime) + ',') + 
                                             (str(decryptionAndWriteTime) + ',') + (str(encryptionTime + decryptionAndWriteTime + compressionAndWriteTime + decompressionTime)) + '\n')
        file.close()

        if os.path.isdir(self.resultsFolder):
            shutil.rmtree(self.resultsFolder)
        else:
            print("Error: %s file not found" % self.resultsFolder)

        if os.path.isdir(self.keysFolder):
            shutil.rmtree(self.keysFolder)
        else:
            print("Error: %s file not found" % self.keysFolder)

        if os.path.isdir('__pycache__'):
            shutil.rmtree('__pycache__')
        else:
            print("No pycache folder, not deleting")


class Sheet:
    def __init__(self):
        self.filename = str(str(time.strftime("%Y-%m-%d--%H-%M")) + '-results.csv')
        self.header = 'source file, source file size (b), encryption algorithm, compression algorithm, order, encryption time (s), compression time (s), encrypted and compressed file size (b), \
                                decompression time (s), decryption time (s), total time (s)\n'
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
