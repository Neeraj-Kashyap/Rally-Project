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
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot, QBasicTimer
from PyQt5 import QtCore
import qdarkstyle
import time
from train_routine import training_service as ts
from synchronizer import sftp_controller as sftp
from manage_lists import View_controller
from ssh_conn import ssh




class TrainingDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.isTraining = False
        self.setWindowTitle('Training Service')
        windowLayout = QVBoxLayout()
        self.setGeometry( parent.left+parent.width/2-200, parent.top+parent.height/2-150, 400, 300)
        self.layout = QGridLayout()
        self.horizontalGroupBox = QGroupBox("Training "+self.parent.model_selected)
        self.horizontalGroupBox.setLayout(self.layout)
        #––TRAIN BUTTON        
        self.start = QPushButton('START', default=False, autoDefault = False)
        self.start.clicked.connect(self.startTrain_clicked)
        # self.start.setFixedWidth(180)
        self.layout.addWidget(self.start, 2, 0) 
        #––PROGRES BAR
        self.progressBar = QProgressBar(self)
        self.progressBar.setStyleSheet("font: 24pt;")
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.timer = QBasicTimer()
        self.pogressStatus = 0
        self.layout.addWidget(self.progressBar, 1, 0)
        #––TUTORIAL IMAGE
        self.tutorialLabel = QLabel("From when you press START you have to\n\n"+
                                    "speek THREE times "+self.parent.model_selected.upper()+
                                    ":\nonce for evry bar filling")
        self.tutorialLabel.setStyleSheet("font: 22pt;")
        self.layout.addWidget(self.tutorialLabel, 0, 0)

        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.timer.start(10, self)
    
    @pyqtSlot()
    def startTrain_clicked(self):
        self.isTraining = True
        if self.parent.model_selected == 'undefined':
            self.progressBar.setValue(0)
            self.progressBar.setFormat('seleziona un modello')
        elif not self.timer.isActive():
            index = self.parent.trainList.currentRow()
            self.parent.trainList.item(index).setIcon(QIcon('icons/unchecked.png'))
            
            self.timer.start(21.5, self)
            recordingThread = threading.Thread(target=ts.updateModel, 
                                               args=[self.parent.model_selected, 
                                                     'samples/', 
                                                     'models/'+self.parent.user_selected+'/', 
                                                      self.parent])
            recordingThread.start()
            # self.pogressStatus = 0
            
    def timerEvent(self, event):
        self.progressBar.setFormat('')
        if self.isTraining:
            if self.pogressStatus >= 300:
                self.timer.stop()
                self.pogressStatus = 0
                self.hide()
                return
            self.pogressStatus += 1
            self.progressBar.setValue( self.pogressStatus%100 )
        else:
            self.pogressStatus += 1
            self.progressBar.setValue( self.pogressStatus )
            if self.pogressStatus >= 12:
                self.progressBar.setValue( 12-self.pogressStatus%12 )
            if self.pogressStatus >= 2*12:
                self.timer.stop()
                self.pogressStatus = 0
                self.progressBar.setValue(0)


class App(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'Training app'
        self.left = 300
        self.top = 200
        self.width = 500
        self.height = 550
        self.secProgressBar = 0
        self.trains_did = 0
        self.vc_obj = View_controller()
        self.user_selected = 'gold'
        self.model_selected = 'undefined'
        self.car_on = False
        self.initUI()
        self.conn = None
        #parametri avanzati
        self.selectedSensivity = 0.5
        self.turningSensitivity = 4 
        self.isEsayDrive = False
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createGridlLayout()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
 
        self.show()


    def createGridlLayout(self):
        
        self.horizontalGroupBox = QGroupBox("Car Console")

        self.layout = QGridLayout()
        
        #USER COLUMN ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– (FIRST)
        #–––USER LIST
        self.userList = QListWidget()
        self.userList.setStyleSheet("font: 22pt;")
        #––––– get user list
        users = self.vc_obj.create_user_list()
        self.userList.addItems(users)
        self.userList.setFixedWidth(250)
        self.userList.currentItemChanged.connect(self.user_clicked)
        #–– ADD USER LINE
        self.userLine = QLineEdit()
        self.userLine.setPlaceholderText('Add a new Player here...')
        self.userLine.returnPressed.connect(self.save_user)
        self.userList.setFixedWidth(250)

        #TRAIN COLUMN ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– (SECOND)
        #––MODELS LIST
        self.trainList = QListWidget()
        self.trainList.setStyleSheet("font: 20pt;")
        #––––get commands just did
        trains_to_do = self.vc_obj.create_command_list('gold')
        self.trainList.addItems(trains_to_do)
        self.trainList.setFixedWidth(180)
        self.trainList.currentItemChanged.connect(self.model_clicked)
        #––TRAIN BUTTON        
        self.startTrain = QPushButton('Train selected Model', default=False, autoDefault = False)
        self.startTrain.clicked.connect(self.openTrainWindow)
        self.startTrain.setFixedWidth(180)

        #TUTORIAL COLUMN ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– (THIRD)
        #––TUTORIAL IMAGE
        self.tutorialLabel = QLabel()
        tutorialImage = QPixmap('prova.png')
        self.tutorialLabel.setPixmap(tutorialImage.scaled(200, 80000, Qt.KeepAspectRatio))
        self.tutorialLabel.setFixedWidth(200)
        #––SYNCHRONIZE BUTTON
        self.settingsButton = QPushButton('⚙️', default=False, autoDefault = False)

        #BELOW COLUMNS ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– BELOW
        
        #––START BUTTON
        self.startCar = QPushButton('START!', default=False, autoDefault = False)
        self.startCar.clicked.connect(self.toggle_car)
        
        #Column 1
        self.layout.addWidget(self.userList, 0, 0)
        self.layout.addWidget(self.userLine, 1, 0)
        #column 2
        self.layout.addWidget(self.trainList, 0, 1)
        self.layout.addWidget(self.startTrain, 1, 1)
        #Column3
        # self.layout.addWidget(self.tutorialLabel, 0, 2)
        # self.layout.addWidget(self.settingsButton, 1, 2)
        #Below columns
        self.layout.addWidget(self.startCar, 10, 0, 4, 0) 


        self.horizontalGroupBox.setLayout(self.layout)
        #select first rows
        self.userList.setCurrentRow( 0 )
        self.trainList.setCurrentRow( 0 )

    def create_advanced_layout(self):
        # create the advanced settings layout
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

        return vLayout

        #self.layout.addLayout(vLayout, 0, 2)
 
    

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
        self.syncClicked()
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
        #Reset widget    
        self.userList.addItem(str(self.userLine.text()))
        self.userLine.setText('')
        
        

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
 
    def syncClicked(self):
        print(self.user_selected)
        result = sftp.synchronizeUser(self.user_selected, 
                                      self.selectedSensivity, 
                                      self.turningSensitivity, 
                                      self.isEsayDrive)
        if not result:
            self.startCar.setStyleSheet("background-color: #571B24")
        else:
            self.startCar.setStyleSheet("background-color: #243427")

    
    def settingsClicked(self):
       settingsLayout = self.create_advanced_layout()   
       self.tutorialLabel.hide()
       self.layout.addWidget(settingsLayout, 0,2)

    def openTrainWindow(self):
        self.training = TrainingDialog(self)
        self.training.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = App()
    sys.exit(app.exec_())