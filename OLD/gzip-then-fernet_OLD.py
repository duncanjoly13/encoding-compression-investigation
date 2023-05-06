# Encryption method based on code by Jason Carpenter

#TODO implement switch between file saving and simple operations on memory objects
#TODO file exists / does not exist error handling - maybe wait for v2 (for loops)

# Import modules
import gzip, os, hashlib, shutil, time
from cryptography.fernet import Fernet

# Initialize variables
order = 'compress then encrypt'
filename = '2000-word-text.txt'
filesize = os.path.getsize(filename)

# Compression
compressionAlg = 'gzip'
beforeCompressionTime = time.time()
with open(filename, 'rb') as f_in:
    with gzip.open(str(filename + '.gz'), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

# Encryption
encryptionAlg = 'Fernet (key = 32B)'
encryptionStartTime = time.time()
dataFilePath = str(filename + '.gz')

fullyQualifiedName = dataFilePath.split('/')[-1]
justFileName = os.path.basename(dataFilePath).split('.')[0]
fileExtension = dataFilePath.split('.')[-1]

dataFileDataFP = open(dataFilePath, 'rb')
rawFileData = dataFileDataFP.read(os.path.getsize(dataFilePath))
dataFileDataFP.close()

key = Fernet.generate_key()
f = Fernet(key)
encMessage = f.encrypt(rawFileData)

fileHash = hashlib.sha1(encMessage)
fileHashString = fileHash.hexdigest()

'''
encDataFP = open('./{}-data'.format(fileHashString), 'wb')
encDataFP.write(encMessage)
encDataFP.flush()
encDataFP.close()
'''
'''
keyFP = open('{}-key'.format(fileHashString), 'wb')
keyFP.write(key)
keyFP.flush()
keyFP.close()
'''
encryptionEndTime = time.time()

# Decryption
'''
decryptFP = open(dataFilePath, 'rb')
decryptData = decryptFP.read()
decryptFP.close()
'''
decryptKey = Fernet(key)
decryptedData = decryptKey.decrypt(encMessage)
decryptEndTime = time.time()

# Decompression
decompressedData = gzip.decompress(decryptedData)
decompressEndTime = time.time()

# Compute durations
compressionTime = encryptionStartTime - beforeCompressionTime
encryptionTime = encryptionEndTime - encryptionStartTime
decryptionTime = decryptEndTime - encryptionEndTime
decompresionTime = decompressEndTime - decryptEndTime

# Generate csv
csvHeader = 'source file, source file size (b), encryption algorithm, compression algorithm, order, encryption time (s), compression time (s), encrypted file size (b), compressed file size (b), decompression time (s), decryption time (s)\n'

ENCRYPTEDFILESIZE = COMPRESSEDFILESIZE = 'N/A'

with open('results.csv', 'w') as results:
    results.write(csvHeader)
    results.write((filename + ',') + (str(filesize) + ',') +(encryptionAlg + ',') + (compressionAlg + ',') + (order + ',') + (str(encryptionTime) + ',') + (str(compressionTime) + ',') + (str(ENCRYPTEDFILESIZE) + ',') + (str(COMPRESSEDFILESIZE) + ',') + (str(decompresionTime) + ',') + (str(decryptionTime) + '\n'))
    results.close()