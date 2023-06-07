def get_time(filesize, network_speed):
    return ((filesize * 8) / network_speed) / 1000

def edit(filename):
    newData = ''
    try:
        with open(filename) as file:
            newData += file.readline()[:-1] + ',compression ratio,estimated network time @ 1Mbps (s),estimated network time @ 5Mbps (s),estimated network time @ 10Mbps (s)\n'
            data = file.readlines()
            for line in data:
                originalSize = int(line.split(',')[1])
                compressedSize = int(line.split(',')[7])
                newData += line[:-1] + ',' + str("{:.3f}".format(originalSize / compressedSize)) + ',' + str(get_time(compressedSize, 1)) + ',' + str(get_time(compressedSize, 5)) + ',' + str(get_time(compressedSize, 10)) + '\n'
            file.close()

        with open(filename[:-4] + '-PROCESSED.csv', 'w') as newFile:
            newFile.write(newData[:-1])
            newFile.close()
    except FileNotFoundError:
        print("File '%s' does not exist" %filename)

if __name__ == '__main__':
    edit('2023-06-06--21-27-results.csv')