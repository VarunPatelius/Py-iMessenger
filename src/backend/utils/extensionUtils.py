'''
This program contains helpful utilies that are intended to make it easier for users to 
create their own extensions
'''

from .setupUtils import PROJECT_DIRECTORY                           #Imports the absolute path of the src/ folder from setupUtils
import requests


EXTENSION_DIRECTORY = PROJECT_DIRECTORY + "/src/backend/plugins"    #The extension directory is the absolute path to the folder which contains all the plugins


def filePath(pathInPlugins):
    '''
    For extensions that send files, they need to provide the messenger
    with the absolute path of the file that needs to be sent, it is sometimes 
    very tedious to find out what the absolute path is. This utility solves the
    problems by finding the absolute path of the plugins folder so all the user
    has to do is provide the path of the image within the plugins folder
    '''

    return f"{EXTENSION_DIRECTORY}/{pathInPlugins}"


def imageDownloader(savePath, fileUrl):
    '''
    For some extensions which may need to download an image from an API endpoint,
    this utility can be used to solve that problem, all the user as to do if provide
    the absolute path of where they want to save the file and the image URL
    '''
    
    with open(savePath, 'wb') as handle:
        image = requests.get(fileUrl, stream=True)

        for block in image.iter_content(1024):
            if not block:
                break
            handle.write(block)