from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QRadioButton, QLCDNumber, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QIcon, QCursor
from .settings.settingsUi import MessengerSettings
from .manager.managerUi import ExtensionManager
import sys
from utils.setupUtils import PROJECT_DIRECTORY


class MessengerUI(QDialog):
    def __init__(self, backend):
        QDialog.__init__(self)

        self.sent = 0                                                   #This keeps count of how many messages have been sent

        self.backend = backend                                          #This contains the backend thread
        self.backendConnection = self.backend(self)                     #The thread is created
        self.backendConnection.start()                                  #The thread is started

        self.settings = MessengerSettings(self)
        self.extManager = ExtensionManager(self)
        self.setupUi()


    def setupUi(self):
        self.DEFAULT_STYLE = "background-color:rgb(236, 236, 236);\n"\
                        "border-color:rgb(94, 96, 112);\n"\
                        "border-style:outset;\n"\
                        "border-width:2px;\n"\
                        "border-radius:10px;\n"\
                        "color:black;"                                  #Contains the stylesheet for the light mode GUI

        self.DEFAULT_STYLE_DARK = "background-color:rgb(30, 30, 30);\n"\
                        "border-color:rgb(94, 96, 112);\n"\
                        "border-style:outset;\n"\
                        "border-width:2px;\n"\
                        "border-radius:10px;\n"\
                        "color:white;"                                  #Contains the stylesheet for the dark mode GUI

        self.setWindowTitle("Py-iMessenger")
        self.setFixedWidth(461)
        self.setFixedHeight(196)

        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)    #Removes the close window button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        self.addExtension = QPushButton(self)
        self.addExtension.setGeometry(QRect(30, 20, 141, 32))                #Sets the geometry of the item in terms of x, y, width, and height
        self.addExtension.setText("Extension Manager")
        self.addExtension.setCursor(QCursor(Qt.PointingHandCursor))
        self.addExtension.clicked.connect(self.openManager)

        self.reloadSystem = QPushButton(self)
        self.reloadSystem.setGeometry(QRect(30, 80, 141, 32))
        self.reloadSystem.setText("Reload System")
        self.reloadSystem.setCursor(QCursor(Qt.PointingHandCursor))
        self.reloadSystem.clicked.connect(self.reloadSystemSwitch)          #Connects to the function which reloads the system

        self.closeSystem = QPushButton(self)
        self.closeSystem.setGeometry(QRect(30, 140, 141, 32))
        self.closeSystem.setText("Close System")
        self.closeSystem.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeSystem.clicked.connect(self.shutSystemOff)                #Connects to the function which turns the system off

        self.systemStatusIndicator = QRadioButton(self)
        self.systemStatusIndicator.setGeometry(QRect(320, 20, 16, 31))
        self.systemStatusIndicator.setStyleSheet("QRadioButton::indicator {background-color : lightgreen}")

        self.systemStatusLabel = QLabel(self)
        self.systemStatusLabel.setGeometry(QRect(340, 26, 91, 16))
        self.systemStatusLabel.setText("System Online")

        self.messagesSentLabel = QLabel(self)
        self.messagesSentLabel.setGeometry(QRect(330, 120, 101, 16))
        self.messagesSentLabel.setText("Messages Sent")

        self.messagesSent = QLCDNumber(self)
        self.messagesSent.setGeometry(QRect(320, 140, 111, 31))
        self.messagesSent.setStyleSheet("color: rgb(0,0,0);")
        self.messagesSent.setProperty("value", 0)

        self.settingsButton = QPushButton(self)
        self.settingsButton.setGeometry(QRect(350, 50, 61, 31))
        self.settingsButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.settingsButton.clicked.connect(self.openSettings)

        self.allButtons = [self.settingsButton, self.closeSystem, self.reloadSystem, self.addExtension]     #A list of all the buttons so that their stylesheets can all be changed in one loop
        self.allLabels = [self.messagesSentLabel, self.systemStatusLabel]
        self.settingsIconDark = f"{PROJECT_DIRECTORY}/src/frontend/assets/images/settingsImgWhite.png"
        self.settingsIconLight = f"{PROJECT_DIRECTORY}/src/frontend/assets/images/settingsImg.png"
        self.darkMode()


    def shutSystemOff(self):
        '''
        This closes the program but turning on a exit switch which ends the
        for loop of the backend thread and then proceeds to close the database
        connection to the iMessage database, prints a confirmation
        '''

        self.backendConnection.closeBackend(programTermination=True)
        self.destroy()
        sys.exit()


    def reloadSystemSwitch(self):
        '''
        Closes the current backend object and creates a new one, 
        database connection is maintained
        '''

        self.backendConnection.closeBackend()
        self.backendConnection = self.backend(self)
        self.backendConnection.start()  


    def openSettings(self):
        '''
        Opens the settings page 
        '''

        self.settings.show()
        self.settings.move(self.pos())
        self.close()


    def openManager(self):
        self.extManager.updateTable()           #Runs the table update sequence on the extension manager before it is opened
        self.extManager.show()
        self.extManager.move(self.pos())
        self.close()


    def darkMode(self):
        if not self.settings.color:                                     #If dark mode is toggled   
            self.setStyleSheet("background-color:rgb(30,30,30)")        #Set the stylesheet for the background
            self.settingsButton.setIcon(QIcon(self.settingsIconDark))

            for button in self.allButtons:                              #Iterate over all buttons and labels and set their new stylesheets
                button.setStyleSheet(self.DEFAULT_STYLE_DARK)
            for label in self.allLabels:
                label.setStyleSheet("color: rgb(255,255,255)")

        else:
            self.setStyleSheet("background-color:rgb(236,236,236)")
            self.settingsButton.setIcon(QIcon(self.settingsIconLight))
            
            for button in self.allButtons:
                button.setStyleSheet(self.DEFAULT_STYLE)
            for label in self.allLabels:
                label.setStyleSheet("color: rgb(0,0,0)")


def makeApp(backendRunner):
    '''
    This is the function which combines the frontend
    with the backend to make Py-iMessenger work :)
    '''

    app = QApplication(sys.argv)
    interface = MessengerUI(backend=backendRunner)
    interface.show()
    sys.exit(app.exec_())