import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

data_df = pd.read_csv("completed_results\\2023-07-04--00-09_LARGE-32_results-PROCESSED.csv")
metric = 'total time EXCL. read + write times (ms)'
desired_filesize = 10239975
enc_alg = 'NaCl'
comp_alg = 'gzip'

data_df = data_df[data_df['encryption algorithm'] != 'NoEnc']
data_df = data_df[data_df['compression algorithm'] != 'NoZip']

data_df['operation id'] = data_df['order'] + '-' + data_df['compression algorithm'] + '-' + data_df['encryption algorithm']

comp_first_sub_df = data_df[data_df['order'] == 'Compression First']
comp_first_sub_df['operation id'] = comp_first_sub_df['compression algorithm'] + '-then-' + comp_first_sub_df['encryption algorithm']

enc_first_sub_df = data_df[data_df['order'] == 'Encryption First']
enc_first_sub_df['operation id'] = enc_first_sub_df['encryption algorithm'] + '-then-' +  enc_first_sub_df['compression algorithm']

data_df = pd.concat([comp_first_sub_df,enc_first_sub_df])

each_unique_filesize = data_df['source file size (B)'].unique()
each_unique_filesize.sort()

for filesize in each_unique_filesize:
    print('file: ' + str(filesize) + 'B...')
    first_sub_df = data_df[data_df['source file size (B)'] == filesize]
    sub_df = first_sub_df[(first_sub_df['compression algorithm'] == comp_alg) & (first_sub_df['encryption algorithm'] == enc_alg)]
    # sub_df = first_sub_df
    print('compression first mean (ms)', sub_df[sub_df['order'] == 'Compression First'][metric].mean())
    print('encryption first mean (ms)', sub_df[sub_df['order'] == 'Encryption First'][metric].mean())

    '''print('comp only', str(sub_df[(sub_df['compression algorithm'] != 'NoZip') & (sub_df['encryption algorithm'] == 'NoEnc')][metric].mean()))
    print('enc only', str(sub_df[(sub_df['compression algorithm'] == 'NoZip') & (sub_df['encryption algorithm'] != 'NoEnc')][metric].mean()))'''

    if filesize == desired_filesize:
        boxplot = sub_df.boxplot(column = [metric], by = ['operation id'], rot=0, showmeans = True, showfliers = False)
        plt.xlabel('Algorithmic Combination')
        plt.ylabel('Operation Time (ms)')
        plt.suptitle('')
        plt.title('{} and {} in a 10MB File'.format(comp_alg, enc_alg))
        plt.savefig('RENAME_THIS.png', dpi=300, bbox_inches='tight', pad_inches=.25)
        plt.close()
    test_group_df = pd.DataFrame()
    for id in data_df['operation id'].unique():
        second_df = sub_df[sub_df['operation id'] == id]
        row = pd.DataFrame()
        row['filesize'] = [filesize]
        row['test id'] = [id]
        row['average'] = [second_df[metric].mean()]
        row['std'] = [second_df[metric].std()]
        row['samples'] = [len(second_df)]
        test_group_df = pd.concat([test_group_df, row])

    comp_first = sub_df[(sub_df['compression algorithm'] == comp_alg) & (sub_df['encryption algorithm'] == enc_alg) & (sub_df['order'] == 'Compression First')]
    enc_first = sub_df[(sub_df['compression algorithm'] == comp_alg) & (sub_df['encryption algorithm'] == enc_alg) & (sub_df['order'] == 'Encryption First')]

    test_result = ttest_ind(comp_first[metric], enc_first[metric], equal_var = False)
    print(test_result)
    print(test_result.confidence_interval())
    
    # test_group_df.to_csv('./filesize-{}.csv'.format(filesize), index = False)
    best = test_group_df[test_group_df['average'] == test_group_df['average'].min()]
    print(best)
    print()