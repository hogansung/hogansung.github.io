import os

prog = '../xmlParser/main'
xml = '../xml'
dat = '../dat'

for idx in range(48):
    for mode in range(2):
        colName = '_'.join(['col', str(idx), str(mode)]) + '.csv'
        o_colPath = os.path.join(xml, colName);
        n_colPath = os.path.join(dat, colName);

        datName = '_'.join(['dat', str(idx), str(mode)]) + '.csv'
        o_datPath = os.path.join(xml, datName);
        n_datPath = os.path.join(dat, datName);

        cmd = ' '.join([prog, o_datPath, o_colPath, str(idx), str(mode), n_datPath, n_colPath])
        print cmd
        os.system(cmd)
