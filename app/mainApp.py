# All'apertura dell'applicazio appare la lista degli utenti che hanno gia effettuato l'addtrestamento
# Per fre questo si va a vedere le sub folders dentro models
# Se l'utente clicca su un profilo vede gli addrestamenti che ha effettuato, anche questo tramite le sub folder create
# Un nuovo utente puo creare un nuovo profilo e cominciare l'addrestamento
# Nella schermata iniziale sara visualizzata la lista degli utenti sulla parte sinistra.
# Nella parte destra si visualizzano gli addrestamenti
import threading
import subprocess
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
from ssh_conn import ssh

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
        self.car_on = False
        self.initUI()
        self.conn = None
 
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
        self.userList.setStyleSheet("font: 22pt;")
        # get user list
        users = self.vc_obj.create_user_list()
        self.userList.addItems(users)
        self.userList.setFixedWidth(250)
        self.userList.currentItemChanged.connect(self.user_clicked)

        self.layout.addWidget(self.userList, 0, 0)

        self.trainList = QListWidget()
        self.trainList.setStyleSheet("font: 20pt;")
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
        self.startCar.clicked.connect(self.toggle_car)
        self.layout.addWidget(self.startCar, 10, 0, 4, 0) 

        self.timer = QBasicTimer()
        self.pogressStatus = 0

        # create QVertical Layout
        vLayout = QVBoxLayout()

        # title label for sens
        default = str(50)
        str_sens = 'Car Sensitivity: ' + default
        self.titleSens = QLabel(str_sens)
        self.titleSens.setAlignment(Qt.AlignCenter)
        self.titleSens.setFixedHeight(40)
        vLayout.addWidget(self.titleSens)
        # slider for Sensitivity
        self.sliderSensitivity = QSlider(QtCore.Qt.Horizontal)
        self.sliderSensitivity.setMinimum(20)
        self.sliderSensitivity.setMaximum(80)
        self.sliderSensitivity.setValue(int(default))
        self.sliderSensitivity.setTickPosition(QSlider.TicksBelow)
        self.sliderSensitivity.setTickInterval(2)
        self.sliderSensitivity.valueChanged.connect(self.sensitivityChanged)
        vLayout.addWidget(self.sliderSensitivity)
        
         # title label for sens
        default = str(4)
        str_turning = 'Car Turning: ' + default
        self.titleTurn = QLabel(str_turning)
        self.titleTurn.setAlignment(Qt.AlignCenter)
        self.titleTurn.setFixedHeight(40)
        #self.titleTurn.setFixedWidth(200)
        vLayout.addWidget(self.titleTurn)
        # slider for turning
        self.sliderTurning = QSlider(QtCore.Qt.Horizontal)
        self.sliderTurning.setMinimum(1)
        self.sliderTurning.setMaximum(7)
        self.sliderTurning.setValue(int(default))
        self.sliderTurning.setTickPosition(QSlider.TicksBelow)
        self.sliderTurning.setTickInterval(1)
        self.sliderTurning.valueChanged.connect(self.turningChanged)
        vLayout.addWidget(self.sliderTurning)
        
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
        #select first rows
        self.userList.setCurrentRow( 0 )
        self.trainList.setCurrentRow( 0 )

    @pyqtSlot()
    def startTrain_clicked(self):
        if self.model_selected == 'undefined':
            self.progressBar.setValue(0)
            self.progressBar.setFormat('seleziona un modello')
        elif not self.timer.isActive():
            index = self.trainList.currentRow()
            self.trainList.item(index).setIcon(QIcon('icons/unchecked.png'))
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
        self.progressBar.setFormat( self.model_selected.upper() ) 
        self.progressBar.setValue( self.pogressStatus%100 )


    def check_models_content(self):
        dir_ = 'models/' + self.user_selected + '/'
        for i in range(len(self.trainList)):
            model_path = dir_ + self.trainList.item(i).text() + '.pmdl'
            statinfo = os.stat(model_path)
            if statinfo.st_size == 0:
                self.trainList.item(i).setIcon(QIcon('icons/unchecked.png'))
            else:
                self.trainList.item(i).setIcon(QIcon('icons/checked.png'))

    @pyqtSlot()    
    def toggle_car(self):
        self.syncButton.setStyleSheet("")
        if not self.car_on: # car off
            self.conn = ssh('rasby.local', 'pi', 'raspberry', caller=self)
            #self.conn.sendCommand("pulseaudio --start ; /bin/echo -e 'connect 1C:52:16:53:72:D5 \n exit \n' | bluetoothctl")
            self.conn.sendCommand("python /home/pi/Desktop/Rally-Project/main.py")
        else: # car on
            self.conn.sendCommand("killall python; python /home/pi/Desktop/Rally-Project/STOP.py")
            self.startCar.setText('Start')
            self.startCar.setStyleSheet('Background: none')
            self.car_on = False

    @pyqtSlot()
    def sensitivityChanged(self):
        str_sens = 'Car Sensitivity: ' + str(self.sliderSensitivity.value())
        self.titleSens.setText(str_sens)

    @pyqtSlot()    
    def turningChanged(self):
        str_turning = 'Car Turning: ' + str(self.sliderTurning.value())
        self.titleTurn.setText(str_turning)

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
        self.userLine.setFocus(True)
        self.userLine.raise_()
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
        files = ['left1', 'left2', 'left3', 'right1', 'right2', 'right3', 'start', 'stop', 'right-simple', 'left-simple']
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
        self.trainList.setCurrentRow( 0 )

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