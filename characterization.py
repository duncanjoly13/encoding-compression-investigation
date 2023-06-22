import numpy as np

keySize = 8
filename = 'enwik8_1mb.txt'

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

print('mean:', str(np.mean(counts)))
print('std:', str(np.std(counts)))
print('max:', str(np.max(counts)))
print('total keys:', str(len(demographic.keys())))