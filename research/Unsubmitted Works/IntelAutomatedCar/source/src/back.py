'''
import all needed packages
'''
import os
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar



'''
default settings
'''
defaultFile = '../dat/dat_0_0.csv'

info = open(defaultFile).readline().strip()
ts, userID, userMode = map(float, info.split(','))

ins_data = pd.read_csv(data_file, header = 1, sep = ',') #???
ins_data['Current Lane'].unique() #???



'''
definitions
'''
COLOR_GREEN = 'rgba(50, 205, 50, 200)'
COLOR_YELLOW = 'rgba(255, 215, 0, 200)'
COLOR_RED = 'rgba(255, 69, 0, 200)'

USER_CAR_LENGTH = 3.8
USER_CAR_WIDTH = 1.4


# ## Helper Functions

# In[4]:

def remove_mul(data, elems):
    res = data
    for k in elems:
        data.remove(k)
    return res


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, dpi=300):
        self.fig, self.axes = plt.subplots(nrows=1, ncols = 1)
        self.fig.tight_layout()
        # We want the axes cleared every time plot() is called
        self.axes.hold(True)


        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

    
class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2*np.pi*t)
        self.axes.plot(t, s)
    def update_figure(self, data):
        pass


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')
        
    def update_figure(self, data, title=None, ylim=None, ylabel=None, x=None, legend=True,*args, **kwargs):
        self.axes.clear()
        if x is not None:
            self.plot(x, data,'r')
            self.axes.set_xlim([x.min(),x.max()])
            self.axes.set_xlabel('Time (s)')
        else:
            self.plot(data.index,data,'r')
        if title:
            self.axes.set_title(title)
        if ylim:
            self.axes.set_ylim(ylim)
        if ylabel:
            self.axes.set_ylabel(ylabel)
        if legend:
            self.axes.legend()
        self.draw()

    def plot(self, x, data, *args, **kwargs):
        if type(data) is list:
            for d in data:
                self.axes.plot(x, d, label=d.name)
        else:
            self.axes.plot(x,data,'r', label=data.name)

        
