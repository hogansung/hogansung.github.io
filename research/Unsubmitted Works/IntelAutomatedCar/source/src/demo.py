''' import all needed packages '''
import os
import sys
import math
from collections import deque

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.figure import Figure
from matplotlib.path import Path
#from matplotlib.backends import qt_compat
#use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
#if use_pyside:
#    from PySide import QtGui, QtCore
#else:
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection



''' some definitions '''
COLOR_GREEN = 'rgba(50, 205, 50, 200)'
COLOR_YELLOW = 'rgba(255, 215, 0, 200)'
COLOR_RED = 'rgba(255, 69, 0, 200)'

USER_CAR_LENGTH = 3.8
USER_CAR_WIDTH = 1.4

FRAME_MIN_LIMIT = 0
FRAME_MAX_LIMIT = 1500

TIME_MAX_LIMIT = 300
FPS = 25
TIME_OUT = int(1000.0 / FPS)

ROAD_LINE_FILLED = 4
ROAD_LINE_BLANK = 6
ROAD_LINE_BLOCK = ROAD_LINE_FILLED + ROAD_LINE_BLANK
ROAD_LINE_WIDTH = 0.1
ROAD_LINE_NUMBER = int(math.ceil(200.0 / ROAD_LINE_BLOCK) + 1)

# Dirty hack: reverse left and right
#RADAR_TARGETS = ['Velocity', 'Dist to Front', 'Dist to Back', 'Dist to Left-Front', 'Dist to Left-Back', 'Dist to Right-Front', 'Dist to Right-Back']
RADAR_TARGETS = ['Velocity', 'Dist to Front', 'Dist to Back', 'Dist to Right-Front', 'Dist to Right-Back', 'Dist to Left-Front', 'Dist to Left-Back']
RADAR_LABELS = ['Velocity', 'Front Dist', 'Back Dist', 'Left-Front Dist', 'Left-Back Dist', 'Right-Front Dist', 'Right-Back Dist']
DIST_TARGETS = ['Dist to Front', 'Dist to Back', 'Dist to Left-Front', 'Dist to Left-Back', 'Dist to Right-Front', 'Dist to Right-Back']

COLOR_GREEN = 'rgba(50, 205, 50, 200)'
COLOR_YELLOW = 'rgba(255, 215, 0, 200)'
COLOR_RED = 'rgba(255, 69, 0, 200)'

#PRED_TARGETS = ['collisions', 'over speed', 'too close', 'lane switch to left', 'lane switch to right']
#PRED_LABELS = ['Collisions', 'Overspeeding', 'Too Close', 'Lane Switch to Left', 'Lane Switch to Right']
PRED_TARGETS = ['over speed', 'too close', 'lane switch to left', 'lane switch to right']
PRED_LABELS = ['Overspeeding', 'Too Close', 'Lane Switch to Left', 'Lane Switch to Right']

YLABEL_MAX_LEN = 18

SLIDER_STYLE = '''QSlider::groove:horizontal { border: 1px solid #bbb; background: white; height: 10px; border-radius: 4px; }
QSlider::sub-page:horizontal { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #66e, stop: 1 #bbf); background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, stop: 0 #bbf, stop: 1 #55f); border: 1px solid #777; height: 10px; border-radius: 4px; }
QSlider::add-page:horizontal { background: #fff; border: 1px solid #777; height: 10px; border-radius: 4px; }
QSlider::handle:horizontal { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #eee, stop:1 #ccc); border: 1px solid #777; width: 13px; margin-top: -2px; margin-bottom: -2px; border-radius: 4px; }
QSlider::handle:horizontal:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fff, stop:1 #ddd); border: 1px solid #444; border-radius: 4px; }
QSlider::sub-page:horizontal:disabled { background: #bbb; border-color: #999; }
QSlider::add-page:horizontal:disabled { background: #eee; border-color: #999; }
QSlider::handle:horizontal:disabled { background: #eee; border: 1px solid #aaa; border-radius: 4px; }'''



