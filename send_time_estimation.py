def get_time(filesize, network_speed):
    return ((filesize * 8) / network_speed) / 1000

def edit(filename):
    newData = ''
    try:
        with open(filename) as file:
            newData += file.readline()[:-1] + ',estimated network time @ 1Mbps (s),estimated network time @ 5Mbps (s),estimated network time @ 10Mbps (s)\n'
            data = file.readlines()
            for line in data:
                speed = int(line.split(',')[7])
                newData += line[:-1] + ',' + str(get_time(speed, 1)) + ',' + str(get_time(speed, 5)) + ',' + str(get_time(speed, 10)) + '\n'
            file.close()

        with open(filename, 'w') as newFile:
            newFile.write(newData[:-1])
            newFile.close()
    except FileNotFoundError:
        print("File '%s' does not exist" %filename)