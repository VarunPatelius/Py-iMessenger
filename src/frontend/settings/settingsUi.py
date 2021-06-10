from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QCursor
from configparser import ConfigParser
from utils.setupUtils import PROJECT_DIRECTORY


class MessengerSettings(QDialog):
    def __init__(self, mainPage):
        '''
        This class contains the code for the GUI that controls the settings for Py-iMessenger,
        this includes things like dark mode and the message counter
        '''

        QDialog.__init__(self)
        self.configReader = ConfigParser()                                                  
        self.configReader.read(f"{PROJECT_DIRECTORY}/src/frontend/settings/configUi.ini")   #Opens the .ini file which contains all the settings for the interface

        self.setupUi()
        self.mainPage = mainPage                                                            #Link to the main page of the GUI so that things such as color can be altered
        self.TESTING_MODE = False                                                           #This page controls if testing mode is enabled or not


    def setupUi(self):
        '''
        This is the initial GUI setup for when the settings page is first pulled up
        '''

        self.DEFAULT_STYLE = "background-color:rgb(236, 236, 236);\n"\
                        "border-color:rgb(94, 96, 112);\n"\
                        "border-style:outset;\n"\
                        "border-width:2px;\n"\
                        "border-radius:10px;\n"\
                        "color:black;"                                                      #Contains the default stylesheet for all the components of the settings page

        self.setWindowTitle("Py-iMessenger Settings")
        self.setFixedWidth(461)
        self.setFixedHeight(196)

        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)                    #Removes the close window button so that the user doesn't break anything
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        self.darkMode = QPushButton(self)
        self.darkMode.setGeometry(QRect(65, 30, 111, 32))                                   #Sets the geometry of the item in terms of x, y, width, and height
        self.darkMode.setCursor(QCursor(Qt.PointingHandCursor))                             #Makes a pointing hand cursor show up when hovering over button
        self.darkMode.setStyleSheet(self.DEFAULT_STYLE)
        self.darkMode.clicked.connect(self.editColor)                                       #Connected to the function that deals with dark/light mode

        self.resetSent = QPushButton(self)
        self.resetSent.setGeometry(QRect(65, 90, 111, 32))
        self.resetSent.setCursor(QCursor(Qt.PointingHandCursor))
        self.resetSent.setStyleSheet(self.DEFAULT_STYLE)
        self.resetSent.clicked.connect(self.editReset)                                      #Connected to the function that deals with the counter reset

        self.testingMode = QPushButton(self)
        self.testingMode.setGeometry(QRect(65, 150, 111, 32))
        self.testingMode.setCursor(QCursor(Qt.PointingHandCursor))
        self.testingMode.setStyleSheet(self.DEFAULT_STYLE)
        self.testingMode.clicked.connect(self.editTesting)                                  #Connected to the function that deals with enabling testing mode

        self.darkModeLabel = QLabel(self)
        self.darkModeLabel.setGeometry(QRect(65, 10, 91, 16))
        self.darkModeLabel.setText("Dark Mode")

        self.resetSentLabel = QLabel(self)
        self.resetSentLabel.setGeometry(QRect(65, 70, 141, 16))
        self.resetSentLabel.setText("Reset Messages Sent")

        self.testingModeLabel = QLabel(self)
        self.testingModeLabel.setGeometry(QRect(65, 130, 91, 16))
        self.testingModeLabel.setText("Testing Mode")

        self.closeSettingsButton = QPushButton(self)
        self.closeSettingsButton.setGeometry(QRect(270, 90, 131, 32))
        self.closeSettingsButton.setText("Save and Close")
        self.closeSettingsButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeSettingsButton.setStyleSheet(self.DEFAULT_STYLE)
        self.closeSettingsButton.clicked.connect(self.closeSettings)                        #Connected to the function that closes the settings page and opens the main page back up

        self.loadSettings(setText=True)


    def loadSettings(self, setText=False):
        '''
        This loads up all the settings from the .ini file and sets them as
        attributes for other methods to access, and on startup, it will set the 
        text for the buttons and labels on the settings page
        '''

        self.color = int(self.configReader["interface"]["color"])                           #Pulls up the color setting from the .ini file
        self.reset = int(self.configReader["interface"]["reset"])                           #Pulls up the reset setting from the .ini file
        
        if setText:                                                                         #If setText is enabled (for when the settings page is first opened)
            if self.color:                                                                  #If self.color = 1 (light mode)
                self.darkMode.setText("Enable")                                             #Set the dark mode enabler button to say "enable"
            else:
                self.darkMode.setText("Disable")                                            #Else set it to say "disable" (meaning dark mode is on)

            if self.reset:                                                                  #If reset is enabled                                       
                self.resetSent.setText("Disable")                                           #Reset enabler button will say "disable" (counter resets when project is reset)
            else:
                self.resetSent.setText("Enable")                                            #Else set it to say "enable" (counter doesn't reset when project is reset)

            self.testingMode.setText("Enable")


    def editReset(self):
        '''
        Sets the reset toggle to determine if the messages sent counter
        will reset everytime the program is reset
        '''

        self.loadSettings()                                                                 #Loads the settings so they're all up-to-date
        if self.reset:
            self.reset = 0                                                                  #Same logic as self.loadSettings()
            self.resetSent.setText("Enable")
            self.configReader.set("interface", "reset", "0")                                #Saves the data to .ini
        else:
            self.reset = 1
            self.resetSent.setText("Disable")
            self.configReader.set("interface", "reset", "1")
        self.saveChanges()                                                                  #.ini is saved


    def editColor(self):
        '''
        Sets the dark mode/light mode for the main page GUi
        '''

        self.loadSettings()
        if self.color:
            self.color = 0
            self.darkMode.setText("Disable")
            self.configReader.set("interface", "color", "0")
        else:
            self.color = 1
            self.darkMode.setText("Enable")
            self.configReader.set("interface", "color", "1")
        self.mainPage.darkMode()
        self.saveChanges()


    def editTesting(self):
        '''
        Used to turn testing mode on and off, testing mode prints out errors
        to the console to allow for better troubleshooting while deployment mode 
        does not
        '''

        self.TESTING_MODE = not self.TESTING_MODE

        if self.TESTING_MODE:
            self.testingMode.setText("Disable")
            self.mainPage.systemStatusIndicator.setStyleSheet("QRadioButton::indicator {background-color : yellow}")    #A yellow indicator light means testing mode is on
        else:
            self.testingMode.setText("Enable")
            self.mainPage.systemStatusIndicator.setStyleSheet("QRadioButton::indicator {background-color : lightgreen}")#A green indicator light means deployment mode is on

        self.mainPage.reloadSystemSwitch()                                                                              #Reloads backend into new mode


    def saveChanges(self):
        '''
        Used to save all changes made to the settings back into the file
        '''

        with open(f"{PROJECT_DIRECTORY}/src/frontend/settings/configUi.ini", "w") as configfile:
            self.configReader.write(configfile)


    def closeSettings(self):
        '''
        This closes the settings page and opens the main page back up
        '''

        self.mainPage.show()
        self.mainPage.move(self.pos())          #self.pos() is used so that there is continuity in the general placement of the GUO
        self.close()