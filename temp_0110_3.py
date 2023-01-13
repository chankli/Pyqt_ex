
from PyQt5.QtWidgets import QWidget, QGridLayout
import pyqtgraph as pg
import time 
import datetime
# from utils import TimeAxisItem, timestamp
import math 
from collections import deque
import numpy as np
from pyqtgraph.Qt import QtCore, QtWidgets

def timestamp():
    return int(time.mktime(datetime.datetime.now().timetuple()))

class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)
        # self.enableAutoSIPrefix(True)

    def tickStrings(self, values, scale, spacing):
        return [datetime.datetime.fromtimestamp(value).strftime("%H:%M:%S") for value in values]

pg.setConfigOption('background', '#FFFFFF')
pg.setConfigOption('foreground', 'k')

app = pg.mkQApp('jinkong')
# 
p1 = pg.PlotWidget(            title="RX/RY"         )
# p1.setBackgroundColor('w')

p2 = pg.PlotWidget(
            title="转速",
            # labels={'left': 'r/min'},
            axisItems={'bottom': TimeAxisItem(orientation='bottom')}
        )
p1.showGrid(x=True, y=True)
p2.showGrid(x=True, y=True)
p1.setXRange(0, 150)
p1.setYRange(-30, 30)
p1Curve = p1.plot(pen=None, symbol='o', symbolPen=None, symbolSize=8, symbolBrush=(100, 100, 255, 200))
# p2Curve = p2.plot(pen=None, symbol='o', symbolPen=None, symbolSize=6, symbolBrush=(100, 100, 255, 200))
# p2Curve = p2.plot(pen=None, symbol='o', symbolPen=None, symbolSize=6, symbolBrush=(248, 0, 0))
p2Curve = p2.plot(pen=None, symbol='o', symbolPen=None, symbolSize=6, symbolBrush='b')
layout = pg.LayoutWidget()

rcheck = QtWidgets.QCheckBox('更新转速曲线')
rcheck.setChecked(True)
layout.addWidget(rcheck)
layout.addWidget(p1, row=1, col=0, colspan=3)
layout.addWidget(p2, row=2, col=0, colspan=3)
layout.resize(800,800)
layout.show()
# layout.setBackground('y')

x = 0.1 
qq = deque(maxlen=1024)
def updatePlot():
  global x,qq 
  x = x +0.01 
  qq.append( [ timestamp() , 1000*math.sin(x) +1000] )

  if len(qq) > 2 and rcheck.isChecked():
    plotData = {'x': [], 'y': []}
    for nnn in range( len(qq) ) :
      plotData['x'].append( qq[nnn][0] )
      plotData['y'].append( qq[nnn][1] )
      p2Curve.setData(plotData['x'], plotData['y'])


timer = pg.QtCore.QTimer()
timer.timeout.connect(updatePlot ) # 定时刷新数据显示
timer.start(1000) # 多少ms调用一次

if __name__ == '__main__':
    pg.exec()
