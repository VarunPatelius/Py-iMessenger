(*
This file is used for sending messages to groupchats using Applescript
it takes the message and the id of the groupchat
*)

on run {targetGroupChatGUID, targetMessageToSend}               #When the file is called, ask for the groupchat ID and the message to send
    tell application "Messages"
	    send targetMessageToSend to chat id targetGroupChatGUID #Send
    end tell
end run