''' car canvas '''
class CarCanvas(FigureCanvas):
    def __init__(self, parent=None, dpi=300):
        self.xRange = (-100, 100)
        self.boundaries = (-100, 100, -13, 0.7)
        self.lineY = [-12.3, -8.2, -4.1, 0]
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
        self.fig.patch.set_alpha(0.0)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Fixed)
        FigureCanvas.updateGeometry(self)
        self.axes.set_aspect('equal')
        self.axes.tick_params(axis='y', left='off', right='off', labelleft='off', labelbottom='on')
        self.fig.subplots_adjust(left=0.0, right=1.0, bottom=0.04, top=1.0)

        self.lines = [0, deque(), deque(), 0]
        self.scList = []

    def drawBackground(self, xMin, xMax):
        self.lines[0] = plt.Rectangle([xMin-USER_CAR_LENGTH+self.xRange[0], self.lineY[0]],
                                      xMax+self.xRange[1]-(xMin-USER_CAR_LENGTH+self.xRange[0]), ROAD_LINE_WIDTH, 
                                      ec='b', fc='b')
        self.lines[3] = plt.Rectangle([xMin-USER_CAR_LENGTH+self.xRange[0], self.lineY[3]],
                                      xMax+self.xRange[1]-(xMin-USER_CAR_LENGTH+self.xRange[0]), ROAD_LINE_WIDTH, 
                                      ec='b', fc='b')
        self.axes.add_patch(self.lines[0])
        self.axes.add_patch(self.lines[3])

        self.car = plt.Rectangle((0, 0), USER_CAR_LENGTH, USER_CAR_WIDTH, fc='r')
        self.axes.add_patch(self.car)

    def updateCars(self, c_pos, sc_infoList):
        self.car.set_xy((c_pos[0]-USER_CAR_LENGTH, c_pos[1]-USER_CAR_WIDTH/2))

        for sc in self.scList:
            sc.remove()

        self.scList = []
        for x, y, h, w in sc_infoList:
            if self.xRange[0] <= x-c_pos[0] and x-c_pos[0] <= self.xRange[1]:
                rect = plt.Rectangle((x-h, y-w/2), h, w, fc='k')
                self.scList.append(rect)
                self.axes.add_patch(rect)

        while (len(self.lines[1]) > 0 and 
                self.lines[1][0].get_xy()[0] < c_pos[0]-USER_CAR_LENGTH/2+self.xRange[0]-ROAD_LINE_BLOCK):
            self.lines[1][0].remove()
            self.lines[1].popleft()
            self.lines[2][0].remove()
            self.lines[2].popleft()

        while (len(self.lines[1]) > 0 and 
                self.lines[1][-1].get_xy()[0] > c_pos[0]-USER_CAR_LENGTH/2+self.xRange[1]):
            self.lines[1][-1].remove()
            self.lines[1].pop()
            self.lines[2][-1].remove()
            self.lines[2].pop()

        if len(self.lines[1]) == 0:
            self.lines[1].append(plt.Rectangle([math.floor((c_pos[0]-USER_CAR_LENGTH/2+self.xRange[0])/ROAD_LINE_BLOCK), 
                self.lineY[1]+ROAD_LINE_WIDTH/2], ROAD_LINE_FILLED, ROAD_LINE_WIDTH, ec='b', fc='b'))
            self.axes.add_patch(self.lines[1][-1])
            self.lines[2].append(plt.Rectangle([math.floor((c_pos[0]-USER_CAR_LENGTH/2+self.xRange[0])/ROAD_LINE_BLOCK), 
                self.lineY[2]+ROAD_LINE_WIDTH/2], ROAD_LINE_FILLED, ROAD_LINE_WIDTH, ec='b', fc='b'))
            self.axes.add_patch(self.lines[2][-1])

        while (self.lines[1][-1].get_xy()[0] < c_pos[0]-USER_CAR_LENGTH/2+self.xRange[1]):
            lastPos = self.lines[1][-1].get_xy()
            self.lines[1].append(plt.Rectangle([lastPos[0]+ROAD_LINE_BLOCK, self.lineY[1]], 
                                 ROAD_LINE_FILLED, ROAD_LINE_WIDTH, ec='b', fc='b'))
            self.axes.add_patch(self.lines[1][-1])
            self.lines[2].append(plt.Rectangle([lastPos[0]+ROAD_LINE_BLOCK, self.lineY[2]], 
                                 ROAD_LINE_FILLED, ROAD_LINE_WIDTH, ec='b', fc='b'))
            self.axes.add_patch(self.lines[2][-1])
        
        while (self.lines[1][0].get_xy()[0] > c_pos[0]-USER_CAR_LENGTH/2+self.xRange[0]-ROAD_LINE_BLOCK):
            lastPos = self.lines[1][0].get_xy()
            self.lines[1].appendleft(plt.Rectangle([lastPos[0]-ROAD_LINE_BLOCK, self.lineY[1]],
                                     ROAD_LINE_FILLED, ROAD_LINE_WIDTH, ec='b', fc='b'))
            self.axes.add_patch(self.lines[1][0])
            self.lines[2].appendleft(plt.Rectangle([lastPos[0]-ROAD_LINE_BLOCK, self.lineY[2]],
                                     ROAD_LINE_FILLED, ROAD_LINE_WIDTH, ec='b', fc='b'))
            self.axes.add_patch(self.lines[2][0])

        self.boundaries = (c_pos[0]-USER_CAR_LENGTH/2+self.xRange[0], 
                           c_pos[0]-USER_CAR_LENGTH/2+self.xRange[1],
                           self.boundaries[2], self.boundaries[3])

        self.axes.axis(self.boundaries)
        self.draw()



