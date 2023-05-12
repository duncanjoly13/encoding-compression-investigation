#TODO add new columns to csv

import pandas
# import full_test

def compute(filesize, network_speed):
    return (filesize * 8) / network_speed

'''test = full_test.Test('2000-word-text.txt')
df = pandas.read_csv(test.run())'''

'''df = pandas.read_csv('2023-05-12--11-13-results.csv')
saved_column = df['encrypted and compressed file size (b)']
'''
pandas.concat([pandas.read_csv('2023-05-12--11-13-results.csv'), pandas.DataFrame('estimated network time (10Mbps)', 'estimated network time (5Mbps)', 'estimated network time (1Mbps)')]).to_csv('output.csv', header=True, index=False)
