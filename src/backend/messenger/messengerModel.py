from os import system
from utils.setupUtils import PROJECT_DIRECTORY


class Command:
    def __init__(self, name, function, helpMessage="None Provided", fileSending=False):
        '''
        This is the command object and stores the name, function, help message, and if it support
        file sending
        '''

        self.name = name
        self.function = function
        self.helpMessage = helpMessage
        self.fileSending = fileSending                                                  #Shows if the extension supports file sending
        self.enabled = True             
        self.graphData = [self.helpMessage, str(self.enabled), str(self.fileSending)]   #Ths information is used to update the extension manager

    
    def updateGraphData(self):
        self.graphData = [self.helpMessage, str(self.enabled), str(self.fileSending)]   #This will update the data that the extension manager uses
        

class MessengerController:
    def __init__(self):
        self.commands = {}                                  #Creates a dictionary where the key is the command name and the value is the command object

        helpExtension = Command("/help", self.helpCommand)  #The help extension is used to show a list of commands and their help messages
        self.commands["/help"] = helpExtension              #The help command is added to the dictionary of all availible commands


    def sendMessage(self, phoneNumber, message):
        '''
        This is the component that sends the message using applescript and os.system
        '''

        system(f'osascript {PROJECT_DIRECTORY}/src/backend/messenger/messageTexter.applescript "{phoneNumber}" "{message}"')


    def sendFile(self, phoneNumber, filePath):
        '''
        This is the component that sends the file using applescript and os.system *REQUIRES FILEPATH, NOT MESSAGE*
        '''
        
        system(f'osascript {PROJECT_DIRECTORY}/src/backend/messenger/fileTexter.applescript "{phoneNumber}" "{filePath}"')


    def addExtension(self, commandName, commandFunction, commandHelp="None Provided", files=False):
        '''
        The extension manager uses this when loading all plugins and this
        creates the command objects and adds it to the dictionary will the other
        commands
        '''

        newCommand = Command(name=commandName, function=commandFunction, helpMessage=commandHelp, fileSending=files)
        self.commands[newCommand.name] = newCommand


    def helpCommand(self, *args):
        '''
        The help command is a command that exists by default and can be used to show
        all availible commands and their corresponding help messages (when no arguments are given).
        If any arguments are given, they will have to be the name of the commands so that the help 
        message will only show the corresponding help messages of the given command names
        '''

        helpMessage = ""
        commandNames = self.commands.keys()                                     #This is the name of all registered plugins
        commandObjects = self.commands.values()                                 #These are the corresponding command objects

                                                                                #Every command is always passed the user object so if the len(args) == 1, no arguments were given
        if len(args) == 1:                                                      #If no arguments given
            for command in commandObjects:                                      #Then for all the commands in the commandObjects list
                if (not (command.name == "/help")) and command.enabled:         #As long as the command is not named /help
                    helpMessage += f"{command.name}: {command.helpMessage}\n\n" #Add the name of the command and its help message
            return helpMessage

        for argument in args[:-1]:                                              #If arguments are given, then for each argument (excluding the last one since it is the user object)
            if f"/{argument}" in commandNames:                                  #If the argument name is in commandNames
                if self.commands[f"/{argument}"].enabled:                       #Checks to see if the command is enabled
                    commandHelp = self.commands[f"/{argument}"].helpMessage     #Pull up the the corresponding help message of the command name
                    helpMessage += f"/{argument}: {commandHelp}\n\n"
        return helpMessage


    def stringCleaner(self, toSend):
        '''
        The string cleaner method is used to ensure that there no issues when os.system is used
        to execute the applescript from the terminal (which has special characters)
        '''

        cleaned = f" {toSend} "                                                         #This spacing is added to ensure that a command wont end up running and infinite loop                                            
        return cleaned.replace("\"", "\\<.>\"").replace("<.>", "").replace("$", "\$")   #Replaces "$" and "\" which are commonly used in bash