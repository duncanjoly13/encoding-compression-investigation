import djcomp, djenc, time

class Test:
    def __init__(self, filename):
        self.basefilename = filename
        self.compressionMethods = [djcomp.Bzip, djcomp.Gzip, djcomp.Zip]
        self.encryptionMethods = [djenc.DJFernet]
        self.results = Sheet

        for compMethod in self.compressionMethods:
            compObj = compMethod(filename)
            compObj.compress()
            for encMethod in self.encryptionMethods:
                encObj = encMethod(filename + compObj.suffix)
                encObj.encrypt()
                encMethod(filename + compObj.suffix + encObj.suffix).decrypt()
                compMethod(filename + compMethod.suffix + '.decrypted').decompress()
                self.results.addData((filename + ',') + (str(compMethod.filesize) + ',') +(encMethod.type + ',') + (compMethod.type + ',') + ('Compression First,') + (str(encMethod.encryptionTime) + ',') + (str(compMethod.compressionTime) + ',') + (str(encMethod.encryptedSize) + ',') + (str(compMethod.compressedSize) + ',') + (str(compMethod.decompresionTime) + ',') + (str(encMethod.decryptionTime) + '\n'))

        for encMethod in self.encryptionMethods:
            encMethod(filename).encrypt()
            for compMethod in self.compressionMethods:
                compMethod(filename + encMethod.suffix).compress()
                compMethod(filename + encMethod.suffix + compMethod.suffix).decompress()
                encMethod(filename + encMethod.suffix + '.decompressed').decrypt()
                self.results.addData((filename + ',') + (str(compMethod.filesize) + ',') +(encMethod.type + ',') + (compMethod.type + ',') + ('Compression First,') + (str(encMethod.encryptionTime) + ',') + (str(compMethod.compressionTime) + ',') + (str(encMethod.encryptedSize) + ',') + (str(compMethod.compressedSize) + ',') + (str(compMethod.decompresionTime) + ',') + (str(encMethod.decryptionTime) + '\n'))

class Sheet:
    def __init__(self):
        self.filename = str(str(time.strftime("%Y-%m-%d %H:%M")) + '-results.csv')
        self.header = 'source file, source file size (b), encryption algorithm, compression algorithm, order, encryption time (s), compression time (s), encrypted file size (b), compressed file size (b), decompression time (s), decryption time (s)\n'
        self.file = open(self.filename, 'w')
        self.file.write(self.header)
        self.file.close()

    def addData(self, data):
        self.file.write(data)

if __name__ == '__main__':
    Test('2000-word-text.txt')
