# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1013, 591)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_graph = QtWidgets.QLabel(self.centralwidget)
        self.label_graph.setObjectName("label_graph")
        self.verticalLayout.addWidget(self.label_graph)
        self.view_layout = QtWidgets.QVBoxLayout()
        self.view_layout.setObjectName("view_layout")
        self.view_graph = QtWidgets.QGraphicsView(self.centralwidget)
        self.view_graph.setObjectName("view_graph")
        self.view_layout.addWidget(self.view_graph)
        self.verticalLayout.addLayout(self.view_layout)
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.verticalLayout.addWidget(self.progress_bar)
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setObjectName("buttons_layout")
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setObjectName("btn_start")
        self.buttons_layout.addWidget(self.btn_start)
        self.btn_stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setObjectName("btn_stop")
        self.buttons_layout.addWidget(self.btn_stop)
        self.verticalLayout.addLayout(self.buttons_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Population Census"))
        self.label_graph.setText(_translate("MainWindow", "Graph:"))
        self.btn_start.setText(_translate("MainWindow", "Render"))
        self.btn_stop.setText(_translate("MainWindow", "Stop"))
