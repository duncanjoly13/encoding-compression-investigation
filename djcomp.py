#TODO add FileExists and FileNotFound error handing
#TODO fix having extra \n

# Import modules
import gzip, os, shutil, time, bz2, zipfile

class Gzip:
    def __init__(self, filename = '2000-word-text.txt'):
        self.filesize = os.path.getsize(filename)
        self.type = 'gzip'
        self.filename = filename
        self.compressionTime = 0
        self.decompressionTime = 0
        self.uncompressedSize = 0
        self.compressedSize = 0

    def compress(self):
        beforeCompressionTime = time.time()
        with open(self.filename, 'rb') as f_in:
            with gzip.open(str(self.filename + '.gz'), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            f_in.close()
            f_out.close()
        self.compressionTime = time.time() - beforeCompressionTime

    def decompress(self):
        beforeDecompressionTime = time.time()
        with open(self.filename, 'rb') as f_in:
            with open(str(self.filename + 'decompressed'), 'w') as f_out:
                data_in = f_in.read()
                decompressedData = gzip.decompress(data_in)
                f_out.write(decompressedData.decode('ascii'))
                f_in.close()
                f_out.close()
        self.decompressionTime = time.time() - beforeDecompressionTime

class Bzip:
    def __init__(self, filename = '2000-word-text.txt'):
        self.filesize = os.path.getsize(filename)
        self.type = 'bzip'
        self.filename = filename
        self.compressionTime = 0
        self.decompressionTime = 0
        self.uncompressedSize = 0
        self.compressedSize = 0

    def compress(self):
        beforeCompressionTime = time.time()
        with open(self.filename, 'r') as f_in:
            with bz2.open(str(self.filename + '.bzip'), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            f_in.close()
            f_out.close()
        self.compressionTime = time.time() - beforeCompressionTime

    def decompress(self):
        beforeDecompressionTime = time.time()
        with open(self.filename, 'r') as f_in:
            with open(str(self.filename + 'decompressed'), 'w') as f_out:
                data_in = f_in.read()
                decompressedData = bz2.decompress(data_in)
                f_out.write(decompressedData.decode('ascii'))
                f_in.close()
                f_out.close()
        self.decompressionTime = time.time() - beforeDecompressionTime

class Zip:
    def __init__(self, filename = '2000-word-text.txt'):
        self.filesize = os.path.getsize(filename)
        self.type = 'zip'
        self.filename = filename
        self.compressionTime = 0
        self.decompressionTime = 0
        self.uncompressedSize = 0
        self.compressedSize = 0

    def compress(self):
        beforeCompressionTime = time.time()
        with open(self.filename, 'r') as f_in:
            with zipfile.ZipFile(str(self.filename + '.zip'), 'w') as f_out:
                f_out.write(self.filename)
            f_in.close()
            f_out.close()
        self.compressionTime = time.time() - beforeCompressionTime

    def decompress(self):
        beforeDecompressionTime = time.time()
        with zipfile.ZipFile(self.filename) as f_in:
            with open(str(self.filename + 'decompressed'), 'w') as f_out:
                data_in = f_in.read(self.filename.rstrip('.zip'))
                f_out.write(data_in.decode('ascii'))
                f_in.close()
                f_out.close()
        self.decompressionTime = time.time() - beforeDecompressionTime

if __name__ == '__main__':
    '''uncompressed = Gzip('2000-word-text.txt')
    compressed = uncompressed.compress()
    newCompressed = Gzip('2000-word-text.txt.gz')
    decompressed = newCompressed.decompress()'''

    '''uncompressed = Bzip('2000-word-text.txt')
    compressed = uncompressed.compress()
    newCompressed = Bzip('2000-word-text.txt.bz')
    decompressed = newCompressed.decompress()'''

    '''uncompressed = Zip('2000-word-text.txt')
    compressed = uncompressed.compress()
    newCompressed = Zip('2000-word-text.txt.zip')
    decompressed = newCompressed.decompress()'''