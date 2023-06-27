import glob

def get_time(filesize, network_speed):
    return ((filesize * 8) / network_speed) / 1000

def edit(filename):
    newData = ''
    try:
        with open(filename) as file:
            rawLines = file.readlines()
            newData += rawLines[0][:-1] + ',total time EXCL. read + write times (ms),total time INCL. read and write times,compression ratio,estimated network time @ 1Mbps (ms),estimated network time @ 5Mbps (ms),estimated network time @ 10Mbps (ms)\n'
            rawData = rawLines[1:]
            for line in rawData:
                data = line.split(',')
                originalSize = float(data[1])
                encryptTime = float(data[5])
                compressTime = float(data[6])
                compressedSize = float(data[7])
                decompressTime = float(data[8])
                decryptTime = float(data[9])
                intermediateWriteTime = float(data[10])
                intermediateReadTime = float(data[11])
                finalWriteTime = float(data[12])

                memoryOperationsTotalTime = encryptTime + compressTime + decompressTime + decryptTime
                totalTime = memoryOperationsTotalTime + intermediateWriteTime + intermediateReadTime + finalWriteTime

                newData += ((line[:-1] + ',') + (str("{:.4f}".format(memoryOperationsTotalTime)) + ',') + (str("{:.4f}".format(totalTime)) + ',') + (str("{:.4f}".format((compressedSize / originalSize))) + ',') + (str("{:.4f}".format(get_time(compressedSize, 1))) + ',') + (str("{:.4f}".format(get_time(compressedSize, 5))) + ',') + str("{:.4f}".format(get_time(compressedSize, 10))) + '\n')
            file.close()

        with open(filename[:-4] + '-PROCESSED.csv', 'w') as newFile:
            newFile.write(newData[:-1])
            newFile.close()
    except FileNotFoundError:
        print("File '%s' does not exist" %filename)

if __name__ == '__main__':
    files = glob.glob('*results.csv')
    edit(files[0])