class CarViewDynamic(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        ''' Default distance: 100m in front and 100m behind '''
        self.boundaries = (-100,100,-13,0.7)
        super(CarViewDynamic, self).__init__(*args, **kwargs)
        MyMplCanvas.setSizePolicy(self,
                                  QtGui.QSizePolicy.Fixed,
                                  QtGui.QSizePolicy.Fixed)
        self.axes.autoscale(enable=False)
        #self.axes.set_xlim([self.boundaries[0],self.boundaries[1]])
        #self.axes.set_ylim([self.boudaries[2],self.boundaries[3]])
        self.axes.axis(self.boundaries)
        #self.axes.axis('off')
        self.fig.subplots_adjust(left=0, right=1)
        self.scList = []
        #self.fig.tight_layout(pad=0, w_pad=0, h_pad=0)
    
    def compute_initial_figure(self):
        #add the lanes
        for y in [-12.3, 0]:
            self.axes.add_line(plt.Line2D([2*self.boundaries[0], 2*self.boundaries[1]], [y, y], ls='-'))
        for y in [-8.2, -4.1]:
            self.axes.add_line(plt.Line2D([2*self.boundaries[0], 2*self.boundaries[1]], [y, y], ls='--'))
        self.car = plt.Rectangle((-USER_CAR_LENGTH/2, -USER_CAR_WIDTH/2), USER_CAR_LENGTH, USER_CAR_WIDTH, fc='g')
        self.axes.add_patch(self.car)
        self.axes.tick_params(axis='y', left='off', right='off', labelleft='off', labelbottom='on')
        #self.axes.axis('off')
   
    def update_figure(self, c_pos, color, sc_infoList):
        # plot the car
        self.car.set_xy((-2, c_pos[1]-1))
        self.car.set_facecolor(color)
        self.draw()
        
        for sc in self.scList: # remove past sumocars
            sc.remove()
        self.scList = []
        for x, y, h, w in sc_infoList: # create current sumocars
            if abs(x - 2 - c_pos[0]) < 200:
                self.scList.append(plt.Rectangle((x-h/2-c_pos[0], y-w/2), h, w, fc='k'))
        for sc in self.scList: # addin created sumocars
            self.axes.add_patch(sc)
        
    def set_boundaries(self, y):
        self.boundaries = (-100-y, 100-y, -13, 0.7)
        self.axes.axis(self.boundaries)
        self.draw()
    


# ### Radar Plots

# In[7]:

from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection

def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = 2*np.pi * np.linspace(0, 1-1./num_vars, num_vars)
    # rotate theta such that the first axis is at the top
    theta += np.pi/2

    def draw_poly_patch(self):
        verts = unit_poly_verts(theta)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(theta * 180/np.pi, labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.

    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts

class MyRadarPlot(MyDynamicMplCanvas):
    def init(self, labels):
        N = len(labels)
        self.theta = radar_factory(N, frame='polygon')
        self.spoke_labels = labels
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(1, 1, 1, projection='radar')
        self.fig.tight_layout()
        self.axes.hold(True)
        self.colors = ['#F19C99', '#9AC7BF', 'b', 'm', 'y'] #TO DO : how to manage if there is more than 5 ? have a huge list of random colors to append ? There won't be many different colors anyway

        FigureCanvas.__init__(self, self.fig)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
    def reinit(self, labels):
        self.fig.delaxes(self.axes)
        N = len(labels)
        self.theta = radar_factory(N, frame='polygon')
        self.spoke_labels = labels
        self.axes = self.fig.add_subplot(1, 1, 1, projection='radar')
        self.axes.hold(True)
        
    def update_figure(self, data, title=None):
        self.axes.clear()
        for d, color in zip(data.index, self.colors):
            self.axes.plot(self.theta, data.loc[d], color=color,)
            self.axes.fill(self.theta, data.loc[d], facecolor=color, alpha=1.0)

        self.axes.set_ylim(0,100)
        
        self.axes.set_varlabels(self.spoke_labels)

        if title:
            self.axes.set_title(title)
            
        self.draw()


# ## Widgets (wrappers)

# ### Dynamic Widgets

# In[8]:

class MyGroupCheckBox(QtGui.QWidget):
    def __init__(self, name,*args, **kwargs):
        super(MyGroupCheckBox, self).__init__(*args, **kwargs)
        self.buttons = {}
        self.name = name
        self.mainLayout=QtGui.QVBoxLayout(self)
        
    def addButton(self,button, idbutton):
        self.buttons[idbutton] = button
    
    def setCheckeds(self, keys):
        for k in keys:
            self.buttons[k].setChecked(True)
            
    def checkedIds(self):
        res = []
        for idb,but in self.buttons.iteritems():
            if but.isChecked():
                res.append(idb)
        return res
    
    def button(id):
        return self.buttons[id]
    def setLayout(self):
        group = QtGui.QGroupBox(self.name)
        layout = QtGui.QGridLayout()
        positions = [(i,j) for i in range(len(self.buttons)/4+1) for j in range(4)]
        for (idb,but),p in zip(self.buttons.iteritems(),positions):
            lineLayout = QtGui.QHBoxLayout()
            lineLayout.addWidget(but)
            label = QtGui.QLabel(str(idb))
            label.setAlignment(QtCore.Qt.AlignLeft)
            lineLayout.addWidget(label)
            layout.addLayout(lineLayout,*p)
        group.setLayout(layout)
        self.mainLayout.addWidget(group)
        
class MyPlotOptionWidget(QtGui.QDialog):
    def __init__(self, linked, line):
        super(MyPlotOptionWidget,self).__init__(parent=linked)
        self.line = line
        self.linked = linked
        self.setWindowTitle("Options")
        self.mainLayout = QtGui.QVBoxLayout(self)
        self.addRename()
        self.addSpecific()
        self.addKeyChoice()
        self.addQuitAndCancel()
        
    def  addRename(self):
        nameLayout = QtGui.QHBoxLayout()
        nameLabel = QtGui.QLabel('Rename')
        self.nameEdit = QtGui.QLineEdit()
        self.nameEdit.setText(self.linked.name)
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameEdit)
        self.mainLayout.addLayout(nameLayout)

    def addTimeSpan(self):
        timeLayout = QtGui.QHBoxLayout()
        timeLabel = QtGui.QLabel('Choose Time Span')
        self.timeEdit = QtGui.QLineEdit()
        self.timeEdit.setText(str(self.linked.timespan))
        timeLayout.addWidget(timeLabel)
        timeLayout.addWidget(self.timeEdit)
        self.mainLayout.addLayout(timeLayout)
        
    def addSpecific(self):
        pass
   
    def addWindowSize(self):
        groupTime = QtGui.QGroupBox("Window Size")
        layoutTime = QtGui.QHBoxLayout()
        self.windowButtons = QtGui.QButtonGroup()
        for t in self.linked.possible_windows:
            newButton = QtGui.QRadioButton(str(t)+" s")
            self.windowButtons.addButton(newButton, t)
            layoutTime.addWidget(newButton)
        layoutTime.addStretch(1)
        groupTime.setLayout(layoutTime)
        self.windowButtons.button(int(self.linked.window_size)).setChecked(True)
        self.mainLayout.addWidget(groupTime)
        
    def addKeyChoice(self):
        pass
    
    def addSimpleKeyChoice(self):
        self.comboKey = QtGui.QComboBox()
        for k in self.linked.possible_keys:
            self.comboKey.addItem(k)
        self.comboKey.setCurrentIndex(self.linked.key_num)
        self.mainLayout.addWidget(self.comboKey)
    
    def addMultipleKeyChoice(self):
        self.comboKey = MyGroupCheckBox("Keys",parent=self)
        for k in self.linked.possible_keys:
            newCheck = QtGui.QCheckBox()
            self.comboKey.addButton(newCheck,k)
        self.comboKey.setCheckeds(self.linked.keys)
        self.comboKey.setLayout()
        self.mainLayout.addWidget(self.comboKey)
            
    def addRankorValueChoice(self):
        groupRoV = QtGui.QGroupBox("Type of Data")
        layoutRoV = QtGui.QHBoxLayout()
        self.rankorvalueButtons = QtGui.QButtonGroup()
        for i,t in enumerate(['Rank', 'Value']):
            newButton = QtGui.QRadioButton(t)
            self.rankorvalueButtons.addButton(newButton, i)
            layoutRoV.addWidget(newButton)
        layoutRoV.addStretch(1)
        groupRoV.setLayout(layoutRoV)
        if self.linked.mode == 'Value':
            self.rankorvalueButtons.button(1).setChecked(True)
        else:
            self.rankorvalueButtons.button(0).setChecked(True)

        self.mainLayout.addWidget(groupRoV)
            
    def addQuitAndCancel(self):
        last_line = QtGui.QHBoxLayout();
        cancel_b = QtGui.QPushButton("&Cancel")
        cancel_b.clicked.connect(self.close)
        conf_b = QtGui.QPushButton("&OK")
        conf_b.clicked.connect(self.okpushed)
        last_line.addWidget(cancel_b)
        last_line.addWidget(conf_b)
        self.mainLayout.addLayout(last_line)
        self.setLayout(self.mainLayout)

    def key_update(self):
        pass
    
    def timespan_update(self):
        self.linked.timespan = int(self.timeEdit.text())

    
    def windowsize_update(self):
        self.linked.window_size = self.windowButtons.checkedId()

    def rankorvalue_update(self):
        if self.rankorvalueButtons.checkedId() == 0:
            self.linked.mode = 'Rank'
        else:
            self.linked.mode = 'Value'
    
    def update_Specific(self):
        pass

    def okpushed(self):
        self.line.label.setText(self.nameEdit.text())
        self.linked.name = self.nameEdit.text()
        self.key_update()
        self.update_Specific()
        self.close()        
    
class MyInstantPlotOptionWidget(MyPlotOptionWidget):
    def addSpecific(self):
        self.addTimeSpan()

    
    def addKeyChoice(self):
        self.addSimpleKeyChoice()
    
    def key_update(self):
        self.linked.key_num = self.comboKey.currentIndex()

    def update_Specific(self):
        self.timespan_update()



class MyWindowPlotOptionWidget(MyPlotOptionWidget):
    def addKeyChoice(self):
        self.addMultipleKeyChoice()
        
    def addSpecific(self):
        self.addTimeSpan()
        self.addWindowSize()
        self.addRankorValueChoice()

        
    def key_update(self):
        self.linked.keys = self.comboKey.checkedIds()
        
    def update_Specific(self):
        self.timespan_update()
        self.windowsize_update()
        self.rankorvalue_update()

class MyRadarPlotOptionWidget(MyPlotOptionWidget):
    def addKeyChoice(self):
        self.addMultipleKeyChoice()
        self.addRankorValueChoice()
    
    def addSpecific(self):
        self.addWindowSize()
        
    def key_update(self):
        self.linked.keys = self.comboKey.checkedIds()
        
    def update_Specific(self):
        self.windowsize_update()
        self.rankorvalue_update()
        self.linked.reinit()

    
class MyDynamicWidget(QtGui.QWidget):
    def __init__(self, name=None, *args, **kwargs):
        super(MyDynamicWidget, self).__init__(*args, **kwargs)
        self.name = name

    def update_item(self,data):
        pass
    
class MyElementWidget(QtGui.QLabel):
    def __init__(self, name=None, *args, **kwargs):
        super(MyElementWidget, self).__init__(*args, **kwargs)
        self.setText(name)
        self.setFixedHeight(30)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.setFrameShape(QtGui.QFrame.Box);
        self.setFrameShadow(QtGui.QFrame.Raised);
    
    def update_item(self, st):
        if st == 0:
            self.setStyleSheet('background-color: ' + COLOR_GREEN + ';')
        elif st == 1:
            self.setStyleSheet('background-color: ' + COLOR_YELLOW + ';')
        else:
            self.setStyleSheet('background-color: ' + COLOR_RED + ';')

            
class MyWarningWidget(MyDynamicWidget):
    def __init__(self,*args, **kwargs):
        super(MyWarningWidget, self).__init__(*args, **kwargs)
        self.layout = QtGui.QVBoxLayout(self)

        self.warnText = MyElementWidget('Warnings')
        self.warnings = [MyElementWidget(m) for m in ['Speed', 'Speed Control', 'Aggressive Lane Switch', 'Dangerous Distance']]
        self.events = [MyElementWidget(m) for m in ['Collisions', 'Overspeeding', 'Too Close', 'Lane Switch to Left', 'Lane Switch to Right']]
        
        ''' put widgets on layout '''
        self.layout.addItem(QtGui.QSpacerItem(10, 10, vPolicy=QtGui.QSizePolicy.Expanding)) # space
        self.layout.addWidget(self.warnText) # warning text
        for e in self.warnings: # four main warnings
            self.layout.addWidget(e)
        self.layout.addItem(QtGui.QSpacerItem(10, 10, vPolicy=QtGui.QSizePolicy.Expanding)) # space
        for e in self.events: # several predicted events
            self.layout.addWidget(e)
        self.layout.addItem(QtGui.QSpacerItem(10, 10, vPolicy=QtGui.QSizePolicy.Expanding)) # space
            
    def update_item(self, update_warnings, update_events):
        self.warnText.update_item(max(update_warnings))
        for w, uw in zip(self.warnings, update_warnings):
            w.update_item(uw)
        for e, ue in zip(self.events, update_events):
            e.update_item(ue)
        
        
class MyDynamicPlotWidget(MyDynamicMplCanvas):
    def __init__(self, keys=[], timespan=0,name = None, possible_windows=None,*args, **kwargs):
        super(MyDynamicPlotWidget, self).__init__(*args, **kwargs)
        self.name = name
        self.timespan = timespan
        self.axes.set_title(self.name)
        self.possible_keys = keys
        self.possible_windows = possible_windows
        
    def update_item(self,*args, **kwargs):
        pass
    def optionMenu(self, line):
        pass

        
class MyInstantPlotWidget(MyDynamicPlotWidget):
    def __init__(self, *args, **kwargs):
        super(MyInstantPlotWidget, self).__init__(*args, **kwargs)
        self.axes.autoscale(enable=False)
        if len(self.possible_keys)==0:
            self.key_num='No Key'
        else:
            self.key_num = 0
        
    def update_item(self, time, data_ins=None, *args, **kwargs):
        self.key = self.possible_keys[self.key_num]
        recent = ins_data[(ins_data['Time'] < time) & (ins_data['Time'] > time - self.timespan)]        
        self.update_figure(recent[self.key], x=recent['Time'], ylim=[ins_data[self.key].min(),ins_data[self.key].max()], title=self.name, ylabel=self.key)

    def optionMenu(self, line):
        menu = MyInstantPlotOptionWidget(self, line)
        menu.show()
    
class MyWindowPlotWidget(MyDynamicPlotWidget):
    def __init__(self, *args, **kwargs):
        super(MyWindowPlotWidget, self).__init__(*args, **kwargs)
        self.axes.autoscale(enable=False)
        if len(self.possible_keys)==0:
            self.keys='No Key'
        else:
            self.keys = self.possible_keys[0:3]
            
        self.window_size = self.timespan
        self.timespan = self.timespan * 2
        self.mode = 'Value'
        
    def update_item(self, time, data_win_p=None, data_win_v = None, *args, **kwargs):
        if self.mode == 'Value':
            data = data_win_v
        else:
            data = data_win_p
        data = data[data['Duration']==self.window_size]
        end = data['Date Begin'] + self.window_size
        recent = data[(end < time) & (end > time - self.timespan)]
        if len(recent)==0:
            recent = data.iloc[0]
            double = data.iloc[0].copy()
            double['Date Begin'] = 0
            recent = pd.DataFrame([recent,double], index=[1,0])

        datas_plot = []
        for l in self.keys:
            datas_plot.append(recent[l])
        

        
        self.update_figure(datas_plot, x=(recent['Date Begin']+self.window_size), ylim=[0,100], ylabel='rank (%)',title=self.name)

    def optionMenu(self, line):
        menu = MyWindowPlotOptionWidget(self, line)
        menu.show()

class MyRadarPlotWidget(MyRadarPlot):
    def __init__(self, keys=[], timespan=0,name = None, possible_windows=None,*args, **kwargs):
        super(MyRadarPlotWidget, self).__init__(*args, **kwargs)
        self.name = name
        self.timespan = timespan
        self.axes.set_title(self.name)
        self.possible_keys = keys
        self.possible_windows = possible_windows

        if len(self.possible_keys)==0:
            self.keys='No Key'
        else:
            self.keys = self.possible_keys[0:5]
        self.window_size = self.timespan
        self.mode = 'Rank'

        self.init(self.keys)
        
    def reinit(self):
        super(MyRadarPlotWidget, self).reinit(self.keys)
        
    def update_item(self, time, data_win_p=None, data_win_v = None, *args, **kwargs):
        if self.mode == 'Value':
            data = data_win_v
        else:
            data = data_win_p
        data = data[data['Duration']==self.window_size]
        end = data['Date Begin'] + self.window_size
        recent = data[(end < time)]
        if len(recent)==0:
            recent=data.iloc[[0]]
        else:
            recent=recent.iloc[[-1]]

        self.update_figure(recent[self.keys],title=self.name)

    def optionMenu(self, line):
        menu = MyRadarPlotOptionWidget(self, line)
        menu.show()



# ### Multiple Widgets

# In[9]:

class MyLineOption(QtGui.QFrame):
    def __init__(self, linked):
        super(MyLineOption, self).__init__()
        
        self.setFrameStyle(0)
        
        self.linked = linked
       
        
        self.layout = QtGui.QHBoxLayout(self)
        
        self.checkbox = QtGui.QCheckBox()
        self.layout.addWidget(self.checkbox)    
        
        self.label = QtGui.QLabel()
        self.label.setText(linked.name)
        self.layout.addWidget(self.label)
        

        
        self.option_b = QtGui.QPushButton("Options")
        self.option_b.clicked.connect(self.optionMenu)
        self.layout.addWidget(self.option_b)
        
        
    def isChecked(self):
        return self.checkbox.isChecked()
        
    def optionMenu(self):
        self.linked.optionMenu(self)
    
        
        
class MyAddMenu(QtGui.QDialog):
    def __init__(self, linked):
        super(MyAddMenu,self).__init__(parent=linked)
        self.linked = linked
        self.setWindowTitle("Add New Plot")
        self.mainLayout = QtGui.QVBoxLayout(self)
    
        # Name
        nameLayout = QtGui.QHBoxLayout()
        nameLabel = QtGui.QLabel('Name')
        self.nameEdit = QtGui.QLineEdit()
        self.nameEdit.setText("NewPlot")
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameEdit)
        self.mainLayout.addLayout(nameLayout)
        # Type
        groupType = QtGui.QGroupBox("Plot Type")
        layoutType = QtGui.QHBoxLayout()
        self.typeButtons = QtGui.QButtonGroup()
        self.types = ['Instant', 'Window', 'Radar']
        for i,t in enumerate(self.types):
            newButton = QtGui.QRadioButton(t)
            self.typeButtons.addButton(newButton, i)
            layoutType.addWidget(newButton)
        layoutType.addStretch(1)
        groupType.setLayout(layoutType)
        self.mainLayout.addWidget(groupType)

        # Time Span
        groupTime = QtGui.QGroupBox("Time span")
        layoutTime = QtGui.QHBoxLayout()
        self.timeButtons = QtGui.QButtonGroup()
        for t in self.linked.linked.times:
            newButton = QtGui.QRadioButton(str(t)+" s")
            self.timeButtons.addButton(newButton, t)
            layoutTime.addWidget(newButton)
        layoutTime.addStretch(1)
        groupTime.setLayout(layoutTime)
            
        self.mainLayout.addWidget(groupTime)
        
        last_line = QtGui.QHBoxLayout()
        
        add_b = QtGui.QPushButton("&Add")
        add_b.clicked.connect(self.addPushed)
        
        quit_b = QtGui.QPushButton("&Quit")
        quit_b.clicked.connect(self.close)
        
        last_line.addWidget(add_b)
        last_line.addWidget(quit_b)
        
        self.mainLayout.addLayout(last_line)
        
        self.setLayout(self.mainLayout)
    
    def addPushed(self):
        if (self.timeButtons.checkedId()<0) or (self.typeButtons.checkedId()<0):
            return
        self.linked.linked.add_item(self.nameEdit.text(), self.timeButtons.checkedId(), self.types[self.typeButtons.checkedId()])
        self.linked.new_line()
        self.close()
        
