import sys
import time

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, figureList):
        super().__init__()
        self.resize(1500, 1100)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QVBoxLayout(self._main)



        # Bat dau sua o day
        self.figureList = figureList
        self.frameNumber = 0                                                                    # Start rendering with frame 0
        thisFigure = self.figureList[self.frameNumber]
        self.dynamic_canvas = FigureCanvas(thisFigure)
        self.layout.addWidget(self.dynamic_canvas)
        #self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.dynamic_canvas, self))
        self._timer = self.dynamic_canvas.new_timer(100, [(self._update_canvas, (), {})])
        self._timer.start()

    def _update_canvas(self):
        if self.frameNumber != len(self.figureList)-1: self.dynamic_canvas.setParent(None)        #The Graph will stop in last Frame
        if self.frameNumber < len(self.figureList) - 1:
            self.frameNumber = self.frameNumber + 1
            figure = self.figureList[self.frameNumber]
            self.dynamic_canvas = FigureCanvas(figure)
            self.layout.addWidget(self.dynamic_canvas)



def khoichay(figureX):
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow(figureX)
    app.show()
    qapp.exec_()

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()