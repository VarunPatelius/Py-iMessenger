from simple.simpleLogic import ping, ting, wordMultiplier, pingHelp, tingHelp, wordyHelp
from news.newsLogic import newsCollector, newsHelp
from todo.todoLogic import clearList, addItem, removeItem, returnToDo, makeToDoList, makeHelp, todoHelp, addHelp, removeHelp, clearHelp
from name.nameLogic import setName, whoAmI, nameHelp, identityHelp
from dog.dogLogic import doggo, doggoHelp
from flags.flagLogic import patriotism, usHelp
#All of the above are different command functions which need to be registered with the messenger object


def loadExtensions(messengerObject):
    '''
    This function is passed in the main messaging client object and then will register all of the
    extensions/plugins with the messenger object
    '''

    messengerObject.addExtension(commandName="/ping", commandFunction=ping, commandHelp=pingHelp)
    messengerObject.addExtension(commandName="/wordy", commandFunction=wordMultiplier, commandHelp=wordyHelp)
    messengerObject.addExtension(commandName="/ting", commandFunction=ting, commandHelp=tingHelp)

    messengerObject.addExtension(commandName="/usnews", commandFunction=newsCollector, commandHelp=newsHelp)

    messengerObject.addExtension(commandName="/makeTodo", commandFunction=makeToDoList, commandHelp=makeHelp)
    messengerObject.addExtension(commandName="/todo", commandFunction=returnToDo, commandHelp=todoHelp)
    messengerObject.addExtension(commandName="/add", commandFunction=addItem, commandHelp=addHelp)
    messengerObject.addExtension(commandName="/remove", commandFunction=removeItem, commandHelp=removeHelp)
    messengerObject.addExtension(commandName="/clear", commandFunction=clearList, commandHelp=clearHelp)

    messengerObject.addExtension(commandName="/name", commandFunction=setName, commandHelp=nameHelp)
    messengerObject.addExtension(commandName="/whoami", commandFunction=whoAmI, commandHelp=identityHelp)

    messengerObject.addExtension(commandName="/doggo", commandFunction=doggo, commandHelp=doggoHelp, files=True)

    messengerObject.addExtension(commandName="/patriot", commandFunction=patriotism, commandHelp=usHelp, files=True)