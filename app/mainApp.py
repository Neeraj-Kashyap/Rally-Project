# All'apertura dell'applicazio appare la lista degli utenti che hanno gia effettuato l'addtrestamento
# Per fre questo si va a vedere le sub folders dentro models
# Se l'utente clicca su un profilo vede gli addrestamenti che ha effettuato, anche questo tramite le sub folder create
# Un nuovo utente puo creare un nuovo profilo e cominciare l'addrestamento
# Nella schermata iniziale sara visualizzata la lista degli utenti sulla parte sinistra.
# Nella parte destra si visualizzano gli addrestamenti

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGroupBox, QDialog, QVBoxLayout, QListWidget, QLabel, QGridLayout, QSlider, QCheckBox, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSlot, QBasicTimer
from PyQt5 import QtCore
import qdarkstyle
import time
class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.title = 'Training app'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 500
        self.secProgressBar = 0
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createGridlLayout()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
 
        self.show()
 
    def createGridlLayout(self):
        self.horizontalGroupBox = QGroupBox("Vama")
        layout = QGridLayout()
        
        # below train services
        self.userList = QListWidget()
        users = ['User 1', 'User 2', 'User 3']
        self.userList.addItems(users)
        self.userList.setFixedWidth(250)
        layout.addWidget(self.userList, 0, 0)
        # slider for speak
        # ToDo
        self.trainList = QListWidget()
        trains_to_do = ['Left 1', 'Left 2', 'Left 3']
        self.trainList.addItems(trains_to_do)
        self.trainList.setFixedWidth(150)
        layout.addWidget(self.trainList, 0, 1)

        self.newUser = QPushButton('New user')
        layout.addWidget(self.newUser, 1, 0)
        
        self.startTrain = QPushButton('Start Train')
        layout.addWidget(self.startTrain, 1, 1)
        self.startTrain.clicked.connect(self.startTrain_clicked)

        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progressBar, 2, 0, 3, 0) 
        self.progressBar.hide()

        self.timer = QBasicTimer()
        self.step = 0

        # create QVertical Layout
        vLayout = QVBoxLayout()
        # slider for Sensitivity
        self.sliderSensitivity = QSlider(QtCore.Qt.Horizontal)
        default = str(50)
        self.sliderSensitivity.setMinimum(30)
        self.sliderSensitivity.setMaximum(80)
        self.sliderSensitivity.setValue(int(default))
        self.sliderSensitivity.setTickPosition(QSlider.TicksBelow)
        self.sliderSensitivity.setTickInterval(2)
        self.sliderSensitivity.valueChanged.connect(self.sensitivityChanged)
        vLayout.addWidget(self.sliderSensitivity)
        # label for slider Sensitivity
        self.labelSens = QLabel(default)
        self.labelSens.setStyleSheet('border: 1px solid black')
        self.labelSens.setAlignment(Qt.AlignCenter)
        self.labelSens.setFixedHeight(20)
        vLayout.addWidget(self.labelSens)
        # slider for turning
        self.sliderTurning = QSlider(QtCore.Qt.Horizontal)
        default = str(2)
        self.sliderTurning.setMinimum(1)
        self.sliderTurning.setMaximum(10)
        self.sliderTurning.setValue(int(default))
        self.sliderTurning.setTickPosition(QSlider.TicksBelow)
        self.sliderTurning.setTickInterval(1)
        self.sliderTurning.valueChanged.connect(self.turningChanged)
        vLayout.addWidget(self.sliderTurning)
        # label for slider Sensitivity
        self.labelturning = QLabel(default)
        self.labelturning.setStyleSheet('border: 1px solid black')
        self.labelturning.setAlignment(Qt.AlignCenter)
        self.labelturning.setFixedHeight(20)
        vLayout.addWidget(self.labelturning)

        # check box for easy drive mode
        self.easyDrive = QCheckBox('Easy Drive mode', self)
        #easyDrive.toggle()
        self.easyDrive.stateChanged.connect(self.turningChanged)
        vLayout.addWidget(self.easyDrive)
        

        # add vertical layout to grid layout
        layout.addLayout(vLayout, 0, 2)

        self.horizontalGroupBox.setLayout(layout)

 
 
    @pyqtSlot()
    def startTrain_clicked(self):
        self.progressBar.show()
        cont = 0
        self.startTrain.setText('Recording')
        if self.timer.isActive():
            print ("cazzo stai a fa")
        else:
            while cont < 3:
                cont += 1
                self.timer.start(20, self)  
                self.step = 0
                self.progressBar.setValue(self.step)


    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            return
        self.step += 1
        self.progressBar.setValue(self.step)



    @pyqtSlot()
    def sensitivityChanged(self):
        self.labelSens.setText(str(self.sliderSensitivity.value()))

    @pyqtSlot()    
    def turningChanged(self):
        print ("porcoddio")
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = App()
    sys.exit(app.exec_())