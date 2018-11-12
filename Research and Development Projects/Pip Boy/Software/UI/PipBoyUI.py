# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PipBoy.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class PipBoyUI(object):
    def setupUi(self, MainWindow):
        """
        function to setup UI

        This function setup:
            - MainWindow
            - centralwidget
            - pb_DispDrone1
            - pb_DispDrone2
            - pb_DispDrone3
            - pb_DispDrone4
            - lbl_CountDownTimer
            - lbl_MissionStatus
            - lbl_Help

        For further information, please refer to PyQt5/Qt5 Documentation

        It should be noted that PyQt Code such as this is not meant to be
        modified (even this much is excessive).
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        droneDisplayFont = QtGui.QFont()
        droneDisplayFont.setPointSize(11)

        timerDisplayFont = QtGui.QFont()
        timerDisplayFont.setFamily("3ds")
        timerDisplayFont.setPointSize(12)
        timerDisplayFont.setBold(True)
        timerDisplayFont.setUnderline(True)
        timerDisplayFont.setWeight(75)

        MissionStatusAndHelpDisplayFont = QtGui.QFont()
        MissionStatusAndHelpDisplayFont.setPointSize(10)

        self.pb_DispDrone1 = QtWidgets.QPushButton(self.centralwidget)
        self.pb_DispDrone1.setGeometry(QtCore.QRect(0, 384, 200, 96))
        self.pb_DispDrone1.setFont(droneDisplayFont)
        self.pb_DispDrone1.setObjectName("pb_DispDrone1")

        self.pb_DispDrone2 = QtWidgets.QPushButton(self.centralwidget)
        self.pb_DispDrone2.setGeometry(QtCore.QRect(200, 384, 200, 96))
        self.pb_DispDrone2.setFont(droneDisplayFont)
        self.pb_DispDrone2.setObjectName("pb_DispDrone2")

        self.pb_DispDrone3 = QtWidgets.QPushButton(self.centralwidget)
        self.pb_DispDrone3.setGeometry(QtCore.QRect(400, 384, 200, 96))
        self.pb_DispDrone3.setFont(droneDisplayFont)
        self.pb_DispDrone3.setObjectName("pb_DispDrone3")

        self.pb_DispDrone4 = QtWidgets.QPushButton(self.centralwidget)
        self.pb_DispDrone4.setGeometry(QtCore.QRect(600, 384, 200, 96))
        self.pb_DispDrone4.setFont(droneDisplayFont)
        self.pb_DispDrone4.setObjectName("pb_DispDrone4")

        self.lbl_CountDownTimer = QtWidgets.QLabel(self.centralwidget)
        self.lbl_CountDownTimer.setGeometry(QtCore.QRect(629, 0, 161, 51))

        self.lbl_CountDownTimer.setFont(timerDisplayFont)
        self.lbl_CountDownTimer.setObjectName("lbl_CountDownTimer")

        self.lbl_Help = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Help.setGeometry(QtCore.QRect(0, 350, 51, 31))

        self.lbl_Help.setFont(MissionStatusAndHelpDisplayFont)
        self.lbl_Help.setObjectName("lbl_Help")

        self.lbl_MissionStatus = QtWidgets.QLabel(self.centralwidget)
        self.lbl_MissionStatus.setGeometry(QtCore.QRect(550, 330, 241, 51))
        self.lbl_MissionStatus.setFont(MissionStatusAndHelpDisplayFont)
        self.lbl_MissionStatus.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.lbl_MissionStatus.setObjectName("lbl_MissionStatus")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pb_DispDrone1.setText(_translate("MainWindow", "Drone #1"))
        self.pb_DispDrone3.setText(_translate("MainWindow", "Drone #3"))
        self.pb_DispDrone4.setText(_translate("MainWindow", "Drone #4"))
        self.pb_DispDrone2.setText(_translate("MainWindow", "Drone #2"))
        self.lbl_CountDownTimer.setText(_translate("MainWindow", "99:99:99.00"))
        self.lbl_Help.setText(_translate("MainWindow", "Help"))
        self.lbl_MissionStatus.setText(_translate("MainWindow", "4 Of 4 Codes found! \nPIN: 99999"))


def main():
    """
    Function to display the PipBoyUI

    For more information please refer to PyQt5/Qt Documentation

    Note that the MainWindow's WindowFlags have been set to FramelessWindowHint.
        This is to ensure that it fits on the needed raspberry pi
        screen (linked below), with minimal screen space wastage

    The dimentions used here are based on the following raspberry pi screen:
        https://www.adafruit.com/product/3578
    """
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    ui = PipBoyUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
