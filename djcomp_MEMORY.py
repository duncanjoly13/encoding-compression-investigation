#TODO test zip
#TODO add FileExists and FileNotFound error handing
#TODO fix having extra \n

# Import modules
import gzip, bz2, zipfile

class Gzip:
    def __init__(self, data):
        self.data = data
        self.type = 'gzip'
        self.suffix = '.gz'

    def compress(self):
        binaryData = str.encode(self.data)
        return gzip.compress(binaryData)

    def decompress(self):
        return gzip.decompress(self.data)

class Bzip:
    def __init__(self, data):
        self.suffix = '.bzip'
        self.type = 'bzip'
        self.data = data

    def compress(self):
        binaryData = str.encode(self.data)
        return bz2.compress(binaryData)
    def decompress(self):
        return bz2.decompress(self.data)

class Zip:
    def __init__(self, data):
        self.suffix = '.zip'
        self.type = 'zip'
        self.data = data

    def compress(self):
        zippedData = zipfile.ZipFile(self.data)
        return zippedData

    def decompress(self):
        toUnzip = zipfile.ZipFile(self.data)
        return toUnzip.extractall()

if __name__ == '__main__':
    testdata = open('2000-word-text.txt').read()
    
    '''bzipped = Bzip(testdata).compress()
    unbzipped = Bzip(bzipped).decompress()
    with open('bzip-complete.txt', 'wb') as output:
        output.write(unbzipped)
        output.close()'''
    
    '''gzipped = Gzip(testdata).compress()
    ungzipped = Gzip(gzipped).decompress()
    with open('gzip-complete.txt', 'wb') as output:
        output.write(ungzipped)
        output.close()'''

    zipped = Zip(testdata).compress()
    unzipped = Zip(zipped).decompress()
    with open('zip-complete.txt', 'wb') as output:
        output.write(unzipped)
        output.close()