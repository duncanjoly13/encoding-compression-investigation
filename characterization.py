import numpy as np

def run(filename, keySize = 10):
    demographic = {}
    counts = []

    with open(filename, 'rb') as file:
        data = file.read()
        file.close()

    counter = 0
    while counter < len(data) - keySize:
        currentPhrase = data[counter:(counter + keySize)]
        if currentPhrase in demographic.keys():
            demographic[currentPhrase] += 1
            counter += keySize
        else:
            demographic[currentPhrase] = 1
            counter += keySize

    for pattern in demographic.keys():
        counts.append(demographic[pattern])
    
    output = {}
    output['mean'] = np.mean(counts)
    output['std'] = np.std(counts)
    output['max'] = np.max(counts)
    output['total'] = len(demographic.keys())

    return output

if __name__ == '__main__':
    run('enwik_1mb.txt')