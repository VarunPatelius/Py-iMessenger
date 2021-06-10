from PyQt5.QtWidgets import QDialog, QPushButton, QTableWidget, QTableWidgetItem, QTableView, QAbstractScrollArea
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QCursor


class ExtensionManager(QDialog):
    def __init__(self, mainPage):
        '''
        This class contains the extension manager which allows users to see
        various information about different extensions such as if they're enabled, if
        they support file sending and their help messages.

        The extension manager also allows users to turn extensions on and off via a 
        double click
        '''

        QDialog.__init__(self)
        self.mainPage = mainPage
        self.setupUi()


    def updateTable(self):
        '''
        In case the system is ever rebooted with new information, this 
        method will always run when the extension manager is opened to ensure that 
        the most accurate information is being displayed as all cells will be reset
        '''

        self.allCommands = self.mainPage.backendConnection.messenger.commands           #Pulls up all the commands that are stored in the messenger object in the backend
        self.commandNames = [cmd for cmd in self.allCommands.keys() if cmd != "/help"]  #Finds all commands except the /help command

        self.extensionTable.setRowCount(len(self.commandNames))
        self.extensionTable.setVerticalHeaderLabels(self.commandNames)

        for i in range(len(self.commandNames)):                                         #Interates over every command
            commandToEnter = self.allCommands[self.commandNames[i]]                     #Accesses the command graph data
            for j in range(3):
                data = commandToEnter.graphData[j]
                processed = QTableWidgetItem(data)
                processed.setFlags(Qt.ItemIsEnabled)
                self.extensionTable.setItem(i, j, processed)                            #Places within the table

        self.extensionTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)   #These are just set to ensure that the table remains clean
        self.extensionTable.resizeColumnsToContents()
        self.extensionTable.resizeRowsToContents()
        self.extensionTable.setWordWrap(True)


    def setupUi(self):
        self.DEFAULT_STYLE = "background-color:rgb(236, 236, 236);\n"\
                        "border-color:rgb(94, 96, 112);\n"\
                        "border-style:outset;\n"\
                        "border-width:2px;\n"\
                        "border-radius:10px;\n"\
                        "color:black;"    

        self.setWindowTitle("Py-iMessenger Extension Manager")
        self.setFixedWidth(461)
        self.setFixedHeight(196)

        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        self.extensionTable = QTableWidget(self)
        self.extensionTable.setGeometry(QRect(10, 0, 441, 151))
        self.extensionTable.setColumnCount(3)
        self.extensionTable.setHorizontalHeaderLabels(["Help", "Enabled", "File Sending"])
        self.extensionTable.setSelectionBehavior(QTableView.SelectRows)                     #Only rows can be selected, not cells
        self.extensionTable.itemDoubleClicked.connect(self.enableEdit)                      #Double clicking a row will disable/enable an extension

        self.closeManagerButton = QPushButton(self)
        self.closeManagerButton.setGeometry(QRect(180, 160, 113, 32))
        self.closeManagerButton.setText("Save and Close")
        self.closeManagerButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeManagerButton.setStyleSheet(self.DEFAULT_STYLE)
        self.closeManagerButton.clicked.connect(self.closeManager)


    def enableEdit(self, itemClicked):
        '''
        After a row is clicked, the row number is brought up and since
        the enable and disable features are all kept in the second column
        the extension is brought up and is swapped
        '''

        rowToAlter = itemClicked.row()                              #Find the row of the click
        extensionToAlter = self.commandNames[rowToAlter]            #Use the row to find the extension using index
        newMode = not self.allCommands[extensionToAlter].enabled    #Switch the enable mode

        self.allCommands[extensionToAlter].enabled = newMode
        self.allCommands[extensionToAlter].updateGraphData()        #Update graph data for later use

        processed = QTableWidgetItem(str(newMode))
        processed.setFlags(Qt.ItemIsEnabled)
        self.extensionTable.setItem(rowToAlter, 1, processed)


    def closeManager(self):
        self.mainPage.show()
        self.mainPage.move(self.pos())
        self.close()