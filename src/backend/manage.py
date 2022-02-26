from src.backend.utils.setupUtils import updateSysPath, osCheck

updateSysPath()                         #This function updates the sys.path to make imports more concise
osCheck()                               #This checks the computer to ensure that it is compatible with the software, if not, and error is shown

from database import databaseModel      #The database component of the backend
from messenger import messengerModel    #The messaging component of the backend
from user import userModel              #This component deals with loading and saving all user information
from plugins import extensionManager    #extensionManager is a helper function that registers all the plugins with the messaging component
from importlib import reload            #Used to reload all the modules as the user has the ability to reload any changes without restarting
from types import ModuleType            #Used to check and make sure that the modules that are reloaded are actually modules
from threading import Thread            #Is inherited to make the BackendThread
from time import sleep
from logging import exception           #Used to print out any error messages which may appear while the program is in testing mode
import sys
from datetime import datetime

userController = userModel.UserController()
databaseController = databaseModel.DatabaseController()


class BackendThread(Thread):
    def __init__(self, parentInterface):
        Thread.__init__(self, target=self.backendRunner)

        self.parentInterface = parentInterface          #This is the frontend object, which the backend can alter
        self.userController = userController            #The userController which deals with saving and loading user data
        self.database = databaseController              #Creates the database object to interact with chat.db
        

    def closeBackend(self, programTermination=False):
        '''
        Multiple threads will use the same connection, but this ensures that the database connection
        is only broken when the program is shut down, not when it is reloaded
        '''

        self.exit = True #Used to break the while loop on the main thread method

        if programTermination:                      #If the termination flag is set, meaning the program needs to close
            self.database.closeConnection()         #The database will be closed
            print("Program successfully exited.")


    def reloadModules(self):
        '''
        This method is used to reload all the components of the application so that the user does not
        need to stop and rerun the program everytime that they make a change
        '''

        reload(messengerModel)                  #Reloads the messenger model
        reload(extensionManager)                #Reloads the extension manager in case any new plugins were registered

        setModules = list(sys.modules.values()) #Creates a set list of all of the modules that are imported

        for module in setModules:
            try:
                if ("src/backend/plugins/" in module.__file__) and (isinstance(module, ModuleType)):
                    reload(module)              #Only reloads modules if they are in the plugins folder
            except:
                pass


    def setup(self):
        '''
        The setup method is run everytime the program first runs or is reloaded, it loads up all the 
        important assets tha tthe program needs in order to run. It also creates any new users that aren't
        already in the database. All existing users are loaded up
        '''

        self.reloadModules()                                            #Ensures all modules are reloaded and good

        if self.parentInterface.settings.reset:                         #The user has the ability to control if the counter goes to 0 after each reset
            self.parentInterface.sent = 0                               #Sets frontend counter to 0 if the reset option is enabled

        self.messenger = messengerModel.MessengerController()           #Creates a messenger object

        extensionManager.loadExtensions(self.messenger)                 #The extension manager loads all the registered plugins onto the messenger object
        self.allNumbers = self.database.loadPhoneNumbers()              #The database loads up all the phone numbers into a list
        self.allUsers = {}                                              #A dictionary that contains the id of a user as the key and the user object itself as the value
        self.allCommands = list(self.messenger.commands.keys())         #Creates a list of all of the commands/plugins
        self.exit = False                                               #Sets the exit flag to false if in a reset so that the backend runner can function

        self.parentInterface.messagesSent.setProperty("value", self.parentInterface.sent)

        for userId, userNumber in self.allNumbers.items():              #For every id and number
            if self.userController.userInDatabase(userId):              #If that id is already in the database 
                returnedUser = self.userController.loadUser(userId)     #Load up the existing user
                self.allUsers[userId] = returnedUser                    #Add that user to the allUsers dictionary for reference

            else:                                                           #Else
                newUser = userModel.User(id=userId, phoneNumber=userNumber) #Create a new user object with the id and phone number
                self.userController.saveUser(newUser)                       #Save that new user to the database for the future
                self.allUsers[userId] = newUser                             #Add that user to the allUsers dictionary for reference


    def messageProcessor(self, message):
        arguments = [component.strip() for component in message[0].split(",")] #This will break the message into its components

        commandName = arguments[0]                  #The number is the first thing that should show
        userId = message[-2]
        messageService = message[-3]                #This returns if the message is SMS or iMessage
        chatGUID = message[-4]                      #A unique identifier for groupchats, will be None if commmand is from private message
        self.database.latestCommand = message[-1]   #This shows the rowId of the latest command and ensures that messages aren't repeated

        del arguments[0]

        if (userId != 0) and (messageService == "iMessage"):    #Ensures that the message is to a iMessage account/groupchat
            userToSend = self.allUsers[userId]                  #Loads up the user that the response needs to be sent to by using the userId from the message

            self.userController.userEnabler(userObj=userToSend, command=commandName, messaging=self.messenger) #This makes sure that user is enabled and can have commands sent to them

            if (commandName in self.allCommands) and (userToSend.enabled):                                      #If the command is in the list of all commands and the user is enabled
                commandToExecute = self.messenger.commands[commandName]                                         #The command name is used to pull up the actual command function that needs to run
                
                if commandToExecute.enabled:                                                                    #Checks to see if the command itself has been enabled to send
                    toSend = commandToExecute.function(*arguments, userToSend)                                  #The function is executed and its return value is saved

                    if commandToExecute.fileSending:                                                            #If the command is used for sending files
                        self.messenger.sendFile(self.allNumbers[userId], toSend)                                #Send the file with the sendFile method of the messenger
                    else:                                                                                       #Else it will be used for sending text messages
                        toSendCleaned = self.messenger.stringCleaner(toSend)                                    #The message is cleaned to make sure it doesnt make any issues in Bash
                        self.messenger.sendMessage(self.allNumbers[userId], toSendCleaned, chatGUID)            #Send the message with the sendMessage method of the messenger, also passes in a GC identifier

                    self.parentInterface.sent += 1                                                      #Adds to the message counter of the frontend
                    self.parentInterface.messagesSent.setProperty("value", self.parentInterface.sent)   #Sets the value to the counter
                

    def testingMode(self):
        while True:
            message = self.database.findCommands()      #The database will return any message which seems like command

            if self.exit:                               #This ends the thread because it is the exit flag
                break

            if (message != None):
                try:
                    self.messageProcessor(message)
                except BaseException:                   #Errors are printed out the console, the program will still keep running
                    exception("Exception was thrown.")

            sleep(0.1)                                  #Can be switched to a fast time, but this is recommended to ensure proper message processing


    def deploymentMode(self):
        while True:
            message = self.database.findCommands()      #The database will return any message which seems like command

            if self.exit:                               #This ends the thread because it is the exit flag
                break

            if (message != None):
                try:                                    
                    self.messageProcessor(message)      
                except:                                 #Errors are not shown and are simply ignored
                    pass

            sleep(0.1)                                  #Can be switched to a fast time, but this is recommended to ensure proper message processing
            

    def backendRunner(self):
        '''
        backendRunner is the method that does much of the work for the backend
        it loads up all the messages that come in, breaks them into their components,
        generates the return message and send it back to the user
        '''

        self.setup()                                    #Runs the setup function everytime it begins to ensure all assets are up to date
        
        if self.parentInterface.settings.TESTING_MODE:
            self.testingMode()
        else:
            self.deploymentMode()