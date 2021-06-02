from configparser import ConfigParser
from utils.setupUtils import PROJECT_DIRECTORY


reader = ConfigParser()
reader.read(f"{PROJECT_DIRECTORY}/src/backend/plugins/config.ini")


def retrieveKey(service, keyValue="key"):
    return reader[service][keyValue] #This function is accessible by all functions and allows them to load API keys and such