# All'apertura dell'applicazio appare la lista degli utenti che hanno gia effettuato l'addtrestamento
# Per fre questo si va a vedere le sub folders dentro models
# Se l'utente clicca su un profilo vede gli addrestamenti che ha effettuato, anche questo tramite le sub folder create
# Un nuovo utente puo creare un nuovo profilo e cominciare l'addrestamento
# Nella schermata iniziale sara visualizzata la lista degli utenti sulla parte sinistra.
# Nella parte destra si visualizzano gli addrestamenti
import threading
import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGroupBox, QDialog, QVBoxLayout, QListWidget, QLabel, QGridLayout, QSlider, QCheckBox, QProgressBar, QLineEdit
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, pyqtSlot, QBasicTimer
from PyQt5 import QtCore
import qdarkstyle
import time
from train_routine import training_service as ts
from synchronizer import sftp_controller as sftp
from manage_lists import View_controller


class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.title = 'Training app'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 550
        self.secProgressBar = 0
        self.trains_did = 0
        self.vc_obj = View_controller()
        self.user_selected = 'gold'
        self.model_selected = 'undefined'
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
        
        self.horizontalGroupBox = QGroupBox("Super Rally Car")

        self.layout = QGridLayout()
        
        # below train services
        self.userList = QListWidget()
        self.userList.setStyleSheet("font: 28pt;")
        # get user list
        users = self.vc_obj.create_user_list()
        self.userList.addItems(users)
        self.userList.setFixedWidth(250)
        self.userList.currentItemChanged.connect(self.user_clicked)

        self.layout.addWidget(self.userList, 0, 0)

        self.trainList = QListWidget()
        self.trainList.setStyleSheet("font: 24pt;")
        # get commands just did
        trains_to_do = self.vc_obj.create_command_list('gold')
        self.trainList.addItems(trains_to_do)
        self.trainList.setFixedWidth(150)
        self.trainList.currentItemChanged.connect(self.model_clicked)
        self.layout.addWidget(self.trainList, 0, 1)

        self.usrLayout = QVBoxLayout()

        self.newUser = QPushButton('New user')
        self.newUser.clicked.connect(self.create_newUser)
        self.usrLayout.addWidget(self.newUser)
        self.layout.addLayout(self.usrLayout, 1, 0)
        
        self.startTrain = QPushButton('Train Model')
        self.layout.addWidget(self.startTrain, 1, 1)
        self.startTrain.clicked.connect(self.startTrain_clicked)

        self.progressBar = QProgressBar(self)
        self.progressBar.setStyleSheet("font: 24pt;")
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.progressBar, 2, 0, 3, 0) 

        self.startCar = QPushButton('START')
        #self.startCar.clicked.connect()
        self.layout.addWidget(self.startCar, 10, 0, 4, 0) 

        self.timer = QBasicTimer()
        self.pogressStatus = 0

        # create QVertical Layout
        vLayout = QVBoxLayout()
        # slider for Sensitivity
        self.sliderSensitivity = QSlider(QtCore.Qt.Horizontal)
        default = str(50)
        self.sliderSensitivity.setMinimum(20)
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
        default = str(4)
        self.sliderTurning.setMinimum(1)
        self.sliderTurning.setMaximum(7)
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
        self.easyDrive = QCheckBox('Easy Drive mode (only Left & Right) - BETA', self)
        #easyDrive.toggle()
        self.easyDrive.stateChanged.connect(self.turningChanged)
        vLayout.addWidget(self.easyDrive)
        

        self.syncButton = QPushButton('Synchronize')
        self.layout.addWidget(self.syncButton, 1, 2)

        self.syncButton.clicked.connect(self.syncClicked)
        # add vertical layout to grid layout
        self.layout.addLayout(vLayout, 0, 2)

        self.horizontalGroupBox.setLayout(self.layout)

    @pyqtSlot()
    def startTrain_clicked(self):
        if self.model_selected == 'undefined':
            self.progressBar.setValue(0)
            self.progressBar.setFormat('seleziona un modello')
        elif not self.timer.isActive():
            self.progressBar.show()
            self.timer.start(21.5, self)
            recordingThread = threading.Thread(target=ts.updateModel, 
                                               args=[self.model_selected, 
                                                     'samples/', 
                                                     'models/'+self.user_selected+'/', 
                                                      self])
            recordingThread.start()
            # self.pogressStatus = 0
            
    def timerEvent(self, event):
        #ts.updateModel('culomerdoso', 'samples/', 'models')
        if self.pogressStatus >= 300:
            self.timer.stop()
            self.pogressStatus = 0
            return
        self.pogressStatus += 1
        self.progressBar.setFormat(self.user_selected+', pronuncia: '+self.model_selected.upper())
        self.progressBar.setValue(self.pogressStatus%100)


    def check_models_content(self):
        dir_ = 'models/' + self.user_selected + '/'

        for i in range(len(self.trainList)):
            file_name = self.trainList.item(i)
            for root, dirs, files in os.walk(dir_):
                for file in files:
                    if file.endswith('pmdl'):
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
    def create_newUser(self):
        self.newUser.hide()
        
        width = self.newUser.frameGeometry().width()
        height = self.newUser.frameGeometry().height()
        self.userLine = QLineEdit()
        self.userLine.setFixedWidth(width)
        self.userLine.setFixedHeight(height)
        self.userLine.setStyleSheet("color: #595c5f;")
        self.userLine.setPlaceholderText('Insert name...')

        self.save_user_btn = QPushButton('Save')
        self.save_user_btn.setFixedWidth(width)
        self.save_user_btn.setFixedHeight(height)
        self.save_user_btn.clicked.connect(self.save_user)

        self.usrLayout.addWidget(self.userLine)
        self.usrLayout.addWidget(self.save_user_btn)
        

    @pyqtSlot()    
    def save_user(self):
        path = 'models/'
        if not str(self.userLine.text()):
            os.mkdir(os.path.join(path,'noName'))
            path += 'noName'
        else:
            os.mkdir(os.path.join(path,str(self.userLine.text())))
            path += str(self.userLine.text())
        files = ['left1', 'left2', 'left3', 'right1', 'right2', 'right3', 'start', 'stop']
        for file in files:
            file += '.pmdl'
            open(os.path.join(path, file), 'w').close()
        # tolgo il layout inserito
        self.userLine.hide()
        self.save_user_btn.hide()
        self.newUser.show()
        self.userList.addItem(str(self.userLine.text()))
        
        

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
        try:
            self.model_selected = self.trainList.currentItem().text()
        except:
            self.model_selected = 'undefined'
 
    @pyqtSlot()    
    def syncClicked(self):
        print(self.user_selected)
        result = sftp.synchronizeUser(self.user_selected, 
                                      self.sliderSensitivity.value()/100, 
                                      self.sliderTurning.value(), 
                                      self.easyDrive.isChecked())
        if not result:
            self.syncButton.setStyleSheet("background-color: #571B24")
        else:
            self.syncButton.setStyleSheet("background-color: #243427")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = App()
    sys.exit(app.exec_())