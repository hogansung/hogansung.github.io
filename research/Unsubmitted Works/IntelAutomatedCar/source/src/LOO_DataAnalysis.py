#!/usr/bin/env 

import pandas as pd
from pandas import DataFrame

import numpy as np
import datetime
import os



class General:
    def __init__(self):
        self.lt_stats = pd.DataFrame()
        self.st_stats = pd.DataFrame()
        self.all_users = {}
        #TO DO : Find the names and copy here

    def readUserData(self, data_file, collision_file) :
        #read the first line to access timestamp, user id, mode 
        line=open(data_file).readline().rstrip().split(",")
        timestamp = float(line[0])
        user_id = float(line[1])
        user_mode = float(line[2])
        #read the files, and create dataframes
        data = pd.read_csv(data_file, header = 1, sep = ',')
        col = pd.read_csv(collision_file, header = 0, sep = ',')
        # Access the user if he is already present
        if (user_id in self.all_users):
            user = self.all_users[user_id]
        else:
            user = User(user_id)
            self.all_users[user_id] = user
        user.addData(data, col, timestamp, user_mode)

    def lt_setRangedStats(self, st, ed):
        for i, u in self.all_users.iteritems():
            u.lt_stats = pd.DataFrame()
            u.lt_statWindows(st, ed)
            self.lt_stats = self.lt_stats.append(u.lt_stats, ignore_index=True)

    def st_setRangedStats(self, st, st_f, st_l):
        print 'f_w', st, st + st_f
        print 'l_w', st + st_f, st + st_f + st_l
        for i, u in self.all_users.iteritems():
            u.st_stats = pd.DataFrame()
            u.st_statWindows(st, st_f, st_l)
            self.st_stats = self.st_stats.append(u.st_stats, ignore_index=True)
    


