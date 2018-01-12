import os
import pandas as pd

RADAR_TARGETS = ['Velocity', 'Dist to Front', 'Dist to Back', 'Dist to Left-Front', 'Dist to Left-Back', 'Dist to Right-Front', 'Dist to Right-Back']

sumList = [0 for i in xrange(len(RADAR_TARGETS))]
maxList = [-1000 for i in xrange(len(RADAR_TARGETS))]
minList = [1000 for i in xrange(len(RADAR_TARGETS))]

with open('../fts/radarStat.csv', 'w') as f:
    f.write(','.join(['User','Scenario'] + RADAR_TARGETS) + '\n')

    for idx in range(48):
        for mode in range(2):
            datName = '_'.join(['dat', str(idx), str(mode)]) + '.csv'
            datPath = os.path.join('../dat', datName);

            data = pd.read_csv(datPath, header=1)[RADAR_TARGETS]
            for name in ['Dist to Front', 'Dist to Back', 'Dist to Left-Front', 'Dist to Left-Back', 'Dist to Right-Front', 'Dist to Right-Back']:
                data[name] = data[name].apply(lambda x: x if x <= 200 and x >= 0 else 200)
#            data['Acceleration'] = data['Acceleration'].apply(lambda x: x if x >= -15 else 0)
            mean = data.mean().tolist()
            maxl = data.max().tolist()
            minl = data.min().tolist()

            for i in range(len(sumList)): 
                sumList[i] += mean[i] / (48 * 2)
                maxList[i] = max(maxList[i], maxl[i])
                minList[i] = min(minList[i], minl[i])

            f.write(','.join(map(str, [idx, mode] + mean)) + '\n')

    for i in range(len(minList)):
        minList[i] = max(minList[i], 0.000001)

    for i in range(1, len(maxList)):
        maxList[i] += 50

    f.write(','.join(map(str, [-1, -1] + sumList)) + '\n') # -1, -1: sum
    f.write(','.join(map(str, [-2, -2] + maxList)) + '\n') # -2, -2: max
    f.write(','.join(map(str, [-3, -3] + minList)) + '\n') # -3, -3: min
