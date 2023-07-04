import gzip, bz2, zipfile, io, lzma

class NoZip:
    def __init__(self, data):
        self.data = data
        self.type = 'NoZip'
        self.suffix = '.nozip'

    def compress(self):
        if type(self.data) != bytes:
            return str.encode(self.data)
        else:
            return self.data
    
    def decompress(self):
        if type(self.data) != bytes:
            return str.encode(self.data)
        else:
            return self.data

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
    
class LZMA:
    def __init__(self, data):
        self.suffix = '.lzma'
        self.type = 'lzma'
        self.data = data

    def compress(self):
        if type(self.data) != bytes:
            self.data = str.encode(self.data)
        return lzma.compress(self.data)
    
    def decompress(self):
        if type(self.data) != bytes:
            self.data = str.encode(self.data)
        return lzma.decompress(self.data)
    
if __name__ == '__main__':
    with open('10_mb.pdf', 'rb') as file:
        testdata = file.read()
        file.close()

    # test NoZip
    nozipped = NoZip(testdata).compress()
    with open('nozip-compressed.pdf', 'wb') as output:
        output.write(nozipped)
        output.close()
    toUnNozip = open('nozip-compressed.pdf', 'rb').read()
    unnozipped = NoZip(toUnNozip).decompress()
    with open('nozip-complete.pdf', 'wb') as output:
        output.write(unnozipped)
        output.close()
    
    # test Bzip
    bzipped = Bzip(testdata).compress()
    with open('bzip-compressed.pdf', 'wb') as output:
        output.write(bzipped)
        output.close()
    toUnBzip = open('bzip-compressed.pdf', 'rb').read()
    unbzipped = Bzip(toUnBzip).decompress()
    with open('bzip-complete.pdf', 'wb') as output:
        output.write(unbzipped)
        output.close()

    # test Gzip
    gzipped = Gzip(testdata).compress()
    with open('gzip-compressed.pdf', 'wb') as output:
        output.write(gzipped)
        output.close()
    toUnGzip = open('gzip-compressed.pdf', 'rb').read()
    ungzipped = Gzip(toUnGzip).decompress()
    with open('gzip-complete.pdf', 'wb') as output:
        output.write(ungzipped)
        output.close()

    # test Zip
    zipped = Zip(testdata).compress()
    with open('zip-compressed.pdf', 'wb') as output:
        output.write(zipped)
        output.close()
    toUnZip = open('zip-compressed.pdf', 'rb').read()
    unzipped = Zip(toUnZip).decompress()
    with open('zip-complete.pdf', 'wb') as output:
        output.write(unzipped)
        output.close()

    # test LZMA
    LZMAtest = LZMA(testdata).compress()
    with open('lzma-compressed.pdf', 'wb') as output:
        output.write(LZMAtest)
        output.close()
    toUnLZMA = open('lzma-compressed.pdf', 'rb').read()
    unLZMAed = LZMA(toUnLZMA).decompress()
    with open('lzma-complete.pdf', 'wb') as output:
        output.write(unLZMAed)
        output.close()