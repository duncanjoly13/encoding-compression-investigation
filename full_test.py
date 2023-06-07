#TODO fix Fernet-firsts and files ending with NoEnc or Fernet
#TODO graphs
#TODO broad narrative
#TODO fix NaCl UnicodeDecodeError or decide on other method
#TODO implement asymmetric key encryption
#TODO implement lossy compression algorithm
#TODO more file types and sizes
#TODO detect invalid files in filelist
#TODO handle existing results file - throw error and require that file is deleted first

import djcomp, djenc, time, os, shutil

class Test:
    def __init__(self, *filenames):
        self.compressionMethods = [djcomp.NoZip, djcomp.Bzip, djcomp.Gzip, djcomp.Zip]
        self.encryptionMethods = [djenc.NoEnc, djenc.DJFernet]
        self.results = Sheet()
        self.resultsFolder = r'./results/'
        self.keysFolder = r'./keys/'
        self.basefilenames = list(filenames)

        if os.path.exists(self.resultsFolder):
            print("%s exists!" % self.resultsFolder)
        else:
            os.makedirs(self.resultsFolder)

        if os.path.exists(self.keysFolder):
            print("%s exists!" % self.keysFolder)
        else:
            os.makedirs(self.keysFolder)

        for filename in filenames:
            if os.path.exists(filename):
                with open(filename, 'rb') as sourceFile:
                    with open(str(self.resultsFolder + filename), 'wb') as newFile:
                        newFile.write(sourceFile.read())
                        newFile.flush()
                        newFile.close()
                        sourceFile.close()
            else: 
                print("%s does not exist!" % filename)

        self.basefilenames = []

        for filename in filenames:
            self.basefilenames.append(self.resultsFolder + filename)
            
    def run(self):
        for filename in self.basefilenames:
            self.compressionFirst(filename)
            self.encryptionFirst(filename)

        '''if os.path.isdir(self.resultsFolder):
            shutil.rmtree(self.resultsFolder)
        else:
            print("Error: %s file not found" % self.resultsFolder)'''

        if os.path.isdir(self.keysFolder):
            shutil.rmtree(self.keysFolder)
        else:
            print("Error: %s file not found" % self.keysFolder)

        if os.path.isdir('__pycache__'):
            shutil.rmtree('__pycache__')
        else:
            print("No pycache folder, not deleting")

    def compressionFirst(self, filename):
        with open(filename, 'rb') as file:
            for compMethod in self.compressionMethods:
                compObj = compMethod(file.read())
                for encMethod in self.encryptionMethods:
                    compressionStartTime = time.time()
                    encObj = encMethod(compObj.compress())
                    compressionTime = (time.time() - compressionStartTime) * 1000 

                    encryptionStartTime = time.time()
                    with open(filename + compObj.suffix + encObj.suffix, 'wb') as compEncOut:
                        compEncOut.write(encObj.encrypt())
                        compEncOut.flush()
                        compEncOut.close()
                    encryptionAndWriteTime = (time.time() - encryptionStartTime) * 1000

                    decryptionStartTime = time.time()
                    with open(filename + compObj.suffix + encObj.suffix, 'rb') as deencFile:
                        deencObj = encMethod(deencFile.read())
                        deencFile.close()
                        decompObj = compMethod(deencObj.decrypt())
                        decryptionTime = (time.time() - decryptionStartTime) * 1000

                        decompressionStartTime = time.time()
                        with open(filename + compObj.suffix + encObj.suffix + '.decrypted.decompressed', 'wb') as finalObj:
                            finalObj.write(decompObj.decompress())
                            finalObj.flush()
                            finalObj.close()
                            decompressionAndWriteTime = (time.time() - decompressionStartTime) * 1000

                            finalSize = os.path.getsize(filename + compObj.suffix + encObj.suffix + '.decrypted.decompressed')
                            if finalSize != os.path.getsize(filename):
                                print(filename, 'with', compObj.type, 'then', encObj.type + ': SIZE DIFFERS')

                            self.results.addData((filename[filename.rfind('/') + 1:] + ',') + (str(os.path.getsize(filename)) + ',') +(encObj.type + ',') + (compObj.type + ',') + ('Compression First,') + (str("{:.3f}".format(encryptionAndWriteTime)) + ',') + 
                                                 (str("{:.3f}".format(compressionTime)) + ',') + (str(os.path.getsize(str(filename + compObj.suffix + encObj.suffix))) + ',') + (str("{:.3f}".format(decompressionAndWriteTime)) + ',') + 
                                                 (str("{:.3f}".format(decryptionTime)) + ',') + (str("{:.3f}".format(encryptionAndWriteTime + decryptionTime + compressionTime + decompressionAndWriteTime))) + '\n')
            file.close()

    def encryptionFirst(self, filename):
        with open(filename, 'rb') as file:
            for encMethod in self.encryptionMethods:
                encObj = encMethod(file.read())
                for compMethod in self.compressionMethods:
                    encryptionStartTime = time.time()
                    compObj = compMethod(encObj.encrypt())
                    encryptionTime = (time.time() - encryptionStartTime) * 1000
                    
                    compressionStartTime = time.time()
                    with open(filename + encObj.suffix + compObj.suffix, 'wb') as encCompOut:
                        encCompOut.write(compObj.compress())
                        encCompOut.flush()
                        encCompOut.close()
                    compressionAndWriteTime = (time.time() - compressionStartTime) * 1000

                    decompressionStartTime = time.time()
                    with open(filename + encObj.suffix + compObj.suffix, 'rb') as decompFile:
                        decompObj = compMethod(decompFile.read())
                        decompFile.close()
                        deencObj = encMethod(decompObj.decompress())
                        decompressionTime = (time.time() - decompressionStartTime) * 1000

                        decryptionStartTime = time.time()
                        with open(filename + encObj.suffix + compObj.suffix + '.decompressed.decrypted', 'wb') as finalObj:
                            finalObj.write(deencObj.decrypt())
                            finalObj.flush()
                            finalObj.close()
                            decryptionAndWriteTime = (time.time() - decryptionStartTime) * 1000

                            finalSize = os.path.getsize(filename + encObj.suffix + compObj.suffix + '.decompressed.decrypted')
                            if finalSize != os.path.getsize(filename):
                                print(filename, 'with', encObj.type, 'then', compObj.type + ': SIZE DIFFERS')

                            self.results.addData((filename[filename.rfind('/') + 1:] + ',') + (str(os.path.getsize(filename)) + ',') +(encObj.type + ',') + (compObj.type + ',') + ('Encryption First,') + (str("{:.3f}".format(encryptionTime)) + ',') + 
                                             (str("{:.3f}".format(compressionAndWriteTime)) + ',') + (str(os.path.getsize(str(filename + encObj.suffix + compObj.suffix))) + ',') + (str("{:.3f}".format(decompressionTime)) + ',') + 
                                             (str("{:.3f}".format(decryptionAndWriteTime)) + ',') + (str("{:.3f}".format(encryptionTime + decryptionAndWriteTime + compressionAndWriteTime + decompressionTime))) + '\n')
            file.close()

class Sheet:
    def __init__(self):
        self.filename = str(str(time.strftime("%Y-%m-%d--%H-%M")) + '-results.csv')
        self.header = 'source file,source file size (b),encryption algorithm,compression algorithm,order,encryption time (ms),compression time (ms),encrypted and compressed file size (b),decompression time (ms),decryption time (ms),total operation time (ms)\n'
        file = open(self.filename, 'w')
        file.write(self.header)
        file.close()

    def addData(self, data):
        file = open(self.filename, 'a')
        file.write(data)
        file.close()

if __name__ == '__main__':
    #test = Test('2000-word-text.txt', '10_mb.pdf', 'enwik8_1mb.txt', 'enwik8_10mb.txt', 'enwik8_95mb.txt')
    test = Test('10_mb.pdf')
    test.run()