import requests
from utils.extensionUtils import filePath, imageDownloader


doggoHelp = "Returns a cute picture of a dog!"


def doggo(*args):
    response = requests.get("https://dog.ceo/api/breeds/image/random").json()
    fileUrl = response["message"]
    fileLocation = filePath("dog/doggo.jpg")

    imageDownloader(fileLocation, fileUrl)

    return fileLocation