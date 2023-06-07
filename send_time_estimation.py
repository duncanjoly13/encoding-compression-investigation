def get_time(filesize, network_speed):
    return ((filesize * 8) / network_speed) / 1000

def edit(filename):
    newData = ''
    try:
        with open(filename) as file:
            rawLines = file.readlines()
            newData += rawLines[0]
            newData += rawLines[1][:-1] + ',compression ratio,estimated network time @ 1Mbps (s),estimated network time @ 5Mbps (s),estimated network time @ 10Mbps (s)\n'
            rawData = rawLines[2:]
            for line in rawData:
                originalSize = int(line.split(',')[1])
                compressedSize = int(line.split(',')[7])
                newData += line[:-1] + ',' + str("{:.3f}".format(originalSize / compressedSize)) + ',' + str("{:.3f}".format(get_time(compressedSize, 1))) + ',' + str("{:.3f}".format(get_time(compressedSize, 5))) + ',' + str("{:.3f}".format(get_time(compressedSize, 10))) + '\n'
            file.close()

        with open(filename[:-4] + '-PROCESSED.csv', 'w') as newFile:
            newFile.write(newData[:-1])
            newFile.close()
    except FileNotFoundError:
        print("File '%s' does not exist" %filename)

if __name__ == '__main__':
    edit('2023-06-07--13-20-results.csv')