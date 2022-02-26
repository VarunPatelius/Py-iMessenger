import sqlite3
from getpass import getuser #Used to retrieve the user name of the logged in user to access the iMessage database


class DatabaseController:
    def __init__(self):
        DATABASE_PATH = f"file:/Users/{getuser()}/Library/Messages/chat.db?mode=ro"     #The absolute path to the database in a read-only mode
        self.conn = sqlite3.connect(DATABASE_PATH, uri=True, check_same_thread=False)   #Connects to the database
        self.cursor = self.conn.cursor()                                                #Creates a cursor to interact with the database

        self.latestCommand = self.findLatestCommand()                                   #Finds the highest rowId to start from when finding commands


    def closeConnection(self):
        '''
        Used to close the connection to the database, prints out a confirmation
        '''

        self.conn.commit()
        self.conn.close()


    def findLatestCommand(self):
        '''
        Finds the latest command that was executed by pulling up its rowId to ensure that the same command
        isn't execute over and over again
        '''

        try:
            self.cursor.execute("SELECT MAX(ROWID) FROM message WHERE text LIKE '/%'")  #Finds the max values of the rowId
            return self.cursor.fetchone()[0]                                            #Fetches the highest value
            
            
        except sqlite3.ProgrammingError:
            pass


    def findCommands(self):
        '''
        This function is used to load all the commands along with the id of the user
        who send them and the rowId that they hold
        '''

        try:
            self.cursor.execute(f"SELECT text, cache_roomnames, service, handle_id, ROWID FROM message WHERE text LIKE '/%' AND ROWID > {self.latestCommand}")
            #Find the text, groupchat ID, platform (SMS/iMessage), userID, and rowId from the message table where the text starts with /% and the rowId is greater than that of the latest executed command
            return self.cursor.fetchone()

        except sqlite3.ProgrammingError:
            pass


    def loadPhoneNumbers(self):
        '''
        This loads up all the phone numbers of the people along with their userId
        '''
        
        self.cursor.execute("SELECT ROWID, id FROM handle WHERE service = 'iMessage'")  #Find the rowId and userId from the handle table where the service is iMessage (not SMS)
        return {key:value for (key,value) in self.cursor.fetchall()}                    #Creates a dictionary of the userId:phoneNumbers from the database