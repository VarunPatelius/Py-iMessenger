'''
This folder contains utilities and helpful functions that the program uses when it first starts up
'''

from pathlib import Path
import sys


PROJECT_DIRECTORY = "/" + "/".join(Path(__file__).parent.absolute().parts[1:-3])    #Returns the absolute path of the src/ folder for absolute path usage
OPERATING_SYSTEM = sys.platform                                                     #Returns the OP of the machine the program is running on


def updateSysPath():
    '''
    This function is used to add the backend and frontend folders to sys.path
    so that it is easier to import them into files, makes use of their absolute path
    '''

    sys.path.append(f"{PROJECT_DIRECTORY}/src/frontend/error")      #This contains the path to the function that can display errors
    sys.path.append(f"{PROJECT_DIRECTORY}/src/backend/plugins")     #This contains the folder which has all user created extensions
    sys.path.append(f"{PROJECT_DIRECTORY}/src/backend")             #Allows for easier access to backend components (ie. database)


def osCheck():
    '''
    Since Py-iMessenger is built upon iMessage and AppleScript, the operating system
    needs to be checked to ensure that it is a MacOS device, this function does that
    '''

    if OPERATING_SYSTEM != "darwin":        #If not a MacOS device
        from errorBox import showError      #Import the showError library for the error message
        showError()                         #The showError function is used when the OS is not MacOS since Py-iMessenger only functions on MacOS
        sys.exit()