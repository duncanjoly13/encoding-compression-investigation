#TODO implement bzip and/or tarzip
#TODO add FileExists and FileNotFound error handing
#TODO fix gzip decompress() having extra \n

# Import modules
import gzip, os, shutil, time

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
        afterCompressionTime = time.time()
        self.compressionTime = afterCompressionTime - beforeCompressionTime

    def decompress(self):
        beforeDecompressionTime = time.time()
        with open(self.filename, 'rb') as f_in:
            with open(str(self.filename + 'decompressed'), 'w') as f_out:
                data_in = f_in.read()
                decompressedData = gzip.decompress(data_in)
                f_out.write(decompressedData.decode('ascii'))
                f_in.close()
                f_out.close()
        afterDecompressionTime = time.time()
        self.decompressionTime = afterDecompressionTime - beforeDecompressionTime

if __name__ == '__main__':
    uncompressed = Gzip('2000-word-text.txt')
    compressed = uncompressed.compress()
    newCompressed = Gzip('2000-word-text.txt.gz')
    decompressed = newCompressed.decompress()