nameHelp = "Save your name with this extension. Example: /name,Johnny"
identityHelp = "Returns a name that has been saved with /name"


def setName(*args):
    if len(args) == 1:
        return "Enter a name to save"

    nameToSave = args[0]
    userObject = args[-1]

    try:
        userObject.name = nameToSave
    except AttributeError:
        userObject.addAttribute(attributeName="name", attributeValue=nameToSave)

    userObject.saveChanges()
    return "Your name has been stored!"


def whoAmI(*args):
    userObject = args[-1]

    try:
        message = f"Your name is {userObject.name}"
        return message
    except AttributeError:
        return "Your name could not be found, set a name using the /name command"