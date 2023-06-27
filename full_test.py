#TODO box plot of counts from characterization.py
#TODO work on readme.md
#TODO documentation
#TODO find file size where preferred order switches - between 10 and 95MB - binary search
#TODO implement asymmetric key encryption
#TODO implement lossy compression algorithm
#TODO graphs
#TODO broad narrative
#TODO examine character of the file - file hashes
#TODO more file types and sizes
#TODO consider Python Style Guide

import testcomp, testenc, time, os, shutil, sys, characterization

class Test:
    def __init__(self, *filenames):
        self.compressionMethods = [testcomp.NoZip, testcomp.Bzip, testcomp.Gzip, testcomp.Zip, testcomp.LZMA]
        self.encryptionMethods = [testenc.NoEnc, testenc.TestFernet, testenc.NaCl, testenc.TestAES]
        self.results = Sheet()
        self.resultsFolder = r'./results/'
        self.keysFolder = r'./keys/'
        self.basefilenames = list(filenames)
        self.characterKeySize = 8

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
            self.compressionFirst(filename, self.characterKeySize)
            self.encryptionFirst(filename, self.characterKeySize)

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

    def compressionFirst(self, filename, characterKeySize):
        with open(filename, 'rb') as file:
            data = file.read()
            file.close()

        compFirstInitialCharacter = characterization.getCharacter(data, characterKeySize)

        for compMethod in self.compressionMethods:
            for encMethod in self.encryptionMethods:
                compressionStartTime = time.time()
                compObj = compMethod(data)
                compressedData = compObj.compress()
                compressionTime = (time.time() - compressionStartTime) * 1000
                firstIntermediateSize = sys.getsizeof(compressedData)

                encryptionStartTime = time.time()
                encObj = encMethod(compressedData)
                encryptedData = encObj.encrypt()
                encryptionTime = (time.time() - encryptionStartTime) * 1000

                intermediateWriteStartTime = time.time()
                with open(filename + compObj.suffix + encObj.suffix, 'wb') as compEncOut:
                    compEncOut.write(encryptedData)
                    compEncOut.flush()
                    compEncOut.close()
                intermediateWriteTime = (time.time() - intermediateWriteStartTime) * 1000

                intermediateReadStartTime = time.time()
                with open(filename + compObj.suffix + encObj.suffix, 'rb') as deencFile:
                    toDecryptData = deencFile.read()
                    deencFile.close()
                intermediateReadTime = (time.time() - intermediateReadStartTime) * 1000

                decryptionStartTime = time.time()
                deencObj = encMethod(toDecryptData)
                decryptedData = deencObj.decrypt()
                decryptionTime = (time.time() - decryptionStartTime) * 1000
                
                decompressionStartTime = time.time()
                decompObj = compMethod(decryptedData)
                decompressedData = decompObj.decompress()
                decompressionTime = (time.time() - decompressionStartTime) * 1000

                finalWriteStartTime = time.time()
                with open(filename + compObj.suffix + encObj.suffix + '.decrypted.decompressed', 'wb') as finalObj:
                    finalObj.write(decompressedData)
                    finalObj.flush()
                    finalObj.close()
                finalWriteTime = (time.time() - finalWriteStartTime) * 1000

                finalSize = os.path.getsize(filename + compObj.suffix + encObj.suffix + '.decrypted.decompressed')
                if finalSize != os.path.getsize(filename):
                    print(filename, 'with', compObj.type, 'then', encObj.type + ': SIZE DIFFERS')

                self.results.addData((filename[filename.rfind('/') + 1:] + ',') + (str(os.path.getsize(filename)) + ',') +(encObj.type + ',') + (compObj.type + ',') + ('Compression First,') + (str("{:.4f}".format(encryptionTime)) + ',') + 
                                        (str("{:.4f}".format(compressionTime)) + ',') + (str(os.path.getsize(str(filename + compObj.suffix + encObj.suffix))) + ',') + (str("{:.4f}".format(decompressionTime)) + ',') + 
                                        (str("{:.4f}".format(decryptionTime)) + ',') + (str("{:.4f}".format(intermediateWriteTime)) + ',') + (str("{:.4f}".format(intermediateReadTime)) + ',') + (str("{:.4f}".format(finalWriteTime)) + ',') + 
                                        ((str(firstIntermediateSize)) + ',') + (str("{:.4f}".format(compFirstInitialCharacter['mean']) + ',')) + (str("{:.4f}".format(compFirstInitialCharacter['std']) + ',')) + 
                                        (str("{:.4f}".format(compFirstInitialCharacter['max'])) + ',') + (str(compFirstInitialCharacter['total']) + ',') + ('N/A,') + ('N/A,') + ('N/A,') + ('N/A') + '\n')

    def encryptionFirst(self, filename, characterKeySize):
        with open(filename, 'rb') as file:
            data = file.read()
            file.close()

        encFirstInitialCharacter = characterization.getCharacter(data, characterKeySize)

        for encMethod in self.encryptionMethods:
            for compMethod in self.compressionMethods:
                encryptionStartTime = time.time()
                encObj = encMethod(data)
                encryptedData = encObj.encrypt()
                encryptionTime = (time.time() - encryptionStartTime) * 1000
                firstIntermediateSize = sys.getsizeof(encryptedData)

                afterEncCharacter = characterization.getCharacter(encryptedData, characterKeySize)

                compressionStartTime = time.time()
                compObj = compMethod(encryptedData)
                compressedData = compObj.compress()
                compressionTime = (time.time() - compressionStartTime) * 1000

                intermediateWriteStartTime = time.time()
                with open(filename + encObj.suffix + compObj.suffix, 'wb') as encCompOut:
                    encCompOut.write(compressedData)
                    encCompOut.flush()
                    encCompOut.close()
                intermediateWriteTime = (time.time() - intermediateWriteStartTime) * 1000

                intermediateReadStartTime = time.time()
                with open(filename + encObj.suffix + compObj.suffix, 'rb') as decompFile:
                    toDecompressData = decompFile.read()
                    decompFile.close()
                intermediateReadTime = (time.time() - intermediateReadStartTime) * 1000

                decompressionStartTime = time.time()
                decompObjEncFirst = compMethod(toDecompressData)
                decompressedData = decompObjEncFirst.decompress()
                decompressionTime = (time.time() - decompressionStartTime) * 1000

                decryptionStartTime = time.time()
                deencObj = encMethod(decompressedData)
                decryptedData = deencObj.decrypt()
                decryptionTime = (time.time() - decryptionStartTime) * 1000

                finalWriteStartTime = time.time()
                with open(filename + encObj.suffix + compObj.suffix + '.decompressed.decrypted', 'wb') as finalObj:
                    finalObj.write(decryptedData)
                    finalObj.flush()
                    finalObj.close()
                finalWriteTime = (time.time() - finalWriteStartTime) * 1000

                finalSize = os.path.getsize(filename + encObj.suffix + compObj.suffix + '.decompressed.decrypted')
                if finalSize != os.path.getsize(filename):
                    print(filename, 'with', encObj.type, 'then', compObj.type + ': SIZE DIFFERS')

                self.results.addData((filename[filename.rfind('/') + 1:] + ',') + (str(os.path.getsize(filename)) + ',') +(encObj.type + ',') + (compObj.type + ',') + ('Encryption First,') + (str("{:.4f}".format(encryptionTime)) + ',') + 
                                    (str("{:.4f}".format(compressionTime)) + ',') + (str(os.path.getsize(str(filename + encObj.suffix + compObj.suffix))) + ',') + (str("{:.4f}".format(decompressionTime)) + ',') + 
                                    (str("{:.4f}".format(decryptionTime)) + ',') + (str("{:.4f}".format(intermediateWriteTime)) + ',') + (str("{:.4f}".format(intermediateReadTime)) + ',') + (str("{:.4f}".format(finalWriteTime)) + ',') + 
                                    (str(firstIntermediateSize) + ',') + (str("{:.4f}".format(encFirstInitialCharacter['mean'])) + ',') + (str("{:.4f}".format(encFirstInitialCharacter['std'])) + ',') + 
                                    (str("{:.4f}".format(encFirstInitialCharacter['max'])) + ',') + (str(encFirstInitialCharacter['total']) + ',') + (str("{:.4f}".format(afterEncCharacter['mean']) + ',')) + 
                                    (str("{:.4f}".format(afterEncCharacter['std'])) + ',') + (str("{:.4f}".format(afterEncCharacter['max'])) + ',') + (str(afterEncCharacter['total'])) + '\n')

class Sheet:
    def __init__(self):
        self.filename = str(str(time.strftime("%Y-%m-%d--%H-%M")) + '-results.csv')
        self.header = 'source file,source file size (B),encryption algorithm,compression algorithm,order,encryption time (ms),compression time (ms),encrypted and compressed file size (B),decompression time (ms),decryption time (ms),intermediate write time(ms),intermediate read time(ms),final write time(ms),first intermediate size (after first operation) (B),initial characterization - mean,initial characterization - std,initial characterization - max,initial characterization - total keys,after encryption characterization - mean,after encryption characterization - std,after encryption characterization - max,after encryption characterization - total keys\n'
        
        if os.path.exists(self.filename):
            print('Results file %s exists!' % self.filename)
        else:
            with open(self.filename, 'w') as file:
                file.write(self.header)
                file.close()

    def addData(self, resultsData):
        with open(self.filename, 'a') as file:
            file.write(resultsData)
            file.close()

if __name__ == '__main__':
    #test = Test('2000-word-text.txt', '10_mb.pdf', 'enwik8_1mb.txt', 'enwik8_10mb.txt', 'enwik8_95mb.txt')
    test = Test('enwik8_1mb.txt')
    test.run()