import os

import pandas as pd


def getfiles():
    filenames = os.listdir('D:\\NLP_HW\\Task1\\data')
    scorelist = []
    filelist = []
    for name in filenames:
        if '.csv' in name:
            filelist.append(name)
            scorelist.append(float(name.replace('.csv', '')))
    return filelist, scorelist


if __name__ == '__main__':
    '''
        Only for Ensembling by the score of {score}.csv, so the path is hardcoded
    '''
    files, scores = getfiles()
    print(files, scores)
    picks = []
    labels = []
    temp0 = './data/'+str(files[0])
    ids = pd.read_csv(temp0)['source_id']
    print(ids)
    for fname in files:
        temp = './data/' + str(fname)
        picks.append(pd.read_csv(temp)['label_for_kaggle'])
    for id in range(100):
        num = []
        for i in range(2):
            num.append(0)
        for i in range(len(picks)):  # 对于id号第i个模型的结果
            label = picks[i][id]
            num[label] += scores[i]
        labels.append(num.index(max(num)))

    with open('submission.csv', 'w') as f:
        f.write('source_id,label_for_kaggle\n')
        for i in range(100):
            f.write(str(ids[i]) + ',' + str(labels[i]) + '\n')
