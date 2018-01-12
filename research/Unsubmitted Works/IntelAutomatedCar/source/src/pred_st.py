import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.metrics import f1_score, roc_auc_score, mean_squared_error, precision_recall_curve, accuracy_score, roc_curve, auc, matthews_corrcoef


gl_f = ['User', 'Scenario']
lt_f = ['Acceleration Average', 'Angle Variance', 'Average Angle', 'Average Front Dist', 'Average Insertion Space', 'Average Overtake Right Space', 'Average Overtake Space', 'Brake Average', 'Dist Before Lane Switch', 'Duration', 'Freq Collisions', 'Freq Insertion', 'Freq Lane Switch', 'Freq Overtake', 'Freq Overtake Right', 'High Speed Average', 'High Speed Ratio', 'High Speed Variance', 'Ratio Inseting too Close', 'Ratio Overtaking Right too Close', 'Ratio Overtaking too Close', 'Ratio too Close', 'Rotation when Overtaking', 'Speed Average', 'Speed Duration', 'Speed Variance', 'Speed When Overtaking', 'Time Big Turn', 'Total Average Angle', 'Rotation Avg', 'Time Big Rotation', 'Speed Dif When Overtaking']

bad_features = ['Average Overtake Right Space','Average Insertion Space', 'High Speed Variance']
identified_bad = ['Speed Average', 'Ratio too Close','Brake Average','Freq Insertion', 'Freq Overtake Right', 'Freq Overtake','Ratio Overtaking Right too Close', 'Angle Variance', 'Total Average Angle', 'Speed When Overtaking']
#tn_X = tn_X.drop(bad_features, axis=1)
#tn_X = tn_X.drop(identified_bad, axis=1)


st_f = ['st_a_ave', 'st_angle_ave', 'st_cl', 'st_d_f_ave', 'st_d_lf_ave', 'st_d_rf_ave', 'st_v_ave']
lb_l = ['st_ls_l']
lb_r = ['st_ls_r']
lb_a = ['st_ls_a']
lb_c = ['st_nc']
lb_os = ['st_os']
lb_tc = ['st_tc']
lb_ag = ['st_ag']


rf_c = RandomForestClassifier(n_estimators=500, n_jobs=-1, class_weight='auto', max_depth=5, max_features=None, random_state=514)
#lsvc_c = LinearSVC(class_weight=None, random_state=514, verbose=True, C=0.1)
#gbm_c = GradientBoostingClassifier(random_state=514)
#lsvc_c = LinearSVC(random_state=514)
svc_c = SVC(random_state=514, probability=True, kernel='rbf', C=0.25, class_weight='auto', gamma=1.0/50)

def readFile(fp):
    df = pd.read_csv(fp)
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


def findTH(y, pp):
    precision, recall, thresholds = precision_recall_curve(y, pp)
    best_f1 = -1
    best_th = 0
    for p, r, t in zip(precision[1:], recall[1:], thresholds):
        f1 = 2 * p * r / (p + r)
        if f1 > best_f1:
            best_f1 = f1
            best_th = t
    print best_f1, best_th
    return best_th


def plotROC(y, p, target):
    fpr, tpr, _ = roc_curve(y, p)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC_' + target)
    plt.legend(loc="lower right")
    plt.savefig('../doc_img/' + 'ROC_' + '_'.join(target.split()) + '.png', dpi=300)


def plotMulROC(ypList, title):
    plt.figure()

    for y, p, target in ypList:
        fpr, tpr, _ = roc_curve(y, p)
        roc_auc = auc(fpr, tpr)

        plt.plot(fpr, tpr, label='ROC curve of ' + target + ' (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC_' + title)
        plt.legend(loc="lower right")

    plt.savefig('../doc_img/' + 'ROC_' + '_'.join(title.split()) + '.png', dpi=300)