class MyMultipleWidgetOption(QtGui.QDialog):
    def __init__(self, linked):
        super(MyMultipleWidgetOption, self).__init__(parent=linked)
        self.initOptions(linked)
    def initOptions(self,linked):
        self.linked = linked
        self.setWindowTitle("Settings")
        self.mainLayout = QtGui.QVBoxLayout(self)
        
        self.linesLayout = QtGui.QVBoxLayout()
        self.lines = []
        for i in range(linked.items.count()):
            new_line = MyLineOption(linked.items.widget(i))
            self.lines.append(new_line)
            self.linesLayout.addWidget(new_line)
        self.mainLayout.addLayout(self.linesLayout)
        #Buttons line
        buttonsLayout = QtGui.QHBoxLayout()
        swap_b = QtGui.QPushButton("Swap")
        swap_b.clicked.connect(self.swap)
        del_b = QtGui.QPushButton("Delete")
        del_b.clicked.connect(self.remove)
        buttonsLayout.addWidget(swap_b)
        buttonsLayout.addWidget(del_b)
        
        self.mainLayout.addLayout(buttonsLayout)
        
        secondButtonsLayout = QtGui.QHBoxLayout()
        self.add_b = QtGui.QPushButton("&New Plot")
        self.add_b.clicked.connect(self.addMenu)
        self.quit_b = QtGui.QPushButton("&Quit")
        self.quit_b.clicked.connect(self.close)
        secondButtonsLayout.addWidget(self.add_b)
        secondButtonsLayout.addWidget(self.quit_b)
        self.mainLayout.addLayout(secondButtonsLayout)
    
        self.setLayout(self.mainLayout)
 
    def list_selected(self):
        selected = []
        for i in range(len(self.lines)):
            if self.lines[i].isChecked():
                selected.append(i)
                self.lines[i].checkbox.toggle()
        return selected
        
    def swap(self):
        selected = self.list_selected()
        if len(selected)<2:
            return
        first = self.lines[selected[0]]
        for i in range(1,len(selected)):
            self.lines[selected[i-1]] = self.lines[selected[i]]
        self.lines[selected[-1]] = first
        self.rearrange_lines()
        self.linked.swap(selected)
    
    def rearrange_lines(self):
        for iline in self.lines:
            self.linesLayout.removeWidget(iline)
            #iline.hide()

        for iline in self.lines:
            self.linesLayout.addWidget(iline)
            #iline.show()
    
    def new_line(self):
        new_line = MyLineOption(self.linked.items.widget(self.linked.items.count()-1))
        self.lines.append(new_line)
        self.linesLayout.addWidget(new_line)
    
    def remove(self):
        selected = self.list_selected()
        del_later = []
        for i in selected:
            to_remove = self.lines[i]
            to_remove.hide()
            self.linesLayout.removeWidget(to_remove)
            
            self.linked.remove(to_remove.linked)
            del_later.append(to_remove)

        for victim in del_later:
            self.lines.remove(victim)
            del victim.linked
            del victim
            
    def addMenu(self):
        window = MyAddMenu(self)
        window.show()

            


