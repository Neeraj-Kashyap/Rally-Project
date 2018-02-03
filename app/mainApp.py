# All'apertura dell'applicazio appare la lista degli utenti che hanno gia effettuato l'addtrestamento
# Per fre questo si va a vedere le sub folders dentro models
# Se l'utente clicca su un profilo vede gli addrestamenti che ha effettuato, anche questo tramite le sub folder create
# Un nuovo utente puo creare un nuovo profilo e cominciare l'addrestamento
# Nella schermata iniziale sara visualizzata la lista degli utenti sulla parte sinistra.
# Nella parte destra si visualizzano gli addrestamenti

import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGroupBox, QDialog, QVBoxLayout, QListWidget, QLabel, QGridLayout, QSlider, QCheckBox, QProgressBar
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, pyqtSlot, QBasicTimer
from PyQt5 import QtCore
import qdarkstyle
import time

from manage_lists import View_controller


class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.title = 'Training app'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 500
        self.secProgressBar = 0
        self.trains_did = 0
        self.vc_obj = View_controller()
        self.user_selected = 'gold'
        self.model_selected = ' '
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
        # get user list
        users = self.vc_obj.create_user_list()
        #users = ['User 1', 'User 2', 'User 3']
        self.userList.addItems(users)
        self.userList.setFixedWidth(250)
        self.userList.currentItemChanged.connect(self.user_clicked)
        layout.addWidget(self.userList, 0, 0)

        self.trainList = QListWidget()
        # get commands just did
        trains_to_do = self.vc_obj.create_command_list('gold')
        self.trainList.addItems(trains_to_do)
        self.trainList.setFixedWidth(150)
        self.trainList.currentItemChanged.connect(self.model_clicked)
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
        #self.labelSens.setStyleSheet('border: 1px solid black')
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
        #self.labelturning.setStyleSheet('border: 1px solid black')
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
        if self.trains_did >= 3:
                self.startTrain.setText('Start train')
                self.train_did = 0
                self.progressBar.hide()
                # da modificare 
                return
        self.trains_did += 1
        self.progressBar.show()
        cont = 0
        self.startTrain.setText('Recording ' + str(self.trains_did))
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

    def check_models_content(self):
        dir_ = '../models/' + self.user_selected + '/'

        for i in range(len(self.trainList)):
            file_name = self.trainList.item(i)
            for root, dirs, files in os.walk(dir_):
                for file in files:
                    if file.endswith('pmdl'):
                        print (file)
                        self.trainList.item(i).setBackground(QColor('#243427'))
                        #print( os.path.getsize(dir_ + file), str(dir_+file) )
                        #if (os.stat(dir_ + file).st_size) == 0:
                         #   print('red')
                          #  self.trainList.item(i).setBackground(QColor('#571B24'))
                        #elif (os.stat(dir_ + file).st_size) > 0 :
                            #self.trainList.item(i).setBackground(QColor('#243427')) # verde

    @pyqtSlot()
    def sensitivityChanged(self):
        self.labelSens.setText(str(self.sliderSensitivity.value()))

    @pyqtSlot()    
    def turningChanged(self):
        self.labelturning.setText(str(self.sliderTurning.value()))

    @pyqtSlot()    
    def user_clicked(self):
        self.user_selected = self.userList.currentItem().text()
        list_models = []
        trains_to_do = self.vc_obj.create_command_list(self.user_selected)
        for models in trains_to_do:
            split = models.split('.')
            list_models.append(split[0])
        self.trainList.clear()
        self.trainList.addItems(list_models)
        # check the empy models and colors the items
        self.check_models_content()

    @pyqtSlot()    
    def model_clicked(self):
        self.model_selected = self.trainList.currentItem().text()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = App()
    sys.exit(app.exec_())