class User:
    def __init__(self, id):
        self.id = id
        self.datas = []
        self.lt_stats = pd.DataFrame()
        self.st_stats = pd.DataFrame()

    def addData(self, data, collision, timestamp, mode):
        #Get new data
        new_data = data
        new_col = collision
        #Compute collisions
        if len(new_col) > 0:
            new_col = self.cleanCollisions(new_col)
        new_data = self.setCollisionTime(timestamp, new_col, new_data)
        # Add the Collision Number Column
        tmp = np.empty(new_data.shape[0])
        tmp.fill(len(new_col))
        mode_col = pd.Series(tmp, name='Nb Collisions')
        new_data = pd.concat([new_data, mode_col], axis=1)
        # Compute frames durations
        new_data = self.setDurations(new_data)
        #add the mode column
        tmp = np.empty(new_data.shape[0])
        tmp.fill(mode)
        mode_col = pd.Series(tmp, name='Mode')
        new_data = pd.concat([new_data, mode_col], axis=1)
        # Compute switching Lanes
        lane_switch = new_data['Current Lane'].diff()
        lane_switch.iloc[0]=0
        lane_switch.name = 'Lane Switch'
        new_data = pd.concat([new_data, lane_switch], axis=1)
        # add the new data
        self.datas.append(new_data)

    def cutUnused(self, fdata):
        # Keep Only if : Velocity > 0 or Pedal or Steer > 0
        fdata = fdata[(fdata['Velocity']>0.1) | ( (abs(fdata['Pedal'])>0.1) | (abs(fdata['Steer'])>0.0001)) ]
        # Note : it doesn't really take off the "starting phase" or the stopping one. 
        return fdata

    def setDurations(self, fdata):
        duration = fdata['Time'].diff()
        duration.name = 'Duration'
        duration.iloc[0] = 0
        fdata = pd.concat([duration, fdata], axis=1)
        return fdata

    def cleanCollisions(self, fcol):
        tmp = fcol.diff()['Timestamp']
        tmp[0] = fcol['Timestamp'][0]
        fcol = fcol[tmp>1]
        return fcol

    def to_seconds(self, dt): 
        return dt / np.timedelta64(1, 's')

    def setCollisionTime(self, ftimestamp, fcol, fdata):
        #Find the moment the collisions occured, in seconds after the beginning of the start
        dateRun = datetime.datetime.fromtimestamp(ftimestamp)
        dateCol = fcol['Timestamp'].apply(datetime.datetime.fromtimestamp)
        dateCol = (dateCol - dateRun).apply(self.to_seconds)
        # Add an empty comlumn for collisions
        tmp = np.empty(fdata.shape[0])
        tmp.fill(0)
        col_col = pd.Series(tmp, name='Collisions')
        fdata = pd.concat([fdata, col_col], axis=1)
        #set the collision to 1 if a collision occured at that seconds
        for it in dateCol.iteritems():
            i = fdata[(fdata['Time']>it[1])].head(1).index
            fdata.loc[i,'Collisions'] = 1
        return fdata

    def lt_statWindows(self, st, ed):
        for dat in self.datas:
            self.lt_stats = self.lt_stats.append(self.lt_statistics(dat[(dat['Time'] > st - 0.001) & (dat['Time'] < ed + 0.001)]))

    def st_statWindows(self, st, st_f, st_l):
        for dat in self.datas:
            f_window = dat[(dat['Time'] > st - 0.001) & (dat['Time'] < st + st_f + 0.001)]
            l_window = dat[(dat['Time'] > st + st_f - 0.001) & (dat['Time'] < st + st_f + st_l + 0.001)]

            if len(f_window) == 0 or len(l_window) == 0: 
                continue
            else:
                self.st_stats = self.st_stats.append(self.st_statistics(f_window, l_window))

    def lt_statistics(self, window, th=0.4, limit=200):
        window = window.reset_index()
        df = pd.DataFrame([{'User' : self.id, 'Scenario' : window.iloc[0]['Mode']}])
        duration = window['Duration'].sum()
        df = df.join(pd.DataFrame([duration], columns = ['Duration']))
        df = df.join(self.speedFeatures(window, limit, duration))
        df = df.join(self.accelFeatures(window))
        df = df.join(self.frontdistFeatures(window, th, limit, duration))
        df = df.join(self.switchFeatures(window, th, limit, duration))
        df = df.join(self.steerFeatures(window, duration)) # There are missing mistakes
        df = df.join(pd.DataFrame([1.0*window['Collisions'].sum()/duration], columns = ['Freq Collisions']))
        return df

    def st_statistics(self, f_window, l_window, th=0.4, limit=200):
        df = pd.DataFrame([{'User' : self.id, 'Scenario' : f_window.iloc[0]['Mode']}])

        data = dict()
        data['st_t_stamp'] = l_window.iloc[0]['Time']
        data['st_cl'] = f_window.iloc[-1]['Current Lane']

        # speed features
        data['st_v_ave'] = self.weightedAverage(f_window['Velocity'], f_window['Duration'])
        a_period = f_window[f_window['Acceleration'] > 0.1]
        data['st_a_ave'] = self.weightedAverage(a_period['Acceleration'], a_period['Duration'])

        # steer fratures
        steer_p = self.findSteeringPhases(f_window, 0.01)
        turn_df = pd.DataFrame(columns=f_window.columns)
        for p in steer_p:
            turn_df = turn_df.append(f_window[p[0] : p[1]])
        data['st_angle_ave'] = self.weightedAverage(abs(turn_df['Steer']),turn_df['Duration'])

        # dist features
        close = f_window.copy()
        close['Dist to Front'].where((close['Dist to Front']<limit) & (close['Dist to Front']>0), other=limit, inplace = True)
        close['Dist to Left-Front'].where((close['Dist to Left-Front']<limit) & (close['Dist to Left-Front']>0), other=limit, inplace = True)
        close['Dist to Right-Front'].where((close['Dist to Right-Front']<limit) & (close['Dist to Right-Front']>0), other=limit, inplace = True)
        data['st_d_f_ave'] = self.weightedAverage(close['Dist to Front'],close['Duration'])
        data['st_d_lf_ave'] = self.weightedAverage(close['Dist to Left-Front'],close['Duration'])
        data['st_d_rf_ave'] = self.weightedAverage(close['Dist to Right-Front'],close['Duration'])

        # switch features
        ls_l = l_window[l_window['Lane Switch'] > 0]
        ls_r = l_window[l_window['Lane Switch'] < 0]
        ls_a = l_window[l_window['Lane Switch'] != 0]
        data['st_ls_l'] = int(len(ls_l) > 0)
        data['st_ls_r'] = int(len(ls_r) > 0)
        data['st_ls_a'] = int(len(ls_a) > 0)

        # collision features
        data['st_nc'] = int(l_window['Collisions'].sum() > 0)

        # over speed features
        ls_os = l_window[l_window['Velocity'] > 95.0/3.6]
        data['st_os'] = int(len(ls_os) > 0)

        # too close features
        ls_tc = l_window[l_window['Dist to Front'] < th*l_window['Velocity']]
        data['st_tc'] = int(len(ls_tc) > 0)

        # aggressive features
        data['st_ag'] = int(len(ls_a) > 0 or len(ls_os) > 0 or len(ls_tc) > 0)

        return df.join(pd.DataFrame([data]))

    def speedFeatures(self, window, limit, duration):
        high_speed = window[window['Velocity']>(60.0/3.6)]
        high_speed_average = self.weightedAverage(high_speed['Velocity'], high_speed['Duration'])
        high_speed_variance =  self.weightedAverage( (high_speed['Velocity'] - high_speed_average)**2, high_speed['Duration'])
        high_speed_duration = high_speed['Duration'].sum()
        average = self.weightedAverage(window['Velocity'], window['Duration'])
        variance =  self.weightedAverage( (window['Velocity'] - average)**2, window['Duration'])
        data = {'High Speed Ratio' : high_speed_duration/duration, 'High Speed Average' : high_speed_average, 'High Speed Variance' : high_speed_variance, 'Speed Average' : average, 'Speed Variance' : variance}
        data['Speed Duration'] = high_speed['Duration'].sum()/duration

        # calculate relative Speed
        speeds = window[['Speed Front','Speed Front Left','Speed Front Right','Speed Back','Speed Back Left','Speed Back Right']].copy()
        speeds['Speed Front'].where(speeds['Speed Front']>0, other=0, inplace=True)
        speeds['Speed Front Left'].where(speeds['Speed Front Left']>0, other=0, inplace=True)
        speeds['Speed Front Right'].where(speeds['Speed Front Right']>0, other=0, inplace=True)
        speeds['Speed Back'].where(speeds['Speed Back']>0, other=0, inplace=True)
        speeds['Speed Back Left'].where(speeds['Speed Back Left']>0, other=0, inplace=True)
        speeds['Speed Back Right'].where(speeds['Speed Back Right']>0, other=0, inplace=True)

        speeds['Speed Front'].where(window['Dist to Front']<limit, other=0, inplace=True)
        speeds['Speed Front Left'].where(window['Dist to Left-Front']<limit, other=0, inplace=True)
        speeds['Speed Front Right'].where(window['Dist to Right-Front']<limit, other=0, inplace=True)
        speeds['Speed Back'].where(window['Dist to Back']<limit, other=0, inplace=True)
        speeds['Speed Back Left'].where(window['Dist to Left-Back']<limit, other=0, inplace=True)
        speeds['Speed Back Right'].where(window['Dist to Right-Back']<limit, other=0, inplace=True)

        speeds_around = speeds.sum(axis=1)
        nb_cars = pd.DataFrame(np.zeros((len(speeds_around),6)) , index=speeds_around.index, columns=['FL','FC','FR','BL','BC','BR'])
        nb_cars['FL'].where(speeds['Speed Front Left'] == 0, other=1, inplace=True)
        nb_cars['FC'].where(speeds['Speed Front'] == 0, other=1, inplace=True)
        nb_cars['FR'].where(speeds['Speed Front Right'] == 0, other=1, inplace=True)
        nb_cars['BL'].where(speeds['Speed Back Left'] == 0, other=1, inplace=True)
        nb_cars['BC'].where(speeds['Speed Back'] == 0, other=1, inplace=True)
        nb_cars['BR'].where(speeds['Speed Back Right'] == 0, other=1, inplace=True)

        nb_car=nb_cars.sum(axis=1)
        non_zero_nb_car = nb_car.where(nb_car>0, other=1)
        speed_around = speeds_around / non_zero_nb_car
        speed_around.where(nb_car>0, other=1, inplace=True)

        data['Speed Rel Other'] = self.weightedAverage(window['Velocity'] / speed_around, window['Duration']) 
        df = pd.DataFrame([data])
        return df

    def accelFeatures(self, window):
        # Acceleration Stats
        accel_period = window[window['Acceleration'] > 0.1]
        acceleration_average = self.weightedAverage(accel_period['Acceleration'], accel_period['Duration'])
        brake_period = window[window['Acceleration'] < -0.1]
        brake_average = self.weightedAverage(abs(brake_period['Acceleration']), brake_period['Duration'])
        return pd.DataFrame([{'Acceleration Average' : acceleration_average, 'Brake Average' : brake_average}])

    def frontdistFeatures(self, window, th, limit, duration) :
        close = window.copy()
        close['Dist to Front'].where((close['Dist to Front']<limit) & (close['Dist to Front'] > 0), other=limit, inplace=True)

        average_dist = self.weightedAverage(close['Dist to Front'],close['Duration'])
        time_too_close = window[(window['Dist to Front']<th*window['Velocity']) & (window['Dist to Front'] > 0)]['Duration'].sum()
        data = {'Average Front Dist' : average_dist, 'Ratio too Close' : time_too_close / duration}
        return pd.DataFrame([data])

    def switchFeatures(self, window, th, limit, duration):
        lane_switch_i, change = self.findLaneChangePhases(window)
        ls_b = lane_switch_i[0]
        ls_a = lane_switch_i[1]

        if (len(ls_b) != len(ls_a)):
            print "DETAILS NEEDED"

        #Frequency Lane Switch
        nb_lane_switch = len(ls_b)
        data = {'Freq Lane Switch' : 1.0 * nb_lane_switch / duration}

        # Before Crossing the Lane
        before = window.iloc[ls_b].copy()
        before['Dist to Front'].where((before['Dist to Front']>0)&(before['Dist to Front']<limit), other=limit, inplace=True)
        
        data['Dist Before Lane Switch'] = self.weightedAverage(before['Dist to Front'], before['Duration'])
        if nb_lane_switch == 0:
            data['Dist Before Lane Switch'] = limit
        if data['Dist Before Lane Switch'] == 0:
            print 'Dist Before Overtaking = 0'
            print window['Time'][0]

        # Statistics "When Changing Lane"
        if nb_lane_switch == 0:
            data['Speed When Lane Switch'] = 0
            data['Speed Dif When Lane Switch'] = 1
            data['Rotation when Lane Switch'] = 0
            data['Average Duration Lane Switch'] = 0
            data['Average Distance Lane Switch'] = limit

        else:
            data['Speed When Lane Switch'] = self.weightedAverage(change['Velocity'], change['Duration'])
            data['Speed Dif When Lane Switch'] = self.weightedAverage(change['Velocity']/   window['Velocity'].mean(), change['Duration'])
            data['Rotation when Lane Switch'] = self.weightedAverage(abs(change['Rotation Z']), change['Duration'])
            data['Average Duration Lane Switch'] = change['Duration'].sum() / nb_lane_switch
            sum_dist = (window.loc[ls_a].reset_index()['X'] - window.loc[ls_b].reset_index()['X']).sum()
            data['Average Distance Lane Switch'] = 1.0 * sum_dist / nb_lane_switch

        lane_switch = change[change['Lane Switch'] != 0].copy()
        lane_switch_right = change[change['Lane Switch'] < 0].copy()
        # "Insertion" Space
        inser = lane_switch[(lane_switch['Dist to Back']>0) & (lane_switch['Dist to Front']>0)]
        inser_r = lane_switch_right[(lane_switch_right['Dist to Back']>0) & (lane_switch_right['Dist to Front']>0)]

        distance = (inser['Dist to Back'] + inser['Dist to Front']).copy()
        distance.where(distance<2*limit,other = 2*limit, inplace=True)

        th_r = inser['Velocity'] * th * 2

        data['Average Insertion Space'] = self.weightedAverage(distance, inser['Duration'])
        nb_inser = len(distance[distance<2*limit])
        data['Freq Insertion'] = 1.0 * nb_inser / duration
        if  nb_inser == 0:
            data['Ratio Inseting too Close'] = 0
        else:
            data['Ratio Inseting too Close'] = 1.0 * len(distance[distance<th_r]) / nb_inser

        # "Overtaking" Distance 
