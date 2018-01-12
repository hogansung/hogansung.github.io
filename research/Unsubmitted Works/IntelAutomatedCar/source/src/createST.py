import pandas as pd
import random
from collections import defaultdict


# read lt data
lt_l = defaultdict()

lt_f = pd.read_csv('../fts/lt_stats.csv')
for i in xrange(lt_f.shape[0]):
    inst = lt_f.iloc[i, :]
    lt_l[int(inst['User'] * 2 + inst['Scenario'])] = inst


# divide users
num_inst = lt_f.shape[0] / 2
print num_inst

num_tn = 30
num_tt = num_inst - num_tn
rows = random.sample(range(num_inst), num_tn)


# read st data
for idx in [30, 20, 10]:
    for jdx in [5, 10]:
        st_l = defaultdict(list)

        st_f = pd.read_csv('../fts/st_stats' + '_' + str(idx) + '_' + str(jdx) + '.csv')
        for i in xrange(st_f.shape[0]):
            inst = st_f.iloc[i, :]
            st_l[int(inst['User'] * 2 + inst['Scenario'])].append(inst[2:])

        # combine features
        tn_df = pd.DataFrame()
        vl_df = pd.DataFrame()
        for i in range(num_inst):
            for j in range(2):
                _df = pd.DataFrame()
                for st in st_l[i * 2 + j]:
                    _df = _df.append(lt_l[i * 2 + j].append(st), ignore_index=True)

                if i in rows:
                    tn_df = tn_df.append(_df)
                else:
                    vl_df = vl_df.append(_df)

        # write features
        tn_df.to_csv('../fts/combine_tn' + '_' + str(idx) + '_' + str(jdx) + '.csv', index=False)
        vl_df.to_csv('../fts/combine_vl' + '_' + str(idx) + '_' + str(jdx) + '.csv', index=False)
