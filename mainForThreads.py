import numpy as np
from PyQt5 import QtWidgets as QtGui, QtWidgets
from PyQt5.QtCore import QThread
import sys
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import urllib.request as urllib2


import design2
import pyqtgraph as pg
import json
import time

class getPostsThread(QThread):
    def __init__(self):
        """
        Make a new thread instance
        """
        QThread.__init__(self)

    def __del__(self):
        self.wait()


    def run(self):
        """
        run in new thread
        """
        import Start
        Start.start()
        #self.sleep(2)

class ThreadingTutorial(QtGui.QMainWindow, design2.Ui_MainWindow):
    """
        How the basic structure of PyQt GUI code looks and behaves like is
        explained in this tutorial
        """
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.btn_start.setText('Render')
        self.btn_start.clicked.connect(self.start_getting_top_posts)


    def start_getting_top_posts(self):
        '''
        When click at Start Button
        '''
        self.btn_start.setEnabled(False)

        print('Start Rendering')
        self.get_thread = getPostsThread()
        self.get_thread.start()


        self.btn_stop.setEnabled(True)
        self.btn_stop.clicked.connect(self.get_thread.terminate)


def main():
    app = QtGui.QApplication(sys.argv)
    form = ThreadingTutorial()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
