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

def create_csv(df, filename):
    stats = {'mean':get_mean, 'std':get_std, 'max':get_max, 'min':get_min}
    fields = trimmedFields = df.columns.values.tolist()
    values = {field: 'not yet initialized' for field in fields}
    toRemove = ['repetition #', 'initial characterization - mean', 'initial characterization - std', 'initial characterization - max', 'initial characterization - total keys', 'after encryption characterization - mean', 'after encryption characterization - std', 'after encryption characterization - max', 'after encryption characterization - total keys']
    for stat in stats.keys():
        method = stats[stat]
        sheet = full_test.Sheet(str(stat.upper() + '-' + filename), ','.join(fields) + '\n')
        for name in list(df['source file'].unique()):
            for encAlg in list(df['encryption algorithm'].unique()):
                for compAlg in list(df['compression algorithm'].unique()):
                    for order in list(df['order'].unique()):
                        values = values.fromkeys(values, 'BLANK')
                        headerFields = {'source file':name, 'encryption algorithm':encAlg, 'compression algorithm':compAlg, 'order':order}
                        for field in trimmedFields:
                            if field in headerFields.keys():
                                values[field] = headerFields[field]
                            elif field in toRemove:
                                values[field] = 'REMOVED'
                            else:
                                datapoint = method(df, name, encAlg, compAlg, order, field)
                                values[field] = datapoint
                        i = 0
                        line = ""
                        while i < len(values.keys()):
                            for value in values.keys():
                                if i == len(values.keys()) - 1:
                                    line += (str(values[value]) + '\n')
                                    i += 1
                                else:
                                    line += (str(values[value]) + ',')
                                    i += 1
                        sheet.addData(line)

if __name__ == '__main__':
    files = glob.glob('*results-PROCESSED.csv')
    for file in files:
        data = pd.read_csv(file)
        print('mean:', get_mean(data, 'single-packet-tele-payload-bytes.data', 'NoEnc', 'NoZip', 'Compression First', 'compression ratio'))
        print('std:', get_std(data, 'single-packet-tele-payload-bytes.data', 'NoEnc', 'NoZip', 'Compression First', 'compression ratio'))
        print('max:', get_max(data, 'single-packet-tele-payload-bytes.data', 'NoEnc', 'NoZip', 'Compression First', 'compression ratio'))
        print('min:', get_min(data, 'single-packet-tele-payload-bytes.data', 'NoEnc', 'NoZip', 'Compression First', 'compression ratio'))
        print('mean:', get_mean(data, 'single-packet-tele-payload-bytes.data', 'NoEnc', 'NoZip', 'Encryption First', 'compression ratio'))
        print('std:', get_std(data, 'single-packet-tele-payload-bytes.data', 'NoEnc', 'NoZip', 'Encryption First', 'compression ratio'))
        print('max:', get_max(data, 'single-packet-tele-payload-bytes.data', 'NoEnc', 'NoZip', 'Encryption First', 'compression ratio'))
        print('min:', get_min(data, 'single-packet-tele-payload-bytes.data', 'NoEnc', 'NoZip', 'Encryption First', 'compression ratio'))

        # create_csv(data, file)