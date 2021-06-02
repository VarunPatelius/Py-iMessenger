from src.backend.manage import BackendThread    #This imports the backend component of Py-iMessenger
from src.frontend.interface import makeApp      #This imports the frontend component of Py-iMessenger


if __name__ == "__main__":
    makeApp(BackendThread)                      #The makeApp function generates the frontend with the backend connection