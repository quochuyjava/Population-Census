from threading import Timer

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
FigureList = []
NumberOfFrames = 0

class getPostsThread(QThread):
    def __init__(self):
        """
        Make a new thread instance
        """
        QThread.__init__(self)

    def __del__(self):
        self.wait()


    # Hilf Function
    def init_years(self, dataReader):
        import Year
        yearsDict = {}
        first_year = dataReader.getFirstYear()
        worldPopulationInYears = dataReader.getWorldPopulationInYearsDict()
        for x in range(dataReader.getCountOfYears()):
            # print(first_year + x)
            this_year = first_year + x
            top_countries_in_this_year = dataReader.getTopCountries(this_year)
            yearsDict[first_year + x] = Year.Year(this_year, top_countries_in_this_year, worldPopulationInYears)
        return yearsDict
    # End Hilf Function

    def run(self):
        """
        run in new thread
        """
        # import Start          das war ok
        # Start.start()         das war ok
        import Graph
        import DataReader as reader
        import pandas as pd
        import Year

        countriesData = pd.read_excel('population -countries.xls', sep=' ', encoding='utf-8')  # Link to excel file
        worldData = pd.read_excel('population - world.xls', sep=' ', encoding='utf-8')
        amountOfTopCountries = 20
        imageOutputFolder = '/Users/quochuy/Desktop/Github/Population-Census/Images'
        videoOutputFolder = '/Users/quochuy/Desktop/Github/Population-Census/Images/Video.avi'
        dataReader = reader.DataReader(countriesData, worldData, amountOfTopCountries)

        yearsDict = self.init_years(dataReader)

        graph = Graph.Graph(dataReader, yearsDict, imageOutputFolder, videoOutputFolder)
        global FigureList
        FigureList = graph.getFigureList()
        global NumberOfFrames
        NumberOfFrames = graph.getNumberofFrames()
        graph.render()




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
        self.btn_start.clicked.connect(self.doSomethingWhenButtonClicked)



    def doSomethingWhenButtonClicked(self):
        '''
        When click at Start Button
        '''
        self.btn_start.setEnabled(False)

        print('Nút Render dc bấm, thred mới dc mở, ở trong thread này nên chạy Graph')
        self.get_thread = getPostsThread()
        self.get_thread.start()

        print('o day van chay tiep, duoi nay de gan Figure vao GUI')

        self.resize(1500, 1100)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QVBoxLayout(self._main)

        # Bat dau sua o day
        global FigureList
        self.frameNumber = 0  # Start rendering with frame 0
        while len(FigureList) <= self.frameNumber:
            print ('waiting for FigureList to init')
            time.sleep(.200)
        thisFigure = FigureList[self.frameNumber]
        self.dynamic_canvas = FigureCanvas(thisFigure)
        self.layout.addWidget(self.dynamic_canvas)
        self._timer = self.dynamic_canvas.new_timer(100, [(self._update_canvas, (), {})])
        self._timer.start()

    def _update_canvas(self):
        print ('Frame needed to show:' + str(self.frameNumber) + '    Frame rendered: [' + str(len(FigureList) -1) + ']')
        while self.frameNumber >= len(FigureList) - 1:
            print ('Frame needed to show: [' + str(self.frameNumber +1 ) + ']    Frame rendered: [' + str(len(FigureList) -1) + ']  - so we have to wait')
            time.sleep(.200)
        self.dynamic_canvas.setParent(None)
        self.frameNumber = self.frameNumber + 1
        figure = FigureList[self.frameNumber]
        self.dynamic_canvas = FigureCanvas(figure)
        self.layout.addWidget(self.dynamic_canvas)
        # Delete previous Frame to save Ram
        FigureList[self.frameNumber -1] = None

        # The Graph will stop in last Frame
        if self.frameNumber == NumberOfFrames - 1 :
            self._timer.stop()
            print (FigureList)


def main():
    app = QtGui.QApplication(sys.argv)
    form = ThreadingTutorial()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
