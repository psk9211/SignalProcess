__author__ = 'jpong'

import random
import numpy as np
import sys
import scipy.fftpack as fft

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

from PyQt4 import QtGui, QtCore

class MatplotlibWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axis1 = self.figure.add_subplot(131)
        self.axis2 = self.figure.add_subplot(132)
        self.axis3 = self.figure.add_subplot(133)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)
        self.layoutVertical.addWidget(self.toolbar)

class ThreadSample(QtCore.QThread):
    newSample = QtCore.pyqtSignal(list)
    newSamplefft = QtCore.pyqtSignal(list)
    newSampleifft = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(ThreadSample, self).__init__(parent)

        self.amp = 1
        self.filter_on = False

    def run(self):
        if self.filter_on == False:
            f = lambda x:random.random()+self.amp*np.sin(x)
            x = np.linspace(0, 10)

            fft_feature = fft.fft(map(f, x))

            ifft_feature = fft.ifft(fft_feature)

            self.newSample.emit(map(f, x))
            self.newSamplefft.emit(list(abs(fft_feature)))
            self.newSampleifft.emit(list(ifft_feature))
        elif self.filter_on == True:
            f = lambda x:random.random()+self.amp*np.sin(x)
            x = np.linspace(0, 10)

            fft_feature = fft.fft(map(f, x))
            mean = np.average(abs(fft_feature))
            fft_feature_filter = fft_feature
            for i in range(len(fft_feature)):
                if abs(fft_feature[i]) >= mean:
                    fft_feature_filter[i] = abs(fft_feature[i])
                else:
                    fft_feature_filter[i] = 0

            ifft_feature = fft.ifft(fft_feature_filter)

            self.newSample.emit(map(f, x))
            self.newSamplefft.emit(list(fft_feature_filter))
            self.newSampleifft.emit(list(ifft_feature))

            self.filter_on = False
        else:
            pass



    def setAmp(self, amp):
        self.amp = amp

    def filter(self):
        self.filter_on = True


class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld.setRange(0, 10)
        self.sld.setValue(1)

        self.pushButtonPlot = QtGui.QPushButton(self)
        self.pushButtonFilter = QtGui.QPushButton(self)
        self.pushButtonPlot.setText("Plot")
        self.pushButtonFilter.setText("Filter")
        self.pushButtonPlot.clicked.connect(self.on_pushButtonPlot_clicked)


        self.matplotlibWidget = MatplotlibWidget(self)
        self.matplotlibWidget.axis1.grid(True)
        self.matplotlibWidget.axis2.grid(True)
        self.matplotlibWidget.axis3.grid(True)

        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.pushButtonPlot)
        self.layoutVertical.addWidget(self.pushButtonFilter)
        self.layoutVertical.addWidget(self.sld)
        self.layoutVertical.addWidget(self.matplotlibWidget)

        self.threadSample = ThreadSample(self)
        self.pushButtonFilter.clicked.connect(self.threadSample.filter)
        self.sld.valueChanged[int].connect(self.threadSample.setAmp)
        self.threadSample.newSample.connect(self.on_threadSample_newSample)
        self.threadSample.newSamplefft.connect(self.on_threadSample_newSamplefft)
        self.threadSample.newSampleifft.connect(self.on_threadSample_newSampleifft)
        #self.threadSample.finished.connect(self.on_threadSample_finished)

    @QtCore.pyqtSlot()
    def on_pushButtonPlot_clicked(self):
        self.samples = 0
        self.matplotlibWidget.axis1.clear()
        self.matplotlibWidget.axis2.clear()
        self.matplotlibWidget.axis3.clear()
        self.matplotlibWidget.axis1.grid(True)
        self.matplotlibWidget.axis2.grid(True)
        self.matplotlibWidget.axis3.grid(True)
        self.threadSample.start()

    @QtCore.pyqtSlot(list)
    def on_threadSample_newSample(self, sample):
        self.matplotlibWidget.axis1.plot(sample)
        self.matplotlibWidget.canvas.draw()

    def on_threadSample_newSamplefft(self, sample):
        self.matplotlibWidget.axis2.plot(sample)
        self.matplotlibWidget.canvas.draw()

    def on_threadSample_newSampleifft(self, sample):
        self.matplotlibWidget.axis3.plot(sample)
        self.matplotlibWidget.canvas.draw()

    @QtCore.pyqtSlot()
    def on_threadSample_finished(self):
        self.samples += 1
        if self.samples <= 2:
            self.threadSample.start()

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.resize(666, 333)
    main.show()

    sys.exit(app.exec_())