# In[ ]:

class MyMultipleWidget(QtGui.QWidget):
    def __init__(self, keys_ins=[], keys_win=[], times=None,*args, **kwargs):
        super(MyMultipleWidget, self).__init__(*args, **kwargs)
        #main layout
        self.keys_ins=keys_ins
        self.keys_win=keys_win
        self.times = times
        
        self.layout = QtGui.QVBoxLayout(self)
        self.addBar()
        self.mainLayout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.mainLayout)
        
        self.items = QtGui.QStackedWidget()        
        
        self.add_item('Test 1', 250, 'Radar')
#        self.add_item('Test 2', 200, 'Instant')
        
        self.items.setCurrentIndex(0)
        self.items.widget(0)
        self.mainLayout.addWidget(self.items)
                                  
    def addBar(self):
        barLayout = QtGui.QHBoxLayout()
        
        # Parameter Button
        param_b = QtGui.QPushButton("Set")
        param_b.clicked.connect(self.paramMenu)
        # Previous Button
        prev_b = QtGui.QPushButton("<<")
        prev_b.clicked.connect(self.prevPushed)
        # Next
        next_b = QtGui.QPushButton(">>")
        next_b.clicked.connect(self.nextPushed)
        
        barLayout.addWidget(param_b)
        barLayout.addWidget(prev_b)
        barLayout.addWidget(next_b)
        
        self.layout.addLayout(barLayout)
    

        
    def paramMenu(self):
        window = MyMultipleWidgetOption(self)
        window.show()
        
    def prevPushed(self):
        # TO DO : show the previous plot (self.current = self.current -1 mod nb_total)
        self.items.setCurrentIndex((self.items.currentIndex() - 1) % self.items.count()) 
    def nextPushed(self):
        #TO DO : advance to the next plot
        self.items.setCurrentIndex((self.items.currentIndex() + 1) % self.items.count()) 
    
    def add_item(self, name, timespan, kind):
        if kind=='Instant':
            self.items.addWidget(MyInstantPlotWidget(name=name,keys=self.keys_ins, timespan=timespan))
        elif kind=='Window':
            self.items.addWidget(MyWindowPlotWidget(name=name,keys=self.keys_win, timespan=timespan, possible_windows=self.times))
        elif kind=='Radar':
            self.items.addWidget(MyRadarPlotWidget(name=name,keys=self.keys_win, timespan=timespan, possible_windows=self.times))

            
    def update_view(self, data_ins, data_win_p, data_win_v, instant):
        if self.items.count() == 0:
            return
        self.items.currentWidget().update_item(instant, data_ins=data_ins, data_win_p=data_win_p, data_win_v=data_win_v)
        
    def swap(self, swap_list):
        first = self.items.widget(swap_list[0])
        self.items.removeWidget(first)

        for i in range(1,len(swap_list)):
            to_move = self.items.widget(swap_list[i]-1) #-1 because we removed one that is before and the index were updated (?)
            self.items.removeWidget(to_move)
            self.items.insertWidget(swap_list[i-1],to_move)
            
        self.items.insertWidget(swap_list[-1], first)
        
    def remove(self, widget):
        self.items.removeWidget(widget)        


