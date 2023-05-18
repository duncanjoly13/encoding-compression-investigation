def get_time(filesize, network_speed):
    return ((filesize * 8) / network_speed) / 1000

def edit(filename):
    newData = ''
    with open(filename) as file:
        newData += file.readline()[:-1] + ',estimated network time @ 1Mbps (s),estimated network time @ 5Mbps (s),estimated network time @ 10Mbps (s)\n'
        data = file.readlines()
        for line in data:
            speed = int(line.split(',')[7])
            newData += line[:-1] + ',' + str(get_time(speed, 1)) + ',' + str(get_time(speed, 5)) + ',' + str(get_time(speed, 10)) + '\n'
        file.close()
    print(newData)

    with open(filename, 'w') as newFile:
        newFile.write(newData[:-1])
        newFile.close()

edit('2023-05-17--22-45-results.csv')