#        over  = lane_switch[lane_switch['Dist to Back']>0]
#        over_r  = lane_switch_right[lane_switch_right['Dist to Back']>0]
        over  = lane_switch.copy()
        over_r  = lane_switch_right.copy()

        over['Dist to Back'].where( (over['Dist to Back']<limit) & (over['Dist to Back'] > 0), other = limit, inplace=True)
        data['Average Overtake Space'] = self.weightedAverage(over['Dist to Back'],over['Duration'])
 
        th_r = over['Velocity'] * th

        nb_overtake = len(over[over['Dist to Back']<limit])
        data['Freq Overtake'] = 1.0 * nb_overtake / duration
        if nb_overtake == 0:
            data['Ratio Overtaking too Close'] = 0
        else:
            data['Ratio Overtaking too Close'] = 1.0 * len(over[over['Dist to Back']<th_r]) / nb_overtake
    
        th_r = over_r['Velocity'] * th

        over_r['Dist to Back'].where((over_r['Dist to Back']<limit) & (over_r['Dist to Back'] > 0), other = limit, inplace=True)
#        data['Average Overtake Right Space'] = self.weightedAverage(over_r[over_r['Dist to Back']<4*th]['Dist to Back'],over_r[over_r['Dist to Back']<4*th]['Duration'])
        data['Average Overtake Right Space'] = self.weightedAverage(over_r['Dist to Back'],over_r['Duration'])
        nb_overtake_r = len(over_r[over_r['Dist to Back']<limit])        
        data['Freq Overtake Right'] = 1.0 * nb_overtake_r / duration
        if nb_overtake_r==0:
            data['Ratio Overtaking Right too Close'] = 0
        else:
            data['Ratio Overtaking Right too Close'] = 1.0 * len(over_r[over_r['Dist to Back']<th_r]) / nb_overtake_r

        return pd.DataFrame([data])

    def steerFeatures(self, window, duration):
        data = dict()
        total_phases = self.findSteeringPhases(window, 0.001)
        turn_df = pd.DataFrame(columns=window.columns)
        for p in total_phases:
            p_df = window[p[0]:p[1]]
            turn_df = turn_df.append(p_df)
        data['Total Average Angle'] = self.weightedAverage(abs(turn_df['Steer']),turn_df['Duration'])
        data['Angle Variance'] = self.weightedAverage( (abs(turn_df['Steer']) - data['Total Average Angle'])**2, turn_df['Duration'])
        
        phases = self.findSteeringPhases(window, 0.01)
       
        turn_df = pd.DataFrame(columns=window.columns)
        for p in phases:
            p_df = window[p[0]:p[1]]
            turn_df = turn_df.append(p_df)
        if len(phases)==0:
            data['Average Angle'] = 0.01
        else:
            data['Average Angle'] = self.weightedAverage(abs(turn_df['Steer']),turn_df['Duration'])

        phases = self.findSteeringPhases(window,0.03)
        turn_df = pd.DataFrame(columns=window.columns)
        for p in phases:
            p_df = window[p[0]:p[1]]
            turn_df = turn_df.append(p_df)
        data['Time Big Turn'] = turn_df['Duration'].sum() / duration

        if data['Average Angle'] == 0:
            print "Average Angle = 0; id= " + str(self.id)
            print window['Steer'].max()

        #Rotation:
        data['Rotation Avg'] = abs(window['Rotation Z']).mean()
        big_rot = window[window['Rotation Z']>0.015]
        data['Time Big Rotation'] = big_rot['Duration'].sum()

        return pd.DataFrame([data])

    def findSteeringPhases(self, w, s_tol):
        frame_begin = -1
        res = []
        for i, row in w.iterrows():
            if (frame_begin == -1 ):   
                if (abs(row['Steer']) > s_tol):
                    frame_begin = i
            elif (abs(row['Steer']) < s_tol):
                res.append((frame_begin, i))
                frame_begin = -1
        return res

    def findLaneChangePhases(self, w):
        change = w[w['Lane Left'] != w['Lane Right']]
        if (len(change)==0):
            return ([], []), pd.DataFrame(columns=w.columns)
        
        frame_begin = -1
        prev = change.index[0]-1
        before = []
        after = []

        lane_changes = pd.DataFrame(columns=change.columns)
        for i, row in change.iterrows():
            if (frame_begin == -1 ):   
                frame_begin = i
            elif (i != prev + 1):
                if change.loc[frame_begin]['Current Lane'] != change.loc[prev]['Current Lane']: 
                    before.append(frame_begin)
                    after.append(prev)
                    lane_changes = lane_changes.append(change.loc[frame_begin:prev])
                frame_begin = -1
            prev = i
        return (before,after), lane_changes
        
    def weightedAverage(self, values, weights):
        if (weights.sum() == 0):
            return 0
        return np.average(values, weights = weights)

gral = General()

fd = '../dat/'

num_files = len(os.listdir(fd)) / 4
print os.listdir(fd)
print num_files

for i in xrange(num_files):
    #if i == 11 or i == 17:              # the files with problem
        #continue
    for j in xrange(2):
        datf = os.path.join(fd, 'dat_' + str(i) + '_' + str(j) + '.csv')
        colf = os.path.join(fd, 'col_' + str(i) + '_' + str(j) + '.csv')
        gral.readUserData(datf, colf)

gral.lt_setRangedStats(0, 300)
gral.lt_stats.to_csv('../fts/LOO_lt_stats.csv', index=False)

st_f = 30
st_l = 5
for i in range(0, 300 - st_f, st_l):
    gral.st_setRangedStats(i, st_f, st_l)
gral.st_stats.to_csv('../fts/LOO_st_stats' + '_' + str(st_f) + '_' + str(st_l) + '.csv', index=False)
