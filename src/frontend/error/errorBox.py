from PyQt5 import QtWidgets

def showError(errorMessage="PyMessenger only works on macOS and has only been tested on Big Sur 11.2.3 and Catalina 10.15.7"):
    '''
    The showError can be used by any file since it is added to path and is
    used to show any sort of critical errors such as OS compatibility and the initial imports
    '''

    app = QtWidgets.QApplication([])

    error_dialog = QtWidgets.QErrorMessage()
    error_dialog.showMessage(errorMessage)          #The errorMessage can be set as a argument for the function

    app.exec_()