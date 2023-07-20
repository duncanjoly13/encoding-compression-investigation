# import modules
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# set path to results file
data_df = pd.read_csv("completed_results\\2023-07-04--00-09_LARGE-32_results-PROCESSED.csv")
# set to column name
metric = 'total time EXCL. read + write times (ms)'
# set to filesize for graphing
desired_filesize = 10239975
# set to algorithm names
enc_alg = 'NaCl'
comp_alg = 'gzip'
second_enc_alg = 'Fernet'
second_comp_alg = 'bzip'

# used when chart contains information within a specific filesize
def specific_size_chart(data_df):
    # used to filter out comp/enc only cases
    data_df = data_df[data_df['encryption algorithm'] != 'NoEnc']
    data_df = data_df[data_df['compression algorithm'] != 'NoZip']

    data_df['operation id'] = data_df['order'] + '-' + data_df['compression algorithm'] + '-' + data_df['encryption algorithm']
    data_df['approach'] = ''

    comp_first_sub_df = data_df[data_df['order'] == 'Compression First']
    comp_first_sub_df['operation id'] = comp_first_sub_df['compression algorithm'] + '-then-' + comp_first_sub_df['encryption algorithm']
    comp_first_sub_df['approach'] = 'Compression First'

    enc_first_sub_df = data_df[data_df['order'] == 'Encryption First']
    enc_first_sub_df['operation id'] = enc_first_sub_df['encryption algorithm'] + '-then-' +  enc_first_sub_df['compression algorithm']
    enc_first_sub_df['approach'] = 'Encryption First'

    # only needed if examining comp/enc only cases
    ###############
    '''no_enc_sub_df = data_df[data_df['encryption algorithm'] == 'NoEnc']
    no_enc_sub_df['approach'] = 'Compression Only'

    no_comp_sub_df = data_df[data_df['compression algorithm'] == 'NoZip']
    no_comp_sub_df['approach'] = 'Encryption Only'''
    ###############

    # add no_enc_sub_df, no_comp_sub_df if they are assigned
    data_df = pd.concat([comp_first_sub_df,enc_first_sub_df])

    each_unique_filesize = data_df['source file size (B)'].unique()
    each_unique_filesize.sort()

    for filesize in each_unique_filesize:
        print('file: ' + str(filesize) + 'B...')
        
        correct_filesize_df = data_df[data_df['source file size (B)'] == filesize]

        # graphing code for specific algorithms and their combinations, includes none cases
        '''correct_algs_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == comp_alg) & (correct_filesize_df['encryption algorithm'] == enc_alg)]
        no_enc_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == comp_alg) & (correct_filesize_df['encryption algorithm'] == 'NoEnc') & (correct_filesize_df['order'] == 'Compression First')]
        no_comp_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == 'NoZip') & (correct_filesize_df['encryption algorithm'] == enc_alg) & (correct_filesize_df['order'] == 'Compression First')]
        sub_df = pd.concat([correct_algs_df, no_enc_df, no_comp_df])'''

        # graphing code for two combinations and their inverses, includes none cases
        '''first_algs_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == comp_alg) & (correct_filesize_df['encryption algorithm'] == enc_alg)]
        second_algs_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == second_comp_alg) & (correct_filesize_df['encryption algorithm'] == second_enc_alg)]
        no_enc_first_comp_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == comp_alg) & (correct_filesize_df['encryption algorithm'] == 'NoEnc') & (correct_filesize_df['order'] == 'Compression First')]
        no_comp_first_enc_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == 'NoZip') & (correct_filesize_df['encryption algorithm'] == enc_alg) & (correct_filesize_df['order'] == 'Compression First')]
        no_enc_second_comp_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == second_comp_alg) & (correct_filesize_df['encryption algorithm'] == 'NoEnc') & (correct_filesize_df['order'] == 'Compression First')]
        no_comp_second_enc_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == 'NoZip') & (correct_filesize_df['encryption algorithm'] == second_enc_alg) & (correct_filesize_df['order'] == 'Compression First')]
        sub_df = pd.concat([first_algs_df, second_algs_df, no_enc_first_comp_df, no_comp_first_enc_df, no_enc_second_comp_df, no_comp_second_enc_df])

        print(sub_df['encryption algorithm'].unique())'''

        # for averages and their baselines (comp first, enc first, comp only, enc only), requires no_enc_sub_df and no_comp_sub_df to be active above
        '''sub_df = correct_filesize_df'''

        # for two combinations and their inverses - requires second_comp_alg and second_enc_alg to be assigned
        '''first_algs_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == comp_alg) & (correct_filesize_df['encryption algorithm'] == enc_alg)]
        second_algs_df = correct_filesize_df[(correct_filesize_df['compression algorithm'] == second_comp_alg) & (correct_filesize_df['encryption algorithm'] == second_enc_alg)]
        sub_df = pd.concat([first_algs_df, second_algs_df])'''

        # needed if none of the above are used
        sub_df = correct_filesize_df
        # used for bar charts in combination with above
        mean_df = pd.DataFrame()
        for id in sub_df['operation id'].unique():
            middle_df = sub_df[sub_df['operation id'] == id]
            row = pd.DataFrame()
            row['operation id'] = [id]
            row['filesize'] = [filesize]
            row['encryption time (ms)'] = [middle_df['encryption time (ms)'].mean()]
            row['compression time (ms)'] = [middle_df['compression time (ms)'].mean()]
            row['decompression time (ms)'] = [middle_df['decompression time (ms)'].mean()]
            row['decryption time (ms)'] = [middle_df['decryption time (ms)'].mean()]
            mean_df = pd.concat([mean_df, row])

        # edit categories to change order of items on x-axis, apply to mean_df for bar charts
        mean_df['operation id'] = pd.Categorical(mean_df['operation id'], categories = ['bzip-then-NoEnc', 'NoZip-then-Fernet','bzip-then-Fernet', 'Fernet-then-bzip', 'gzip-then-NoEnc', 'NoZip-then-NaCl', 'gzip-then-NaCl', 'NaCl-then-gzip'], ordered = True)
        mean_df = mean_df.sort_values(by = ['operation id'])

        '''print('compression first mean (ms)', sub_df[sub_df['order'] == 'Compression First'][metric].mean())
        print('encryption first mean (ms)', sub_df[sub_df['order'] == 'Encryption First'][metric].mean())'''

        if filesize == desired_filesize:
            # by = ['order'] for most, by = ['approach'] for high-level baselines
            #f or boxplot:
            print('graphing:', str(filesize))
            boxplot = sub_df.boxplot(column = [metric], by = ['operation id'], rot = 45, showmeans = True, showfliers = False)
            # for stacked bar chart:
            '''barchart = mean_df.plot(x = 'operation id', y = ['encryption time (ms)', 'compression time (ms)', 'decompression time (ms)', 'decryption time (ms)'], stacked = True, rot = 45)'''
            plt.xlabel('Algorithmic Combination')
            plt.ylabel('Operation Time (ms)')
            plt.suptitle('')
            # edit title
            plt.title('Encryption and Compression Combinations in a 10MB File')
            plt.savefig('RENAME_THIS.png', dpi = 300, bbox_inches = 'tight', pad_inches = .25)
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