''' statistical figures '''
class StatCanvas(FigureCanvas):
    def __init__(self, parent=None, dpi=300):
        self.xRange = 30 # 30 sec
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
        self.fig.patch.set_alpha(0.0)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Fixed)
        FigureCanvas.updateGeometry(self)

        self.axes.tick_params(left='on', right='on', labelleft='on', labelbottom='off', labelright='on')
        self.fig.subplots_adjust(left=0.23, right=0.95, bottom=0.03, top=0.92)

    def drawBackground(self, vList, tList, yLabel, title, yRange=None, yTicks=None, 
                       labelbottom=None, margin=None, mode=0, *args, **kw):
        self.axes.set_ylabel(yLabel, rotation=0, va='center', ha='center', labelpad=75, weight='normal')
        if mode == 0:
            self.axes.plot(tList, vList, *args, **kw)
        else:
            self.axes.step(tList, vList, *args, **kw)
        if yRange != None:
            self.axes.set_ylim(yRange)
        if yTicks != None:
            plt.yticks(yTicks[0], yTicks[1], rotation='horizontal', weight='normal')
        if labelbottom != None:
            self.axes.tick_params(labelbottom=labelbottom)
            self.axes.set_xlabel('Time (s)')
        if margin != None:
            self.fig.subplots_adjust(bottom=margin[0], top=1-margin[1])
        self.draw()

    def renewBackground(self, vList, tList, mode=0, *args, **kw):
        self.axes.lines[0].remove()
        if mode == 0:
            self.axes.plot(tList, vList, *args, **kw)
        else:
            self.axes.step(tList, vList, *args, **kw)

    def updateStat(self, currentTime):
        self.axes.set_xlim([currentTime - self.xRange, currentTime])
        self.draw()



def _invert(x, limits):
    """inverts a value x on a scale from
    limits[0] to limits[1]"""
    return limits[1] - (x - limits[0])

def _scale_data(data, ranges):
    """scales data[1:] to ranges[0],
    inverts if the scale is reversed"""
    for d, (y1, y2) in zip(data[1:], ranges[1:]): assert (y1 <= d <= y2) or (y2 <= d <= y1)
    x1, x2 = ranges[0]
    d = data[0]
    if x1 > x2:
        d = _invert(d, (x1, x2))
        x1, x2 = x2, x1
    sdata = [d]
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        if y1 > y2:
            d = _invert(d, (y1, y2))
            y1, y2 = y2, y1
        sdata.append((d-y1) / (y2-y1) * (x2 - x1) + x1)
    return sdata

