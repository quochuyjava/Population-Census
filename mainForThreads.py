import copy

import pandas as pd
from PyQt5 import QtWidgets as QtGui, QtWidgets
from PyQt5.QtCore import QThread, QRect
import sys

from PyQt5.QtWidgets import QApplication
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import DataReader
import Graph
import design
import time

# Declaration of global Variables
countriesData = pd.read_excel('population -countries.xls', sep=' ', encoding='utf-8')  # Link to excel file
worldData = pd.read_excel('population - world.xls', sep=' ', encoding='utf-8')
amountOfTopCountries = 20       # amount of top Countries per Year
imageOutputFolder = '/Users/quochuy/Desktop/Github/Population-Census/Images'
videoOutputFolder = '/Users/quochuy/Desktop/Github/Population-Census/Images/Video.avi'

FigureList = []         # List contains rendered Figures
NumberOfFramesWouldBeRendered = 0


def init_years(dataReader):
    '''
    initialize a dictonary of years, which contains all Year Objects in the Data
    :param dataReader: Object from type Datareader, which analyze Excel data files
    :return: dictionary of years key: year (int) value: Year object
    '''
    import Year
    yearsDict = {}
    first_year = dataReader.getFirstYear()
    worldPopulationInYears = dataReader.getWorldPopulationInYearsDict()
    for x in range(dataReader.getCountOfYears()):
        this_year = first_year + x
        top_countries_in_this_year = dataReader.getTopCountries(this_year)
        yearsDict[first_year + x] = Year.Year(this_year, top_countries_in_this_year, worldPopulationInYears)
    return yearsDict


class DrawGraphThread(QThread):
    '''
    This Class's functions run in a new Thread to do functional tasks. For example: analyse Data, render Frames, export Images and Video
    '''
    def __init__(self):
        """
        Make a new thread instance, prevent it to wait for the GUI
        """
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        """
        run in new thread
        """
        import Graph
        import DataReader

        dataReader = DataReader.DataReader(countriesData, worldData, amountOfTopCountries)
        yearsDict = init_years(dataReader)
        graph = Graph.Graph(dataReader, yearsDict, imageOutputFolder, videoOutputFolder)

        global FigureList
        FigureList = graph.getFigureList()

        global NumberOfFramesWouldBeRendered
        NumberOfFramesWouldBeRendered = graph.getNumberofFramesWouldBeRendered()

        graph.render()


class MainWindow(QtGui.QMainWindow, design.Ui_MainWindow):
    """
    This Class's functions draw figures on GUI and do tasks with GUI
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.btn_start.clicked.connect(self.renderButtonClicked)
        self.btn_play_pause.clicked.connect(self.play)
        self.btn_stop.clicked.connect(self.stop)
        self.resize(1500, 1100)


    def renderButtonClicked(self):
        '''
        What do when Start Button is clicked
        '''
        # Change GUI Components
        QApplication.processEvents()
        self.btn_start.setEnabled(False)

        # FROM HIER: RUN IN NEW THREAD
        self.get_thread = DrawGraphThread()
        self.get_thread.start()             # New Thread started
        self.drawFigure()

    def drawFigure(self):
        '''
        Draw first figure on GUI and wait the FigureList to be filled, so it could draw another Figure
        :return:
        '''
        global FigureList
        self.frameNumber = 0  # Start rendering with frame 0

        # Wait FigureList to fill the first Figure
        while len(FigureList) <= self.frameNumber:
            print('waiting for FigureList to init')
            time.sleep(.200)

        #First Figure Initialized
        thisFigure = FigureList[self.frameNumber]
        self.dynamic_canvas = FigureCanvas(thisFigure)
        self.view_layout.addWidget(self.dynamic_canvas)
        self.view_layout.removeWidget(self.dynamic_canvas)


        #Loop to update Figures
        self._timer = self.dynamic_canvas.new_timer(100,
                                                    callbacks=[(self.updateFigure, [], {})])
        self._timer.start()



    def updateFigure(self):
        '''
        Update the Figure. When the a figure need to draw but still not in the FigureList, it wait with a for-loop
        :return:
        '''

        # Update Progess bar
        if self.progress_bar.value() != 100:
            self.progress_bar.setValue(float((len(FigureList) / NumberOfFramesWouldBeRendered)) * 100)

            # Add new Frame
            self.view_layout.addWidget(self.view_graph)
            self.dynamic_canvas.setParent(None)
            figure = copy.copy(FigureList[len(FigureList) -1])  # prevent figure to zoom in
            self.dynamic_canvas = FigureCanvas(figure)
            self.view_layout.addWidget(self.dynamic_canvas)
            self.view_layout.removeWidget(self.dynamic_canvas)
            self.label_status.setText("Rendering "+ str(self.progress_bar.value()) + '% done')


        else:       # All Frames are rendered
            self._timer.stop()
            self.btn_play_pause.setEnabled(True)
            self.btn_stop.setEnabled(True)
            self.progress_bar.hide()
            self.dynamic_canvas.setParent(None)
            self.label_status.setText("Rendering is finished.")


    def play(self):
        # Update UI
        self.btn_play_pause.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.label_status.hide()

        self.frameNumber = 0
        self._timer2 = self.dynamic_canvas.new_timer(100, callbacks=[(self.updateFigurePlayback, [], {})])
        self._timer2.start()



    def stop(self):
        #self.btn_play_pause.setEnabled(True)

        self._timer2.stop()


    def updateFigurePlayback(self):
        '''
        Update the Figure. When the a figure need to draw but still not in the FigureList, it wait with a for-loop
        :return:
        '''
        # The Graph will stop at last Frame
        if self.frameNumber >= NumberOfFramesWouldBeRendered - 1:
            self._timer.stop()
        else:  # Not at last Frame
            self.view_graph.setParent(None)
            self.view_layout.removeWidget(self.label_status)
            if self.frameNumber != 0:
                self.view_layout.removeWidget(self.dynamic_canvas)
                self.dynamic_canvas.deleteLater()
            self.frameNumber = self.frameNumber + 1
            figure = FigureList[self.frameNumber]
            self.dynamic_canvas = FigureCanvas(figure)
            self.view_layout.addWidget(self.dynamic_canvas)

    def closeEvent(self, event):
        sys.exit(app.exec_())


def main():
    global app
    app = QtGui.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
