#ENSURE THAT A KEY IS ADDED TO THE CONFIG.INI
import requests
from keyManager import retrieveKey


key = retrieveKey("news")
url = "https://newsapi.org/v2/top-headlines?"
parameters = {
    "country": "us",
    "category": "general",
    "apiKey": key,
}


newsHelp = "Brings up the top news headlines in the US. No args necessary"


def newsCollector(*args):
    try:
        response = requests.get(url, params=parameters)
        data = response.json()

        toSend = ""
        articles = data["articles"]

        for i in range(3):
            article = articles[i]

            title = article["title"]
            description = article["description"]

            toSend += f"{title}\n\t- {description}\n\n"

        return toSend
    except:
        return "The news could not be pulled up."