def classify(tn_X, tn_y, vl_X, vl_y, target):
    print '---------------------------------------\n' + 'Now is working on: ' + target + '\n'

    '''
    gbm_c.fit(tn_X, tn_y)
    tn_p = gbm_c.predict(tn_X)
    vl_p = gbm_c.predict(vl_X)
    tn_pp = gbm_c.predict_proba(tn_X)[:, 1]
    vl_pp = gbm_c.predict_proba(vl_X)[:, 1]
    '''
 
    svc_c.fit(tn_X, tn_y)
    tn_p = svc_c.predict(tn_X)
    vl_p = svc_c.predict(vl_X)
    tn_pp = svc_c.predict_proba(tn_X)[:, 1]
    vl_pp = svc_c.predict_proba(vl_X)[:, 1]
    
    '''
    rf_c.fit(tn_X, tn_y)
    tn_p = rf_c.predict(tn_X)
    vl_p = rf_c.predict(vl_X)
    tn_pp = rf_c.predict_proba(tn_X)[:, 1]
    vl_pp = rf_c.predict_proba(vl_X)[:, 1]
    '''

    #z_tn_p = pd.Series(np.zeros(tn_p.shape[0]))
    #z_vl_p = pd.Series(np.zeros(vl_p.shape[0]))

    #print rf_c.feature_importances_

    #best_th = findTH(tn_y, tn_pp[:, 1])
    #tn_p = map(int, tn_pp[:, 1] > best_th)
    #vl_p = map(int, vl_pp[:, 1] > best_th)

    #print sum(tn_y)
    #print sum(tn_p)
    #print sum(vl_y)
    #print sum(vl_p)

    #print 'tn->tn (acc)', accuracy_score(tn_y, tn_p)
    print 'tn->tn (f1)', f1_score(tn_y, tn_p)
    print 'tn->tn (auc)', roc_auc_score(tn_y, tn_pp) 
    print 'tn->tn (mat)', matthews_corrcoef(tn_y, tn_p)
    #print 'tn->tn (reg)', mean_squared_error(tn_y, tn_pp[:, 1])
    print 'tn->z_tn (acc)', accuracy_score(tn_y, tn_p)

    #print 'tn->vl (acc)', accuracy_score(vl_y, vl_p)
    print 'tn->vl (f1)', f1_score(vl_y, vl_p)
    print 'tn->vl (auc)', roc_auc_score(vl_y, vl_pp)
    print 'tn->vl (mat)', matthews_corrcoef(vl_y, vl_p)
    #print 'tn->vl (reg)', mean_squared_error(vl_y, vl_pp[:, 1])
    print 'tn->z_vl (acc)', accuracy_score(vl_y, vl_p)

    #plotROC(vl_y, vl_pp[:, 1], target)
    return tn_y, tn_pp, vl_y, vl_pp


def main():
    auc_res = []
    for idx in [30, 20, 10]:
        for jdx in [5, 10]:
            suffix = '_' + str(idx) + '_' + str(jdx)

            # read file
            tn_dList = readFile('../fts/combine_tn' + suffix + '.csv')
            vl_dList = readFile('../fts/combine_vl' + suffix + '.csv')
            print 'working on:', idx, jdx


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
            colName = ['collisions', 'all lane switches', 'all aggressiveness', 'over speed', 'too close', 'lane switch to left', 'lane switch to right']

            MERGE_FLAG = False

            if MERGE_FLAG:
                tn_y_df = pd.DataFrame(index=range(len(tn_dList[0][1])))
                tn_pp_df = pd.DataFrame(index=range(len(tn_dList[0][1])))
                vl_y_df = pd.DataFrame(index=range(len(vl_dList[0][1])))
                vl_pp_df = pd.DataFrame(index=range(len(vl_dList[0][1])))

            for i in range(7):
                if i != 2:
                    continue
                #if i < 3:
                    #continue
                tn_y, tn_pp, vl_y, vl_pp = classify(tn_tList[i][0], tn_tList[i][1], vl_tList[i][0], vl_tList[i][1], colName[i] + suffix)
                
                if MERGE_FLAG:
                    tn_y_df = tn_y_df.join(pd.DataFrame({colName[i] : tn_y}))
                    tn_pp_df = tn_pp_df.join(pd.DataFrame({colName[i] : tn_pp}))
                    vl_y_df = vl_y_df.join(pd.DataFrame({colName[i] : vl_y}))
                    vl_pp_df = vl_pp_df.join(pd.DataFrame({colName[i] : vl_pp}))

            if MERGE_FLAG:
                tn_y = tn_y_df.apply(lambda x: int(sum(x) > 0), axis=1)
                tn_pp = tn_pp_df.apply(np.max, axis=1)
                vl_y = vl_y_df.apply(lambda x: int(sum(x) > 0), axis=1)
                vl_pp = vl_pp_df.apply(np.max, axis=1)

                print '\nMERGE'
                print 'tn->tn (auc)', roc_auc_score(tn_y, tn_pp) 
                print 'tn->vl (auc)', roc_auc_score(vl_y, vl_pp)
                print '\n\n'

            #auc_res.append([vl_y, vl_pp, 'lane switch to left' + suffix])


    # plot figures: predicting lane switch to left
    '''
    plotMulROC([auc_res[i] for i in range(0, 6, 2)], 'Predicting lane switch to left 5 seconds in advance')
    plotMulROC([auc_res[i] for i in range(1, 6, 2)], 'Predicting lane switch to left 10 seconds in advance')
    plotMulROC([auc_res[i] for i in range(0, 2)], 'Predicting lane switch to left using 30 seconds history')
    plotMulROC([auc_res[i] for i in range(2, 4)], 'Predicting lane switch to left using 20 seconds history')
    plotMulROC([auc_res[i] for i in range(4, 6)], 'Predicting lane switch to left using 10 seconds history')
    '''

    # plot figures: predicting lane switch to right
    '''
    plotMulROC([auc_res[i] for i in range(0, 6, 2)], 'Predicting lane switch to right 5 seconds in advance')
    plotMulROC([auc_res[i] for i in range(1, 6, 2)], 'Predicting lane switch to right 10 seconds in advance')
    plotMulROC([auc_res[i] for i in range(0, 2)], 'Predicting lane switch to right using 30 seconds history')
    plotMulROC([auc_res[i] for i in range(2, 4)], 'Predicting lane switch to right using 20 seconds history')
    plotMulROC([auc_res[i] for i in range(4, 6)], 'Predicting lane switch to right using 10 seconds history')
    '''


if __name__ == '__main__':
    main()