class ComplexRadar():
    def __init__(self, fig, variables, ranges, n_ordinate_levels=5):
        angles = np.arange(0, 360, 360./len(variables))

        self.axes = [fig.add_axes([0.10,0.15,0.80,0.80], polar=True, label = "axes{}".format(i)) 
                     for i in range(len(variables))]
        l, text = self.axes[0].set_thetagrids(angles, labels=variables, ha='center', va='center', weight='normal')
        [txt.set_rotation(angle-90) for txt, angle in zip(text, angles)]
        for ax in self.axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)
        for i, ax in enumerate(self.axes):
            grid = np.linspace(*ranges[i], num=n_ordinate_levels)
            gridlabel = ["{}".format(round(x,2)) for x in grid]
            if ranges[i][0] > ranges[i][1]: grid = grid[::-1] # hack to invert grid; gridlabels aren't reversed
            gridlabel[0] = "" # clean up origin
            ax.set_rgrids(grid, labels=gridlabel, angle=angles[i], size='x-small')
            #ax.spines["polar"].set_visible(False)
            ax.set_ylim(*ranges[i])
        # variables for plotting
        self.angle = np.deg2rad(np.r_[angles, angles[0]])
        self.ranges = ranges
        rLine = mlines.Line2D([], [], color='r', label='All Driver Average Behavior')
        gLine = mlines.Line2D([], [], color='g', label='Driver Long-term Behavior')
        bLine = mlines.Line2D([], [], color='b', label='Driver Short-term Behavior')
        self.axes[0].legend(handles=[rLine, gLine, bLine], loc=8, mode='expand', shadow=True,
                            bbox_to_anchor=(0, -0.35, 1, 0.102))

    def clear(self, limit):
        for line in self.axes[0].lines[limit:]:
            line.remove()
        for patch in self.axes[0].patches[limit:]:
            patch.remove()

    def plot(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.axes[0].plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

    def fill(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.axes[0].fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)



''' radar figure '''
class RadarCanvas(FigureCanvas):
    def __init__(self, parent=None, dpi=300):
        self.fig = plt.figure(figsize=(6, 6))
        self.fig.patch.set_alpha(0.0)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Fixed)
        FigureCanvas.updateGeometry(self)

        self.fig.subplots_adjust(left=0.2, right=1.0, bottom=0.0, top=1.0)

    def drawBackground(self, meanData, longData, spokeLabels, ranges):
        self.radar = ComplexRadar(self.fig, spokeLabels, ranges)
        self.radar.plot(meanData, color='r')
        self.radar.fill(meanData, alpha=0.2, color='r')
        self.radar.plot(longData, color='g')
        self.radar.fill(longData, alpha=0.2, color='g')
        self.draw()

    def renewBackground(self, longData):
        self.radar.clear(1)
        self.radar.plot(longData, color='g')
        self.radar.fill(longData, alpha=0.2, color='g')
        self.draw()

    def updateRadar(self, data):
        self.radar.clear(2)
        self.radar.plot(data, color='b')
        self.radar.fill(data, alpha=0.2, color='b')
        self.draw()



''' main application '''
class MainApplication(QtGui.QMainWindow):
    def __init__(self):
        desktop = QtGui.QDesktopWidget()
        self.screen_size = QtCore.QRectF(desktop.screenGeometry(desktop.primaryScreen()))

        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('ITS Data Analysis Demo')
