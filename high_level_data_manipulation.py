import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

data_df = pd.read_csv("completed_results\\2023-07-04--00-09_LARGE-32_results-PROCESSED.csv")
metric = 'total time EXCL. read + write times (ms)'
desired_filesize = 10239975
enc_alg = 'NaCl'
comp_alg = 'gzip'

'''data_df = data_df[data_df['encryption algorithm'] != 'NoEnc']
data_df = data_df[data_df['compression algorithm'] != 'NoZip']'''

data_df['operation id'] = data_df['order'] + '-' + data_df['compression algorithm'] + '-' + data_df['encryption algorithm']
data_df['approach'] = ''

comp_first_sub_df = data_df[data_df['order'] == 'Compression First']
comp_first_sub_df['operation id'] = comp_first_sub_df['compression algorithm'] + '-then-' + comp_first_sub_df['encryption algorithm']
comp_first_sub_df['approach'] = 'Compression First'

enc_first_sub_df = data_df[data_df['order'] == 'Encryption First']
enc_first_sub_df['operation id'] = enc_first_sub_df['encryption algorithm'] + '-then-' +  enc_first_sub_df['compression algorithm']
enc_first_sub_df['approach'] = 'Encryption First'

no_enc_sub_df = data_df[data_df['encryption algorithm'] == 'NoEnc']
no_enc_sub_df['approach'] = 'Compression Only'

no_comp_sub_df = data_df[data_df['compression algorithm'] == 'NoZip']
no_comp_sub_df['approach'] = 'Encryption Only'

data_df = pd.concat([comp_first_sub_df,enc_first_sub_df, no_enc_sub_df, no_comp_sub_df])

each_unique_filesize = data_df['source file size (B)'].unique()
each_unique_filesize.sort()

for filesize in each_unique_filesize:
    print('file: ' + str(filesize) + 'B...')
    
    correct_filesize_df = data_df[data_df['source file size (B)'] == filesize]

    # FOR SPECIFIC ALGS AND THEIR BASELINES
    '''correct_algs_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == comp_alg) & (correct_filesize_df['encryption algorithm'] == enc_alg)]
    no_enc_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == comp_alg) & (correct_filesize_df['encryption algorithm'] == 'NoEnc') & (correct_filesize_df['order'] == 'Compression First')]
    no_comp_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == 'NoZip') & (correct_filesize_df['encryption algorithm'] == enc_alg) & (correct_filesize_df['order'] == 'Compression First')]
    sub_df = pd.concat([correct_algs_df, no_enc_df, no_comp_df])'''

    # FOR AVERAGES AND BASELINES (COMP FIRST, ENC FIRST, COMP ONLY, ENC ONLY)
    sub_df = correct_filesize_df
        
    print('compression first mean (ms)', sub_df[sub_df['order'] == 'Compression First'][metric].mean())
    print('encryption first mean (ms)', sub_df[sub_df['order'] == 'Encryption First'][metric].mean())

    if filesize == desired_filesize:
        # by = ['order'] for most, by = ['approach'] for high-level baselines
        boxplot = sub_df.boxplot(column = [metric], by = ['approach'], rot = 45, showmeans = True, showfliers = False)
        plt.xlabel('Algorithmic Combination')
        plt.ylabel('Operation Time (ms)')
        plt.suptitle('')
        plt.title('Average Operation Times in a 10MB File'.format(comp_alg, enc_alg))
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