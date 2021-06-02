makeHelp = "This command is used to create your todo list. Example: /makeTodo,chores,homework,read"
todoHelp = "This command will return any existing todo list"
addHelp = "Use this command to add one or multiple items to an existing todo list. Example: /add,eat,sleep"
removeHelp = "Use this command to remove an item from an existing todo list using its corresponding number. Example: /remove,1 (first item)"
clearHelp = "Used to clear an entire todo list"


def makeToDoList(*args):
    if len(args) == 1:
        return "You need to pass the items you would like in your todo list"

    thingsToDo = args[:-1]
    userObject = args[-1]

    saveValue = list(thingsToDo)

    returnMessage = "You've successfully made a to-do list with the following items: "
    for position, thing in enumerate((thingsToDo), 1):
        returnMessage += f"\n\n {position}. {thing}"

    try:
        userObject.todo = saveValue
    except AttributeError:
        userObject.addAttribute(attributeName="todo", attributeValue=saveValue)

    userObject.saveChanges()
    return returnMessage


def returnToDo(*args):
    userObject = args[-1]

    returnMessage = "Your Todo List:"
    try:
        savedToDo = userObject.todo
        for position, thing in enumerate((savedToDo), 1):
            returnMessage += f"\n\n {position}. {thing}"
        return returnMessage

    except AttributeError:
        return "It seems you haven't made a todo list yet. You can make one with /makeTodo,<args>"


def addItem(*args):
    if len(args) == 1:
        return "You need to pass the items you would like in your todo list"

    userObject = args[-1]
    thingsToAdd = args[:-1]

    returnMessage = "Additions have been made to your todo list, it is now:"
    try:
        for item in thingsToAdd:
            userObject.todo.append(item)
            
        savedToDo = userObject.todo
        for position, thing in enumerate((savedToDo), 1):
            returnMessage += f"\n\n {position}. {thing}"
        userObject.saveChanges()
        return returnMessage

    except AttributeError:
        return "It seems you haven't made a todo list yet. You can make one with /makeTodo,<args>"



def removeItem(*args):
    if len(args) > 2:
        return "Ensure you are only passing in the corresponding number of one item"

    userObject = args[-1]
    itemToRemove = args[0]

    returnMessage = "After removing the item, your todo list is:"
    try:
        indexToRemove = int(itemToRemove) - 1
        del userObject.todo[indexToRemove]

        toDo = userObject.todo
        for position, thing in enumerate((toDo), 1):
            returnMessage += f"\n\n {position}. {thing}"
        userObject.saveChanges()
        return returnMessage

    except (ValueError, IndexError, AttributeError, TypeError) as error:
        return "Ensure you are entering a corrected item number to remove and that a todo list exists."



def clearList(*args):
    userObject = args[-1]

    clearedMessage = "Your todo list has now been cleared"
    try:
        userObject.todo = []
        userObject.saveChanges()
        return clearedMessage

    except AttributeError:
        return "It seems you haven't made a todo list yet. You can make one with /makeTodo,<args>"