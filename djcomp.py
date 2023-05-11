# Import modules
import gzip, bz2, zipfile, io

class Gzip:
    def __init__(self, data):
        self.data = data
        self.type = 'gzip'
        self.suffix = '.gz'

    def compress(self):
        if type(self.data) != bytes:
            self.data = str.encode(self.data)
        return gzip.compress(self.data)

    def decompress(self):
        return gzip.decompress(self.data)

class Bzip:
    def __init__(self, data):
        self.suffix = '.bzip'
        self.type = 'bzip'
        self.data = data

    def compress(self):
        if type(self.data) != bytes:
            self.data = str.encode(self.data)
        return bz2.compress(self.data)
    
    def decompress(self):
        if type(self.data) != bytes:
            self.data = str.encode(self.data)
        return bz2.decompress(self.data)

class Zip:
    def __init__(self, data):
        self.suffix = '.zip'
        self.type = 'zip'
        self.data = data
    
    def compress(self):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr('data', self.data)
        compressed_data = zip_buffer.getvalue()
        return compressed_data

    def decompress(self):
        file_buffer = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(self.data), mode='r') as zip_file:
            file_buffer.write(zip_file.read('data'))
        file_buffer.seek(0)
        return file_buffer.read()

if __name__ == '__main__':
    testdata = open('2000-word-text.txt').read()
    
    bzipped = Bzip(testdata).compress()
    unbzipped = Bzip(bzipped).decompress()
    with open('bzip-complete.txt', 'wb') as output:
        output.write(unbzipped)
        output.close()
    
    gzipped = Gzip(testdata).compress()
    ungzipped = Gzip(gzipped).decompress()
    with open('gzip-complete.txt', 'wb') as output:
        output.write(ungzipped)
        output.close()

    zipped = Zip(testdata).compress()
    unzipped = Zip(zipped).decompress()
    with open('zip-complete.txt', 'wb') as output:
        output.write(unzipped)
        output.close()

if __name__ == '__main__':
    '''# Test Bzip
    with open('2000-word-text.txt') as file:
        testBzip = Bzip(file.read())
        with open('compressed.out', 'wb') as compressed:
            compressed.write(testBzip.compress())
            compressed.close()
        file.close()
    with open('compressed.out', 'rb') as toDecompress:
        toDecompressBzip = Bzip(toDecompress.read())
        with open('finished.out', 'w') as finalFile:
            finalFile.write(toDecompressBzip.decompress().decode())
            finalFile.close()
        toDecompress.close()'''
