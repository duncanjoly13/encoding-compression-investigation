#TODO implement output folder
#TODO add FileExists and FileNotFound error handing
#TODO fix having extra \n

# Import modules
import gzip, os, shutil, time, bz2, zipfile

class Gzip:
    def __init__(self, filename):
        self.filesize = os.path.getsize(filename)
        self.type = 'gzip'
        self.filename = ''
        if self.filename.find('results') > -1:
            self.filename = self.filename[(self.filename.find('results/') + 8):]
        else:
            self.filename = filename
        self.compressionTime = 0
        self.decompressionTime = 0
        self.uncompressedSize = 0
        self.compressedSize = 0
        self.suffix = '.gz'

    def compress(self):
        beforeCompressionTime = time.time()
        with open(self.filename, 'rb') as f_in:
            with gzip.open(str(self.filename + self.suffix), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            f_in.close()
            f_out.close()
        self.compressionTime = time.time() - beforeCompressionTime
        self.compressedSize = str(os.path.getsize(str(self.filename + self.suffix)))

    def decompress(self):
        beforeDecompressionTime = time.time()
        with open(self.filename, 'rb') as f_in:
            with open(str(self.filename + '.decompressed'), 'wb') as f_out:
                data_in = f_in.read()
                decompressedData = gzip.decompress(data_in)
                f_out.write(decompressedData)
                f_in.close()
                f_out.close()
        self.decompressionTime = time.time() - beforeDecompressionTime
        self.decompressedSize = str(os.path.getsize(self.filename))

class Bzip:
    def __init__(self, filename):
        self.type = 'bzip'
        self.compressionTime = 0
        self.decompressionTime = 0
        self.uncompressedSize = 0
        self.compressedSize = 0
        self.suffix = '.bzip'
        if filename.find('results') > -1:
            self.filename = filename[(filename.find('results/') + 8):]
        else:
            self.filename = filename
        self.filesize = os.path.getsize(filename)

    def compress(self):
        beforeCompressionTime = time.time()
        with open('./results/' + self.filename, 'rb') as f_in:
            with bz2.open(str('./results/' + self.filename + self.suffix), 'wb') as f_out:
                f_out.write(f_in.read())
                f_out.flush()
            f_in.close()
            f_out.close()
        self.compressionTime = time.time() - beforeCompressionTime
        self.compressedSize = str(os.path.getsize(str('./results/' + self.filename + self.suffix)))

    def decompress(self):
        beforeDecompressionTime = time.time()
        with bz2.open('./results/' + self.filename, 'rb') as f_in:
            with open(str('./results/' + self.filename + '.decompressed'), 'wb') as f_out:
                data_in = f_in.read()
                f_out.write(data_in)
                f_out.close()
        self.decompressionTime = time.time() - beforeDecompressionTime
        self.decompressedSize = str(os.path.getsize('./results/' + self.filename))

class Zip:
    def __init__(self, filename):
        self.filesize = os.path.getsize(filename)
        self.type = 'zip'
        self.compressionTime = 0
        self.decompressionTime = 0
        self.uncompressedSize = 0
        self.compressedSize = 0
        self.suffix = '.zip'
        '''if self.filename.find('results') > -1:
            self.filename = filename[(filename.find('results/') + 8):]
        else:
            self.filename = filename'''
        self.filename = filename[(filename.find('results/') + 8):]

    def compress(self):
        beforeCompressionTime = time.time()
        with open('./results/' + self.filename, 'r') as f_in:
            with zipfile.ZipFile(str('./results/' + self.filename + self.suffix), 'w') as f_out:
                f_out.write('./results/' + self.filename)
            f_in.close()
            f_out.close()
        self.compressionTime = time.time() - beforeCompressionTime
        self.compressedSize = str(os.path.getsize(str('./results/' + self.filename + self.suffix)))

    def decompress(self):
        beforeDecompressionTime = time.time()
        with zipfile.ZipFile('./results/' + self.filename) as f_in:
            with open(str('./results/' + self.filename + '.decompressed'), 'w') as f_out:
                newFilename = self.filename[:self.filename.find('.zip')]
                print(f_in.filename)
                print('./results/' + newFilename)
                data_in = f_in.read(newFilename)
                f_out.write(data_in.decode('ascii'))
                f_in.close()
                f_out.close()
        self.decompressionTime = time.time() - beforeDecompressionTime
        self.decompressedSize = str(os.path.getsize('./results/' + self.filename))

if __name__ == '__main__':
    '''uncompressed = Gzip('2000-word-text.txt')
    compressed = uncompressed.compress()
    newCompressed = Gzip('2000-word-text.txt.gz')
    decompressed = newCompressed.decompress()'''

    '''uncompressed = Bzip('2000-word-text.txt')
    compressed = uncompressed.compress()
    newCompressed = Bzip('2000-word-text.txt.bzip')
    decompressed = newCompressed.decompress()'''

    '''uncompressed = Zip('2000-word-text.txt')
    compressed = uncompressed.compress()
    newCompressed = Zip('2000-word-text.txt.zip')
    decompressed = newCompressed.decompress()'''