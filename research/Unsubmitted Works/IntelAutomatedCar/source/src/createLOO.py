import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.metrics import f1_score, roc_auc_score, mean_squared_error, precision_recall_curve, accuracy_score, roc_curve, auc, matthews_corrcoef


# constant define 
idx = 30
jdx = 5
FIRST_THRESHOLD = 0.05
SECOND_THRESHOLD = 0.15


# model setting
svc_c = SVC(random_state=514, probability=True, kernel='rbf', C=0.25, class_weight='auto', gamma=1.0/50)


# feature setting
st_f = ['st_a_ave', 'st_angle_ave', 'st_cl', 'st_d_f_ave', 'st_d_lf_ave', 'st_d_rf_ave', 'st_v_ave']
lb_l = ['st_ls_l']
lb_r = ['st_ls_r']
lb_a = ['st_ls_a']
lb_c = ['st_nc']
lb_os = ['st_os']
lb_tc = ['st_tc']
lb_ag = ['st_ag']

gl_f = ['User', 'Scenario', 'st_t_stamp']
lt_f = ['Acceleration Average', 'Angle Variance', 'Average Angle', 'Average Front Dist', 'Average Insertion Space', 'Average Overtake Right Space', 'Average Overtake Space', 'Brake Average', 'Dist Before Lane Switch', 'Duration', 'Freq Collisions', 'Freq Insertion', 'Freq Lane Switch', 'Freq Overtake', 'Freq Overtake Right', 'High Speed Average', 'High Speed Ratio', 'High Speed Variance', 'Ratio Inserting too Close', 'Ratio Overtaking Right too Close', 'Ratio Overtaking too Close', 'Ratio too Close', 'Speed Average', 'Speed Duration', 'Speed Variance', 'Speed When Lane Switch', 'Time Big Turn', 'Total Average Angle', 'Rotation Avg', 'Time Big Rotation', 'Speed Dif When Lane Switch']
bad_features = ['Average Overtake Right Space','Average Insertion Space', 'High Speed Variance']
identified_bad = ['Speed Average', 'Ratio too Close','Brake Average','Freq Insertion', 'Freq Overtake Right', 'Freq Overtake','Ratio Overtaking Right too Close', 'Angle Variance', 'Total Average Angle', 'Speed When Lane Switch']


def read_lt():
    lt_l = defaultdict()
    lt_f = pd.read_csv('../fts/LOO_lt_stats.csv')
    for i in xrange(lt_f.shape[0]):
        inst = lt_f.iloc[i, :]
        lt_l[int(inst['User'] * 2 + inst['Scenario'])] = inst
    return lt_l


def read_st():
    st_l = defaultdict(list)
    st_f = pd.read_csv('../fts/LOO_st_stats' + '_' + str(idx) + '_' + str(jdx) + '.csv')
    for i in xrange(st_f.shape[0]):
        inst = st_f.iloc[i, :]
        st_l[int(inst['User'] * 2 + inst['Scenario'])].append(inst[2:])
    return st_l


def createFeature(num_inst, lt_l, st_l, target):
    tn_df = pd.DataFrame()
    vl_df = pd.DataFrame()
    for i in range(num_inst):
        for j in range(2):
            _df = pd.DataFrame()
            for st in st_l[i * 2 + j]:
                _df = _df.append(lt_l[i * 2 + j].append(st), ignore_index=True)
            if i != target:
                tn_df = tn_df.append(_df)
            else:
                vl_df = vl_df.append(_df)
    return tn_df, vl_df


