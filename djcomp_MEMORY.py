#TODO test zip
#TODO add FileExists and FileNotFound error handing
#TODO fix having extra \n

# Import modules
import gzip, bz2, zipfile, io

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
        # self.in_memory_zip = io.StringIO()

    '''def compress(self):
        file = zipfile.ZipFile(self.in_memory_zip, 'a', zipfile.ZIP_DEFLATED, False)
        file.writestr('data', self.data.encode())
        return file'''
    
    def compress(self):
        # Create an in-memory bytes buffer to hold the compressed data
        zip_buffer = io.BytesIO()
        # Create a ZipFile object with the buffer as the output file
        with zipfile.ZipFile(zip_buffer, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            # Add the file contents to the ZIP archive with the given filename
            zip_file.writestr('data', self.data)
        # Get the compressed data as a bytes object
        compressed_data = zip_buffer.getvalue()
        return compressed_data

    '''def decompress(self):
        pretendObject = io.BytesIO(self.data)
        toUnzip = zipfile.ZipFile(pretendObject)
        return toUnzip.extractall()'''

    def decompress(self):
        # Create an in-memory bytes buffer to hold the decompressed data
        file_buffer = io.BytesIO()

        # Create a ZipFile object with the compressed data
        with zipfile.ZipFile(io.BytesIO(self.data), mode='r') as zip_file:
            # Extract the file contents to the in-memory buffer
            file_buffer.write(zip_file.read('data'))

        # Set the file buffer's current position to the beginning
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