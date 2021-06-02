import json
import jsonpickle                                       #jsonpickle is a library that objects to be pickled into a string that is easy to read and save to a string
from utils.setupUtils import PROJECT_DIRECTORY


SAVE_PATH = f"{PROJECT_DIRECTORY}/src/backend/user/savedUser.json"           #This is the save path to the database which contains all of user data


class User:
    def __init__(self, id, phoneNumber):
        self.enabled = True                             #If the user is enabled then they can have messages sent to the, if they are disabled messages will not be sent
        self.id = id
        self.phoneNumber = phoneNumber


    def addAttribute(self, attributeName, attributeValue):
        '''
        If a plugin wants to add an attribute to a user they can do so by using this method
        '''

        setattr(self, attributeName, attributeValue)


    def pickleUser(self):
        '''
        This returns the pickled version of the user which is used for saving
        '''

        serialized = jsonpickle.encode(self)
        return serialized


    def deleteAttribute(self, attributeName):
        '''
        If a plugin wants to delete an attribute, they can do so by using this method
        '''

        try:
            delattr(self, attributeName)

        except AttributeError:
            pass


    def saveChanges(self):
        '''
        This saves any changes that have been made to the user to the database
        '''

        with open(SAVE_PATH, "r") as userFile:
            data = json.load(userFile)                  #Loads up all the data into a dictionary

        data["users"][self.id] = self.pickleUser()      #The pickled user is saved to the dictionary

        with open(SAVE_PATH, "w") as userFile:
            json.dump(data, userFile)                   #The dictionary is saved into the database


class UserController:
    def __init__(self):
        '''
        The user controller deals with things such as checking if the user is in the database
        or if they need to be saved
        '''

        self.initialData = self.returnSavedData()               #Returns a set of initial data so that the database doesn't have to be constantly reloaded


    def userInDatabase(self, userId):
        '''
        This function is used to check to ensure that a user is actually
        present in the user database by checking to see if their unique userId
        is in the list of all known Ids
        '''

        return userId in self.initialData["users"]["storedIds"] #Checks if the user is in the database


    def returnSavedData(self):
        with open(SAVE_PATH, "r") as userFile:
            return json.load(userFile)                          #Returns the data from the database


    def pickleUser(self, userObj):
        '''
        This is used to convert the user object into something which can be saved
        as a string in the user database 
        '''

        serialized = jsonpickle.encode(userObj)
        return serialized


    def unpickleUser(self, pickledUser):
        '''
        This converts the object string back into an object which can be interacted
        with and changed
        '''

        normal = jsonpickle.decode(pickledUser)
        return normal


    def saveUser(self, userObj):
        '''
        This function is used to save the user to the database and any changes
        made to the user object
        '''

        data = self.returnSavedData()                           #Pulls up the current save data so the updated user can be added to it

        allActiveUsers = data["users"]["storedIds"]             #Creates a list of all the known userIds

        if userObj.id not in allActiveUsers:                    #If the user objects id is not with the other known userIds
            data["users"]["storedIds"].append(userObj.id)       #Add the new userId to the list of known userIds

        data["users"][userObj.id] = self.pickleUser(userObj)    #Save the string version of the user object to the database

        with open(SAVE_PATH, "w") as userFile:
            json.dump(data, userFile)                           #Dump the new data back into the file


    def loadUser(self, userId):
        '''
        This is used to load all user from the database so the user's
        attributes can be accessed
        '''

        data = self.returnSavedData()                           #Pulls up the current save data so the user can be found

        allActiveUsers = data["users"]["storedIds"]             #Creates a list of all known userIds

        if userId in allActiveUsers:                            #If the user is with the known userIds
            userObj = data["users"][str(userId)]                #Pull up the object string
            return self.unpickleUser(userObj)                   #Convert the object string into a user object to use


    def enableUser(self, userObj):
        '''
        Turns messaging on for the user and saves the changes
        '''

        userObj.enabled = True
        userObj.saveChanges()


    def disableUser(self, userObj):
        '''
        Turns messaging off for the user and saves the changes
        '''

        userObj.enabled = False
        userObj.saveChanges()


    def userEnabler(self, userObj, command, messaging):
        '''
        This function is used so that the user can enable or disable messaging
        to them. If a user is enabled, then messages can be sent to them. If a
        user is disabled, then messages cannot be sent to them.
        '''

        number = userObj.phoneNumber

        if command == "/enable":                                                                                    #If the enable command is passed
            if userObj.enabled:                                                                                     #If the user is already enabled
                messaging.sendMessage(message="Py-iMessenger is already enabled for you!", phoneNumber=number)        #Inform them that they're already enabled
            else:                                                                                                   #Else
                self.enableUser(userObj)                                                                            #Enable the user
                messaging.sendMessage(message="Py-iMessenger has been reenabled for you!", phoneNumber=number)

        elif command == "/disable":                                                                                 #If the disable command is passed
            if userObj.enabled:                                                                                     #If the user is already enabled
                self.disableUser(userObj)                                                                           #Disable the user
                messaging.sendMessage(message="Py-iMessenger has been disabled for you!", phoneNumber=number)
            else:                                                                                                   #Else
                messaging.sendMessage(message="Py-iMessenger has already been disabled for you!", phoneNumber=number) #Inform them that they're already disabled