def extractFeatures(df):
    cX = df[lt_f + st_f].drop(bad_features + identified_bad, axis=1)
    cy = df[lb_c].squeeze()

    aX = df[lt_f + st_f].drop(bad_features + identified_bad, axis=1)
    ay = df[lb_a].squeeze()
    
    agX = df[lt_f + st_f].drop(bad_features + identified_bad, axis=1)
    agy = df[lb_ag].squeeze()

    osX = df[lt_f + st_f].drop(bad_features + identified_bad, axis=1)
    osy = df[lb_os].squeeze()

    tcX = df[lt_f + st_f].drop(bad_features + identified_bad, axis=1)
    tcy = df[lb_tc].squeeze()

    df_l = df#[df['st_cl'] > 0]
    lX = df_l[lt_f + st_f]
    lX = lX.drop(bad_features + identified_bad, axis=1)
    ly = df_l[lb_l].squeeze()

    df_r = df#[df['st_cl'] < 2]
    rX = df_r[lt_f + st_f]
    rX = rX.drop(bad_features + identified_bad, axis=1)
    ry = df_r[lb_r].squeeze()

    return [[cX, cy], [aX, ay], [agX, agy], [osX, osy], [tcX, tcy], [lX, ly], [rX, ry]]


def stagedLabel(pp):
    sp = sorted(pp, reverse=True)
    ft = sp[int(FIRST_THRESHOLD * len(pp))]
    st = sp[int(SECOND_THRESHOLD * len(pp))]

    ret = []
    for v in pp:
        if v < st:
            ret.append(0)
        elif v < ft:
            ret.append(1)
        else:
            ret.append(2)
    return np.array(ret)


def classify(tn_X, tn_y, vl_X, vl_y, target):
    print 'Now is working on: ' + target

    svc_c.fit(tn_X, tn_y)
    tn_p = svc_c.predict(tn_X)
    vl_p = svc_c.predict(vl_X)
    tn_pp = svc_c.predict_proba(tn_X)[:, 1]
    vl_pp = svc_c.predict_proba(vl_X)[:, 1]
    
    #print 'tn->tn (f1)', f1_score(tn_y, tn_p)
    #print 'tn->tn (auc)', roc_auc_score(tn_y, tn_pp) 
    #print 'tn->tn (mat)', matthews_corrcoef(tn_y, tn_p)
    #print 'tn->z_tn (acc)', accuracy_score(tn_y, tn_p)

    #print 'tn->vl (f1)', f1_score(vl_y, vl_p)
    #print 'tn->vl (auc)', roc_auc_score(vl_y, vl_pp)
    #print 'tn->vl (mat)', matthews_corrcoef(vl_y, vl_p)
    #print 'tn->z_vl (acc)', accuracy_score(vl_y, vl_p)

    return tn_y, tn_pp, vl_y, stagedLabel(vl_pp)


def main():
    # read lt data
    lt_l = read_lt()

    # read st data
    st_l = read_st()

    # get the instance number
    num_inst = len(lt_l) / 2

    # create table for all drivers
    drivers_df = pd.DataFrame()
    for i in range(num_inst):
        tn_df, vl_df = createFeature(num_inst, lt_l, st_l, i)
        tn_dList = extractFeatures(tn_df)
        vl_dList = extractFeatures(vl_df)

        # scale data
        tn_tList = []
        vl_tList = []
        for tn, vl in zip(tn_dList, vl_dList):
            scaler = StandardScaler().fit(tn[0])
            tn_tX = pd.DataFrame(scaler.transform(tn[0]))
            vl_tX = pd.DataFrame(scaler.transform(vl[0]))
            tn_tList.append([tn_tX, tn[1]])
            vl_tList.append([vl_tX, vl[1]])

        
        # classify
        # c, a, ag, os, tc, l, r
        colName = ['sudden break', 'over speed', 'too close', 'lane switch to left', 'lane switch to right']


        # create table for one driver
        print 'Now is at round #' + str(i)
        driver_df = vl_df[gl_f]

        for j in range(7):
            tn_y, tn_pp, vl_y, vl_pp = classify(tn_tList[j][0], tn_tList[j][1], vl_tList[j][0], vl_tList[j][1], colName[j])
            driver_df = driver_df.join(pd.DataFrame({colName[j] : vl_pp}))

        drivers_df = drivers_df.append(driver_df)


    # write into file
    drivers_df.to_csv('../fts/LOO_prediction.csv', index=False) 
            

if __name__ == '__main__':
    main()
