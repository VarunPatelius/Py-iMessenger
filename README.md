# Py-iMessenger
Py-iMessenger is a chatbot that works with iMessage to execute commands using text messages.
![Home Page](https://github.com/VarunPatelius/Py-iMessenger/blob/main/github/logos/mainBanner.png?raw=true)

## About
Py-iMessenger is a simple chatbot that is powered by Python and Applescript. By reading from the iMessage database on MacOS devices, Py-iMessenger allows developers to create extensions that can do various tasks such as sending files, pulling up the recent news, or adding to a todo list. These extensions can be accessed by users simply through texting.

Py-iMessenger's frontend design takes inspiration from Zeke Snider's [Jared](https://github.com/ZekeSnider/Jared), however the backend was written by myself in Python.

## Installation
The following steps show how to get Py-iMessenger up and running.

**Be advised, Py-iMessenger is only compatible with MacOS devices which support iMessage, iMessage must be enabled to for the program to run. Running this program on a Windows or Linux device will result in an error message**

1. Begin by cloning or downloading the .zip file to your MacOS device
2. Change directory into the cloned/downloaded folder
```bash
cd PATH/TO/FOLDER/Py-iMessenger
```
3. Create a virtual environment within the folder 
```bash
python3 -m venv venv (or any name you want to give to the virtual environment)
```
4. Activate the virtual environment
```bash
source venv/bin/activate
```
5. Install all the dependencies necessary for Py-iMessenger
```bash
pip3 install -r requirements.txt
```
6. Run the program
```bash
python3 main.py
```
* If you see an error that means that either the terminal or your IDE do not have "Full Disk Access", to remedy this click on the Apple logo on the top left of your screen, click "System Preferences", select "Security & Privacy", use the scroll bar on the left to find and click "Full Disk Access", select the lock icon at the bottom to allow changes and give full disk access to your terminal or IDE.

![Disk Perms](https://github.com/VarunPatelius/Py-iMessenger/blob/main/github/setup/diskAccessGIF.gif?raw=true)

* The program you are using to run the program (terminal/IDE) may also ask you for permissions to control the Messages app, allow this.

![Message Perms](https://github.com/VarunPatelius/Py-iMessenger/blob/main/github/setup/messagePerms.png?raw=true)

## Usage
Py-iMessenger supports sending both messages and files:

![Messenger Demo](https://github.com/VarunPatelius/Py-iMessenger/blob/main/github/usage/messengerDemo.gif?raw=true)


## Technologies
* [AppleScript](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/introduction/ASLR_intro.html) - Used to control iMessage
* [SQLite3](https://docs.python.org/3/library/sqlite3.html) - Used to read the iMessage database
* [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - Used to create frontened

## Helpful Tips
When Py-iMessenger runs for the first time, all user data will be automatically loaded into _src/backend/user/savedUser.json_
along with a couple other config files for things such as API keys and the settings UI, to stop these config files from showing up
when doing "git status", it would be wise to run the following commands in the project directory:

```bash
> git update-index --skip-worktree src/backend/user/savedUser.json
> git update-index --skip-worktree src/backend/plugins/config.ini
> git update-index --skip-worktree src/frontend/settings/configUi.ini
```

## Documentation
Documentation regarding how the program works, how to create an extension, and how to use the multitude of features that Py-iMessenger gives to develops, check out the [YouTube playlist](https://www.youtube.com/playlist?list=PLNtd-r4MGC3eL4dsinuG-RB1gMV5QGbsl)

## Acknowledgments
_A special thanks to Annelis Irigoyen for creating the logo._

## License
Py-iMessenger uses the GNU Affero General Public License v3.0 

More details regarding this license can be found [here](https://choosealicense.com/licenses/agpl-3.0/).