# ## Main Application

# In[ ]:

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
                
        #load the data
        self.win_data_p = pd.read_csv('userpos.csv')
        self.win_data_v = pd.read_csv('valuepos.csv')
        self.times = self.win_data_p['Duration'].unique()
        
        self.prediction = pd.read_csv('../fts/LOO_prediction.csv')

        data_file = '../ndat/data_0_0.csv'
        self.load_data(data_file)

        #set the application
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("ITS Data Analysis Demo")
        self.makeMenu()
        self.main_widget = QtGui.QWidget(self)
        
        #set the layout of the application
        layout = QtGui.QVBoxLayout(self.main_widget)
        layout.setContentsMargins(0,0,0,0)

        self.addTimeControl(layout)
        self.addCarView(layout)
        self.addInfoView(layout)    
        self.setLayout(layout)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        
        #load the data
        data_file = '../ndat/data_47_0.csv'
        self.load_data(data_file)
        
        # timer starts
        self.frame = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1)
        
        # default warnings and predicted events
        self.update_warnings = [0, 0, 0, 0]
        self.update_events = [0, 0, 0, 0, 0]
        
        # settings and definitions for warnings
        self.warnings_details = {'Speeding':['Speed Average', 'High Speed Ratio'],
                                 'Speed Control':['Acceleration Average', 'Speed Variance'],
                                 'Dangerous Distance':['- Average Front Distance', 'Front Too Close Ratio', '- Average Overtake Space', 'Overtaking Too Close Ratio', '- Average Distance Before Lane Switch'],
                                 'Aggressive Lane Switch':['- Average Overtake Space', 'Overtaking Too Close Ratio', '- Average Distance Before Lane Switch', 'Lane Switch Frequency', 'Overtaking Frequency', 'Average Speed When Lane Switch']}
        self.warnings_threshold = [80, 90]
        self.warning_duration = 60
        
    def fileQuit(self):
        self.close()
    
    def loadMenu(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,caption='Open File',directory='../ndat',filter='data*.csv')
        self.load_data(str(fname))        
        self.update()
        
    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtGui.QMessageBox.about(self, "About",
""" Demonstration of the different models created for ITS Data Analysis.

It was created by Stan and Hao-En for the Intel-NTU CCC ITS Project (2015).

Inspired by "embedding_in_qt4.py example" (Copyright 2005 Florent Rougon, 2006 Darren Dale)
"""
)

    def load_data(self,data_file):
        line=open(data_file).readline().rstrip().split(",")
        timestamp = float(line[0])
        self.user_id = float(line[1])
        self.user_mode = float(line[2])
        self.ins_data = pd.read_csv(data_file, header = 1, sep = ',')
        self.frame = 0
        self.current_userpos = self.win_data_p[(self.win_data_p['User']==self.user_id)&(self.win_data_p['Scenario']==self.user_mode)]
        self.current_valuepos = self.win_data_v[(self.win_data_v['User']==self.user_id)&(self.win_data_v['Scenario']==self.user_mode)]
        self.current_prediction = self.prediction[(self.prediction['User']==self.user_id)&(self.prediction['Scenario']==self.user_mode)]

        ins_rem_key = ['Time', 'X', 'Y', 'Current Lane','Rotation X', 'Rotation Y', 'Lane Left', 'Lane Right', 'SumoCars']
        win_rem_key = ['Unnamed: 0', 'User', 'Duration', 'Scenario', 'Date Begin']
        keyz = list(self.ins_data)
        self.keys_ins = remove_mul(keyz, ins_rem_key)
        keyz = list(self.win_data_p)
        self.keys_win = remove_mul(keyz, win_rem_key)
                
    def makeMenu(self):
        self.file_menu = QtGui.QMenu('&File', self)

        self.file_menu.addAction('&Open', self.loadMenu, QtCore.Qt.CTRL + QtCore.Qt.Key_F)
        self.file_menu.addAction('&Quit', self.fileQuit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        
        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        
    def addTimeControl(self, layout):
        pause_b = QtGui.QPushButton("&Pause")
        pause_b.setCheckable(True)
        pause_b.clicked[bool].connect(self.pauseTime)
        self.isPaused = False
        
        self.sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld.setMinimum(0)
        self.sld.setMaximum(300)
        self.sld.valueChanged[int].connect(self.timeControl)

        controller =  QtGui.QHBoxLayout()
        controller.addWidget(pause_b)
        controller.addWidget(self.sld)
        
        layout.addLayout(controller)   

    def addCarView(self, layout):
        # Make the Widget
        carLayout = QtGui.QVBoxLayout()
        self.carView = CarViewDynamic(self, dpi=300)
        
        # make sure primary window size
        desktop = QtGui.QDesktopWidget()
        screen_size = QtCore.QRectF(desktop.screenGeometry(desktop.primaryScreen()))
        self.carView.setFixedWidth(screen_size.width())
        self.carView.setFixedHeight(75)
        
        pos_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        pos_slider.setMinimum(-99)
        pos_slider.setMaximum(99)
        pos_slider.valueChanged[int].connect(self.carView.set_boundaries)
        
        carLayout.addWidget(self.carView)
        carLayout.addWidget(pos_slider)
        layout.addLayout(carLayout)

    def addInfoView(self, layout):
        infoLayout = QtGui.QHBoxLayout()
        splitter = QtGui.QSplitter()
        self.addWarning(splitter)

        # Stats Plots
        self.addStats(splitter)
        infoLayout.addWidget(splitter)

        layout.addLayout(infoLayout)

    def addWarning(self, layout):
        self.warning = MyWarningWidget()
        layout.addWidget(self.warning)
        
    def addStats(self, layout):
        self.plots = {}
        self.plots[0] = MyMultipleWidget(keys_ins = self.keys_ins, keys_win = self.keys_win, times=self.times)
        self.plots[1] = MyMultipleWidget(keys_ins = self.keys_ins, keys_win = self.keys_win, times=self.times)

        splitter = QtGui.QSplitter()
        splitter.addWidget(self.plots[0])
        splitter.addWidget(self.plots[1])
        layout.addWidget(splitter)
        
    def check_warnings_threshold(self, v):
        if v < self.warnings_threshold[0]:
            return 0
        elif v < self.warnings_threshold[1]:
            return 1
        else:
            return 2
    
    def getSumoCarsInfo(self, info):
        posList = info.split(';')
        ret = []
        for pos in posList:
            ret.append(map(float, pos.split('_')))
        return ret
        
    def update(self):
        self.frame = self.frame + 1
        current_time = self.ins_data['Time'].iloc[self.frame]
        self.sld.setValue(int(current_time))
        if current_time > 300:
            self.timer.stop()
        
        ''' update statistical warnings '''
        #warnings = self.current_userpos[self.current_userpos['Date Begin'] + 30 == current_time]
        #self.update_warnings = [max(self.check_warnings_threshold(warnings[lbl].values[0]) for lbl in self.warnings_details[tar]) for tar in ['Speeding', 'Speed Control', 'Dangerous Distance', 'Aggressive Lane Switch']]
        '''
        for tar in ['Speeding', 'Speed Control', 'Dangerous Distance', 'Aggressive Lane Switch']:
            for lbl in self.warnings_details[tar]:
                print lbl
                print warnings
                print self.check_warnings_threshold(warnings[lbl].values[0])
        '''

        ''' update predicted events '''
        prediction = self.current_prediction[self.current_prediction['st_t_stamp'] == current_time]
        if len(prediction) > 0:
            self.update_events = [prediction[lbl].values[0] for lbl in ['collisions', 'over speed', 'too close', 'lane switch to left', 'lane switch to right']]
        
        self.setWarnings(current_time)
        if max(self.update_warnings) == 0:
            color = '#32CD32'
        elif max(self.update_warnings) == 1:
            color = '#FFD700'
        else:
            color = '#FF4500'
        
        self.carView.update_figure([self.ins_data['X'].iloc[self.frame], self.ins_data['Y'].iloc[self.frame]], color, self.getSumoCarsInfo(self.ins_data['SumoCars'].iloc[self.frame]))
        self.warning.update_item(self.update_warnings, self.update_events)
        
        ''' update figures '''
        self.plots[0].update_view(self.ins_data, self.current_userpos, self.current_valuepos, current_time) 
        self.plots[1].update_view(self.ins_data, self.current_userpos, self.current_valuepos, current_time)
        
        message = "User " + str(self.user_id) + "-" + str(self.user_mode) + "  |  Time : " + str(current_time) + " s "
        if self.isPaused:
            message = message + "(Paused)"
        self.statusBar().showMessage(message)
        
    def setWarnings(self, time):
        used_Data = self.win_data_p[self.win_data_p['Duration']==self.warning_duration]
        recent = used_Data[used_Data['Date Begin']+self.warning_duration < time]
        if len(recent)==0:
            data=used_Data.iloc[0]
        else:
            data=recent.iloc[-1]
        warnings = ['Speeding','Speed Control', 'Aggressive Lane Switch', 'Dangerous Distance']
        for i,w in enumerate(warnings):
            cols = self.warnings_details[w]
            most = data[cols].max()
            print w, most
            if most > self.warnings_threshold[1]:
                self.update_warnings[i]=2
            elif most > self.warnings_threshold[0]:
                self.update_warnings[i]=1
            else :
                self.update_warnings[i]=0
        print self.update_warnings
            
    def timeControl(self, value):
        self.frame = self.ins_data[self.ins_data['Time'] > value - 0.01].iloc[0].name
        self.update()
        
    def pauseTime(self, paused):
        self.isPaused = paused
        if paused:
            self.timer.stop()
        else :
            self.timer.start(1)
        self.update()
        
qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("test")
aw.showFullScreen()
aw.show()
#sys.exit(qApp.exec_()) %tb
qApp.exec_();


# In[ ]:




# * WindowPlot
#     * ne pas calculer le classement pous user, scenario, time, duration !!!
#     * finir le tri des donnees
#     * faire le menu des options. Similaire au Instant, mais pleins de checkbox pour choisir les keys, et des radio button pour choisir la taille des fenetres a prendre en compte, et le mode : value ou rank ?
#     
# * Radar plot
#     * recopier le code, option menu similaire a window plot avec en plus le choix radar ou plat

# In[ ]:

import pandas as pd
win_data_v = pd.read_csv('valuepos.csv')

times = win_data_v['Duration'].unique()
times
list(win_data_v)

data = win_data_v
recent = data.iloc[0]
double = data.iloc[0].copy()
double['Date Begin'] = double['Date Begin'] + 10
recent = pd.DataFrame([recent,double], index=[0,1])


# In[ ]:

b = [6,3,6,8,9,0]

for i,bn in enumerate(b):
    print i,bn
    
b[1:]

a = {1:'1', 2:'7',  3:'8'}
a.keys()
for i,(k,v) in enumerate(a.iteritems()):
    print i,k,v


#     vhmffh,ghj,