# used to chart with filesize as x-axis
def all_sizes_chart(data_df):
    # used to filter out comp/enc only cases
    data_df = data_df[data_df['encryption algorithm'] != 'NoEnc']
    data_df = data_df[data_df['compression algorithm'] != 'NoZip']

    data_df['operation id'] = data_df['order'] + '-' + data_df['compression algorithm'] + '-' + data_df['encryption algorithm']
    data_df['approach'] = ''

    comp_first_sub_df = data_df[data_df['order'] == 'Compression First']
    comp_first_sub_df['operation id'] = comp_first_sub_df['compression algorithm'] + '-then-' + comp_first_sub_df['encryption algorithm']
    comp_first_sub_df['approach'] = 'Compression First'

    enc_first_sub_df = data_df[data_df['order'] == 'Encryption First']
    enc_first_sub_df['operation id'] = enc_first_sub_df['encryption algorithm'] + '-then-' +  enc_first_sub_df['compression algorithm']
    enc_first_sub_df['approach'] = 'Encryption First'
    
    # only needed if examining comp/enc only cases
    ###############
    '''no_enc_sub_df = data_df[data_df['encryption algorithm'] == 'NoEnc']
    no_enc_sub_df['approach'] = 'Compression Only'

    no_comp_sub_df = data_df[data_df['compression algorithm'] == 'NoZip']
    no_comp_sub_df['approach'] = 'Encryption Only'''
    ###############

    # add no_enc_sub_df, no_comp_sub_df if they are assigned
    data_df = pd.concat([comp_first_sub_df,enc_first_sub_df])

    each_unique_filesize = data_df['source file size (B)'].unique()
    each_unique_filesize.sort()

    first_algs_df = data_df[(data_df['compression algorithm'] == comp_alg) & (data_df['encryption algorithm'] == enc_alg)]
    second_algs_df = data_df[(data_df['compression algorithm'] == second_comp_alg) & (data_df['encryption algorithm'] == second_enc_alg)]
    no_enc_first_comp_df = data_df[(data_df['compression algorithm'] == comp_alg) & (data_df['encryption algorithm'] == 'NoEnc') & (data_df['order'] == 'Compression First')]
    no_comp_first_enc_df = data_df[(data_df['compression algorithm'] == 'NoZip') & (data_df['encryption algorithm'] == enc_alg) & (data_df['order'] == 'Compression First')]
    '''no_enc_second_comp_df = data_df[(data_df['compression algorithm'] == second_comp_alg) & (data_df['encryption algorithm'] == 'NoEnc') & (data_df['order'] == 'Compression First')]
    no_comp_second_enc_df = data_df[(data_df['compression algorithm'] == 'NoZip') & (data_df['encryption algorithm'] == second_enc_alg) & (data_df['order'] == 'Compression First')]'''
    correct_algs_df = pd.concat([first_algs_df, second_algs_df, no_enc_first_comp_df, no_comp_first_enc_df])

    wanted_sizes = [1206, 1086844, 10239975, 101128023]
    first_correct_size_df = correct_algs_df[correct_algs_df['source file size (B)'] == wanted_sizes[0]]
    second_correct_size_df = correct_algs_df[correct_algs_df['source file size (B)'] == wanted_sizes[1]]
    third_correct_size_df = correct_algs_df[correct_algs_df['source file size (B)'] == wanted_sizes[2]]
    fourth_correct_size_df = correct_algs_df[correct_algs_df['source file size (B)'] == wanted_sizes[3]]
    sub_df = pd.concat([first_correct_size_df, second_correct_size_df, third_correct_size_df, fourth_correct_size_df])

    mean_df = pd.DataFrame()
    for id in sub_df['operation id'].unique():
        middle_df = sub_df[sub_df['operation id'] == id]
        print(middle_df['source file size (B)'])
        row = pd.DataFrame()
        row['operation id'] = [id]
        row['encryption time (ms)'] = [middle_df['encryption time (ms)'].mean()]
        row['compression time (ms)'] = [middle_df['compression time (ms)'].mean()]
        row['decompression time (ms)'] = [middle_df['decompression time (ms)'].mean()]
        row['decryption time (ms)'] = [middle_df['decryption time (ms)'].mean()]
        mean_df = pd.concat([mean_df, row])

    print(mean_df)
    
    barchart = mean_df.plot.bar(y = ['encryption time (ms)', 'compression time (ms)', 'decompression time (ms)', 'decryption time (ms)'], stacked = True, rot = 45)
    plt.xlabel('Algorithmic Combination')
    plt.ylabel('Operation Time (ms)')
    plt.suptitle('')
    # edit title
    plt.title('TEST in a 10MB File')
    plt.savefig('RENAME_THIS.png', dpi = 300, bbox_inches = 'tight', pad_inches = .25)
    plt.close()

if __name__ == '__main__':
    specific_size_chart(data_df)
    # all_sizes_chart(data_df)