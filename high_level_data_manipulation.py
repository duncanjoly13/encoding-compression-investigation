import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

data_df = pd.read_csv("completed_results\\2023-07-03--11-40_SMALL_results-PROCESSED.csv")

'''data_df = data_df[data_df['encryption algorithm'] != 'NoEnc']
data_df = data_df[data_df['compression algorithm'] != 'NoZip']'''

data_df['operation id'] = data_df['order'] + data_df['compression algorithm'] + data_df['encryption algorithm']

print(len(data_df['operation id'].unique()))

each_unique_filesize = data_df['source file size (B)'].unique()
each_unique_filesize.sort()

for filesize in each_unique_filesize:
    sub_df = data_df[data_df['source file size (B)'] == filesize]
    print(sub_df[sub_df['order'] == 'Compression First']['total time EXCL. read + write times (ms)'].mean())
    print(sub_df[sub_df['order'] == 'Encryption First']['total time EXCL. read + write times (ms)'].mean())
    print('comp only', str(sub_df[(sub_df['compression algorithm'] != 'NoZip') & (sub_df['encryption algorithm'] == 'NoEnc')]['total time EXCL. read + write times (ms)'].mean()))
    print('enc only', str(sub_df[(sub_df['compression algorithm'] == 'NoZip') & (sub_df['encryption algorithm'] != 'NoEnc')]['total time EXCL. read + write times (ms)'].mean()))
    if filesize == 1086844:
        boxplot = sub_df.boxplot(column = ['total time EXCL. read + write times (ms)'], by = ['operation id'], rot=90, showmeans = True)
        plt.title(filesize)
        plt.show()
        plt.close()
    test_group_df = pd.DataFrame()
    for id in data_df['operation id'].unique():
        second_df = sub_df[sub_df['operation id'] == id]
        # print('{} mean {} +- {} samples {}'.format(id, second_df['total time EXCL. read + write times (ms)'].mean(), second_df['total time EXCL. read + write times (ms)'].std(), len(second_df)))
        row = pd.DataFrame()
        row['filesize'] = [filesize]
        row['test id'] = [id]
        row['average'] = [second_df['total time EXCL. read + write times (ms)'].mean()]
        row['std'] = [second_df['total time EXCL. read + write times (ms)'].std()]
        row['samples'] = [len(second_df)]
        test_group_df = pd.concat([test_group_df, row])
    
    test_group_df.to_csv('./filesize-{}.csv'.format(filesize), index = False)
    best = test_group_df[test_group_df['average'] == test_group_df['average'].min()]
    print(best)