#        self.setStyleSheet('background-color: darkgray')
        self.setStyleSheet('background-color: rgb(240, 240, 250)')

        self.predictionSet = pd.read_csv('../fts/LOO_prediction.csv')
        for name in PRED_TARGETS:
            self.predictionSet[name] = self.predictionSet[name].apply(lambda x: 0 if x < 2 else 1)
            

        radarStat = pd.read_csv('../fts/radarStat.csv')
        self.radarStat = radarStat.iloc[range(48*2)]
        self.radarMean = radarStat[RADAR_TARGETS].iloc[-3]
        self.radarMaxl = radarStat[RADAR_TARGETS].iloc[-2]
        self.radarMinl = radarStat[RADAR_TARGETS].iloc[-1]

        defaultFile = '../dat/dat_0_0.csv'
        self.loadFile(defaultFile)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.currentTime = 0

        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        self.addPlayCanvas(layout)
        self.addStatCanvas(layout)

        centralWidget = QtGui.QWidget(self)
        centralWidget.setLayout(layout)
        centralWidget.setFocus()
        self.setCentralWidget(centralWidget)

        self.addMenu()
        self.addStatus()

    def addMenu(self):
        self.fileMenu = QtGui.QMenu('&File', self)
        self.fileMenu.addAction('&Load', self.loadMenu, QtCore.Qt.CTRL + QtCore.Qt.Key_F)
        self.fileMenu.addAction('&Quit', self.quitMenu, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.fileMenu)

    def addStatus(self):
        self.statusBar().showMessage('System Initialized Finished!')

    def addPlayCanvas(self, layout):
        self.carCanvas = CarCanvas(self, dpi=300)
        self.carCanvas.setFixedWidth(self.screen_size.width())
        self.carCanvas.setFixedHeight(135)

        self.carCanvas.drawBackground(min(self.data['X']), max(self.data['X']))
        self.carCanvas.updateCars([self.data['X'].iloc[self.frame], self.data['Y'].iloc[self.frame]],
                                  self.getSumoCarInfo(self.data['SumoCars'].iloc[self.frame]))

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setStyleSheet(SLIDER_STYLE)
        self.slider.setMinimum(0)
        self.slider.setMaximum(300)
        self.slider.sliderReleased.connect(self.timeControl)

        backwardButton = QtGui.QPushButton('')
        backwardButton.setIcon(QtGui.QIcon('../img/backward.png'))
        backwardButton.setIconSize(QtCore.QSize(30, 30))
        backwardButton.setStyleSheet("background-color: rgba(255, 255, 255, 1.0)")
        backwardButton.setCheckable(False)
        backwardButton.clicked.connect(self.backward)

        self.pauseButton = QtGui.QPushButton('')
        self.pauseButton.setIcon(QtGui.QIcon('../img/play.png'))
        self.pauseButton.setIconSize(QtCore.QSize(30, 30))
        self.pauseButton.setStyleSheet("background-color: rgba(255, 255, 255, 1.0)")
        self.pauseButton.setCheckable(True)
        self.pauseButton.clicked.connect(self.playControl)

        fowardButton = QtGui.QPushButton('')
        fowardButton.setIcon(QtGui.QIcon('../img/foward.png'))
        fowardButton.setIconSize(QtCore.QSize(30, 30))
        fowardButton.setStyleSheet("background-color: rgba(255, 255, 255, 1.0)")
        fowardButton.setCheckable(False)
        fowardButton.clicked.connect(self.foward)

        controller =  QtGui.QHBoxLayout() 
        controller.setAlignment(QtCore.Qt.AlignTop)
        controller.addWidget(self.slider)
        controller.addWidget(backwardButton)
        controller.addWidget(self.pauseButton)
        controller.addWidget(fowardButton)

        playLayout = QtGui.QVBoxLayout()
        playLayout.setContentsMargins(0,0,0,0)
        playLayout.addWidget(self.carCanvas)
        playLayout.addLayout(controller)
        layout.addLayout(playLayout)

    def addStatCanvas(self, layout):
        self.velCanvas = StatCanvas(self, dpi=300)
        self.velCanvas.drawBackground(self.data['Velocity'], self.data['Time'], 'Velocity (m/s)', 'Velocity', [-2.5, 32.5], margin=[0.03,0.15])
        self.velCanvas.updateStat(self.currentTime)
        self.velCanvas.setFixedWidth(self.screen_size.width()*0.6)
        self.velCanvas.setFixedHeight(self.screen_size.height()*0.15)

        self.frontCanvas = StatCanvas(self, dpi=300)
        self.frontCanvas.drawBackground(self.data['Dist to Front'], self.data['Time'], 'Front Dist (m)', 'Distance to Front', [-20,220], [range(0, 240, 40), range(0, 240, 40)], margin=[0.03, 0.03])
        self.frontCanvas.updateStat(self.currentTime)
        self.frontCanvas.setFixedWidth(self.screen_size.width()*0.6)
        self.frontCanvas.setFixedHeight(self.screen_size.height()*0.15)

        self.laneCanvas = StatCanvas(self, dpi=300)
        self.laneCanvas.drawBackground(self.data['Current Lane'], self.data['Time'], 'Lane (#)', 'Current Lane', [-0.6,2.5], [range(3), ['rhs', 'mhs', 'lhs']], labelbottom='on', margin=[0.23, 0.06])
        self.laneCanvas.updateStat(self.currentTime)
        self.laneCanvas.setFixedWidth(self.screen_size.width()*0.6)
        self.laneCanvas.setFixedHeight(self.screen_size.height()*0.1)

        self.radarCanvas = RadarCanvas(self, dpi=300) 
        self.radarCanvas.drawBackground(self.radarMean, self.ltBehavior, RADAR_LABELS, 
                                        [(self.radarMinl['Velocity'], self.radarMaxl['Velocity'])]
                                        + zip(self.radarMaxl[DIST_TARGETS], self.radarMinl[DIST_TARGETS]))
        self.radarCanvas.updateRadar(self.data[RADAR_TARGETS].iloc[self.frame])
        self.radarCanvas.setFixedWidth(self.screen_size.width()*0.35)
        self.radarCanvas.setFixedHeight(self.screen_size.height()*0.75)

        ltLayout = QtGui.QVBoxLayout()
        ltLayout.setSpacing(0);
        ltLayout.addWidget(self.velCanvas)
        ltLayout.addWidget(self.frontCanvas)
        ltLayout.addWidget(self.laneCanvas)

        lbLayout = QtGui.QVBoxLayout()
        lbLayout.setSpacing(0);

        t_stamp = self.prediction['st_t_stamp'].tolist()
        maxList = [0 for i in xrange(len(t_stamp))]
        self.predCanvasSet = []
        first=True
        for tar, name in zip(PRED_TARGETS, PRED_LABELS):
            results = self.prediction[tar].tolist()
            maxList = [max(m, v) for m, v in zip(maxList, results)]
            predCanvas = StatCanvas(self, dpi=300)
            predCanvas.setFixedWidth(self.screen_size.width()*0.6)
            if first:
                predCanvas.drawBackground(results, t_stamp, name, name, [-0.6, 1.5], [range(2), ['off', 'on']], margin=[0.11,0.40], mode=1, color='b')
                predCanvas.setFixedHeight(self.screen_size.height()*0.06)
                first=False
            else:
                predCanvas.drawBackground(results, t_stamp, name, name, [-0.6, 1.5], [range(2), ['off', 'on']], margin=[0.11,0.11], mode=1, color='b')
                predCanvas.setFixedHeight(self.screen_size.height()*0.05)
            predCanvas.updateStat(self.currentTime)
            self.predCanvasSet.append(predCanvas)
            lbLayout.addWidget(predCanvas)

        self.hazardCanvas = StatCanvas(self, dpi=300)
        self.hazardCanvas.drawBackground(maxList, t_stamp, 'Potential danger', 'Potential danger', [-0.6, 1.5], [range(2), ['off', 'on']], labelbottom='on', margin=[0.35,0.11], mode=1, color='r')
        self.hazardCanvas.updateStat(self.currentTime)
        self.hazardCanvas.setFixedWidth(self.screen_size.width()*0.6)
        self.hazardCanvas.setFixedHeight(self.screen_size.height()*0.07)
        lbLayout.addWidget(self.hazardCanvas)

        leftLayout = QtGui.QVBoxLayout()
        leftLayout.addLayout(ltLayout)
        leftLayout.addLayout(lbLayout)

        rightLayout = QtGui.QVBoxLayout()
        rightLayout.addWidget(self.radarCanvas)

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        layout.addLayout(mainLayout)

    def playControl(self):
        if self.pauseButton.isChecked(): # from play to pause
            self.pauseButton.setIcon(QtGui.QIcon('../img/pause.png'))
            self.timer.start(TIME_OUT)
            self.isPaused = False
        else: # from pause to play
            self.pauseButton.setIcon(QtGui.QIcon('../img/play.png'))
            self.timer.stop()
            self.isPaused = True
        self.updateStatus()

    def foward(self):
        self.frame = min(self.frame + 5, FRAME_MAX_LIMIT)
        self.update(update=False)

    def backward(self):
        self.frame = max(self.frame - 5, FRAME_MIN_LIMIT)
        self.update(update=False)
        
    def timeControl(self):
        value = self.slider.value()
        self.frame = self.data[self.data['Time'] > value - 0.01].iloc[0].name
        self.update()

    def loadFile(self, fileName):
        info = open(fileName).readline().strip().split(',')
        self.ts = float(info[0])
        self.userID = int(info[1])
        self.userMode = int(info[2])
        self.data = pd.read_csv(fileName, header=1, sep=',')
        self.frame = 0
        self.isPaused = True

        self.prediction = self.predictionSet[(self.predictionSet['User']==float(self.userID)) &
                                             (self.predictionSet['Scenario']==float(self.userMode))]
        self.ltBehavior = self.radarStat[(self.radarStat['User']==float(self.userID)) &
                                         (self.radarStat['Scenario']==float(self.userMode))][RADAR_TARGETS].iloc[0]
            
        for name in DIST_TARGETS:
            self.data[name] = self.data[name].apply(lambda x: x if x <= 200 and x >= 0 else 200)

    def loadMenu(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,caption='Load File',directory='../dat',filter='dat*.csv')
        self.loadFile(str(fileName))
        self.radarCanvas.renewBackground(self.ltBehavior)

        t_stamp = self.prediction['st_t_stamp'].tolist()
        maxList = [0 for i in xrange(len(t_stamp))]
        for tar, name, predCanvas in zip(PRED_TARGETS, PRED_LABELS, self.predCanvasSet):
            results = self.prediction[tar].tolist()
            maxList = [max(m, v) for m, v in zip(maxList, results)]
            predCanvas.renewBackground(results, t_stamp, 'b')
        self.hazardCanvas.renewBackground(maxList, t_stamp, color='r')

        self.update(update=False)

    def quitMenu(self):
        self.close()

    def getSumoCarInfo(self, info):
        posList = info.split(';')
        ret = []
        for pos in posList:
            ret.append(map(float, pos.split('_')))
        return ret

    def update(self, update=True):
        if update:        
            self.frame += 1
        self.currentTime = self.data['Time'].iloc[self.frame]
        self.slider.setValue(self.currentTime)

        if self.currentTime > TIME_MAX_LIMIT:
            self.timer.stop()
            self.pauseButton.click() # same as pause
        else:
            self.carCanvas.updateCars([self.data['X'].iloc[self.frame], self.data['Y'].iloc[self.frame]],
                                      self.getSumoCarInfo(self.data['SumoCars'].iloc[self.frame]))
        if self.frame % 5 == 0 or update == False:
            self.velCanvas.updateStat(self.currentTime)
        if self.frame % 5 == 1 or update == False:
            self.frontCanvas.updateStat(self.currentTime)
        if self.frame % 5 == 2 or update == False:
            self.laneCanvas.updateStat(self.currentTime)
        if self.frame % 5 == 3 or update == False:
            self.radarCanvas.updateRadar(self.data[RADAR_TARGETS].iloc[self.frame])
        if self.frame % 5 == 4 or update == False:
            self.hazardCanvas.updateStat(self.currentTime)
            for predCanvas in self.predCanvasSet:
                predCanvas.updateStat(self.currentTime)

        print self.frame, self.currentTime # for debugging

        self.updateStatus()

    def updateStatus(self):
        if self.userID <= 10:
            msg = ' '.join(['User', str(self.userID), ' - ', 'Normal' if self.userMode == 0 else 'Aggressive',
                            'Mode', ' | ', 'Time', ':', str(self.currentTime), 's'])
        else:
            msg = ' '.join(['User', str(self.userID), ' - ', 'Normal' if self.userMode == 0 else 'Giraffed',
                            'Mode', ' | ', 'Time', ':', str(self.currentTime), 's'])
        if self.isPaused == True:
            msg += '  (Paused)'
        self.statusBar().showMessage(msg)



''' main '''
def main():
    qApp = QtGui.QApplication(sys.argv)
    mApp = MainApplication()
    mApp.showFullScreen()
    sys.exit(qApp.exec_())



if __name__ == '__main__':
    main()
