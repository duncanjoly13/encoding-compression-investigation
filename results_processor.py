import glob, full_test
import pandas as pd

def get_data(df, file, encAlg, compAlg, order):
    fileMask = df['source file'] == file
    correctFile = df[fileMask]
    encMask = correctFile['encryption algorithm'] == encAlg
    correctEnc = correctFile[encMask]
    compMask = correctEnc['compression algorithm'] == compAlg
    correctComp = correctEnc[compMask]
    orderMask = correctComp['order'] == order
    allCorrect = correctComp[orderMask]
    return allCorrect

def get_mean(df, file, encAlg, compAlg, order, field):
    data = get_data(df, file, encAlg, compAlg, order)
    return data[field].mean()

def get_std(df, file, encAlg, compAlg, order, field):
    data = get_data(df, file, encAlg, compAlg, order)
    return data[field].std()

def get_max(df, file, encAlg, compAlg, order, field):
    data = get_data(df, file, encAlg, compAlg, order)
    return data[field].max()

def get_min(df, file, encAlg, compAlg, order, field):
    data = get_data(df, file, encAlg, compAlg, order)
    return data[field].min()

def get_unique(df, column):
    return df[column].unique()

def create_csv(df, name):
    stats = {'mean':get_mean, 'std':get_std, 'max':get_max, 'min':get_min}
    fields = df.columns.values.tolist()
    toRemove = ['source file', 'encryption algorithm', 'compression algorithm', 'order', 'repetition #']
    for notWanted in toRemove:
        fields.pop(fields.index(notWanted))
    print(fields)
    for stat in stats.keys():
        sheet = full_test.Sheet(str(stat.upper() + '-' + name))
        for name in list(df['source file'].unique()):
            for encAlg in list(df['encryption algorithm'].unique()):
                for compAlg in list(df['compression algorithm'].unique()):
                    for order in list(df['order'].unique()):
                        for field in fields:
                            method = stats[stat]
                            sheet.addData(method(df, name, encAlg, compAlg, order, field))

if __name__ == '__main__':
    files = glob.glob('*results-PROCESSED.csv')
    for file in files:
        data = pd.read_csv(file)
        print('mean:', get_mean(data, 'single-packet-tele-payload-bytes.data', 'Fernet', 'bzip', 'Compression First', 'compression ratio'))
        print('std:', get_std(data, 'single-packet-tele-payload-bytes.data', 'Fernet', 'bzip', 'Compression First', 'compression ratio'))
        print('max:', get_max(data, 'single-packet-tele-payload-bytes.data', 'Fernet', 'bzip', 'Compression First', 'compression ratio'))
        print('min:', get_min(data, 'single-packet-tele-payload-bytes.data', 'Fernet', 'bzip', 'Compression First', 'compression ratio'))
        print('mean:', get_mean(data, 'single-packet-tele-payload-bytes.data', 'Fernet', 'bzip', 'Encryption First', 'compression ratio'))
        print('std:', get_std(data, 'single-packet-tele-payload-bytes.data', 'Fernet', 'bzip', 'Encryption First', 'compression ratio'))
        print('max:', get_max(data, 'single-packet-tele-payload-bytes.data', 'Fernet', 'bzip', 'Encryption First', 'compression ratio'))
        print('min:', get_min(data, 'single-packet-tele-payload-bytes.data', 'Fernet', 'bzip', 'Encryption First', 'compression ratio'))

        create_csv(data, file)