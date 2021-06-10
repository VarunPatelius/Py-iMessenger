pingHelp = "A simple extension to ensure that Py-iMessenger is online."
tingHelp = "A simple extension to ensure that Py-iMessenger is online."
wordyHelp = "An extension that can be used to multiply the word you give. Example: '/wordy,Hello,200' would repeat 'Hello' 200 times."


def ping(*args):
    return "Pong"


def wordMultiplier(*args):
    word = args[0]
    multiply = args[1]

    return word * int(multiply)


def ting(*args):
    return "Ping Cling Bing Hing Zing Ring"