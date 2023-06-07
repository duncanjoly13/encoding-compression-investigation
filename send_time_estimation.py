def get_time(filesize, network_speed):
    return ((filesize * 8) / network_speed) / 1000

def edit(filename):
    newData = ''
    try:
        with open(filename) as file:
            rawLines = file.readlines()
            newData += rawLines[0][:-1] + ',total time EXCL. read + write times (ms),total time INCL. read and write times,compression ratio,estimated network time @ 1Mbps (s),estimated network time @ 5Mbps (s),estimated network time @ 10Mbps (s)\n'
            rawData = rawLines[1:]
            for line in rawData:
                originalSize = float(line.split(',')[1])
                encryptTime = float(line.split(',')[5])
                compressTime = float(line.split(',')[6])
                compressedSize = float(line.split(',')[7])
                decompressTime = float(line.split(',')[8])
                decryptTime = float(line.split(',')[9])
                intermediateWriteTime = float(line.split(',')[10])
                intermediateReadTime = float(line.split(',')[11])
                finalWriteTime = float(line.split(',')[12])

                memoryOperationsTotalTime = encryptTime + compressTime + decompressTime + decryptTime
                totalTime = memoryOperationsTotalTime + intermediateWriteTime + intermediateReadTime + finalWriteTime

                newData += line[:-1] + str("{:.3f}".format(memoryOperationsTotalTime)) + ',' + str("{:.3f}".format(totalTime)) + ',' + str("{:.3f}".format((compressedSize / originalSize))) + ',' + str("{:.3f}".format(get_time(compressedSize, 1))) + ',' + str("{:.3f}".format(get_time(compressedSize, 5))) + ',' + str("{:.3f}".format(get_time(compressedSize, 10))) + '\n'
            file.close()

        with open(filename[:-4] + '-PROCESSED.csv', 'w') as newFile:
            newFile.write(newData[:-1])
            newFile.close()
    except FileNotFoundError:
        print("File '%s' does not exist" %filename)

if __name__ == '__main__':
    edit('2023-06-07--13-35-results.csv')