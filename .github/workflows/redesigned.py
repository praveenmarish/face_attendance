from PyQt5 import QtCore, QtGui, QtWidgets
from core import test, take_photos, train, attendence
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 80, 121, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(500, 80, 121, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(150, 170, 121, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(500, 170, 121, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 295, 121, 51))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(150, 350, 471, 211))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "attendence automation system"))
        self.pushButton.setText(_translate("MainWindow", "Test camera"))
        self.pushButton_2.setText(_translate("MainWindow", "Take photos"))
        self.pushButton_3.setText(_translate("MainWindow", "Train dataset"))
        self.pushButton_4.setText(_translate("MainWindow", "Take attendance"))
        self.label.setText(_translate("MainWindow", "message:"))
        
        self.pushButton.clicked.connect(self.one_click)
        self.pushButton_2.clicked.connect(self.two_click)
        self.pushButton_3.clicked.connect(self.three_click)
        self.pushButton_4.clicked.connect(self.four_click)
        pass
        
    def one_click(self):
        self.textEdit.setText("Testing camera...")
        test()
        self.textEdit.setText(" ")
        pass
    
    def two_click(self):
        self.textEdit.setText("Taking photos...")
        take_photos()
        self.textEdit.setText(" ")
        pass
        
    def three_click(self):
        self.textEdit.setText("Train from images...")
        train()
        self.textEdit.setText(" ")
        pass
        
    def four_click(self):
        self.textEdit.setText("Taking attendance")
        attendence()
        self.textEdit.setText(" ")
        pass


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
