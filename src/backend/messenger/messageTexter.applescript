(*
This file is used for sending messages via AppleScript, it simply needs to be 
given the phone number and the message that the user would like to send out
*)

on run {targetPhoneNumber, targetMessageToSend}                         #When the file is called, ask for a phone number and the message that needs to be sent
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage  #Enable iMessage as the messaging service of choice
        set targetBuddy to buddy targetPhoneNumber of targetService     #Set the phone number to the one the user passed in
        set targetMessage to targetMessageToSend                        #Set the inteded message as the message that was passed in
        send targetMessage to targetBuddy                               #Send the message
    end tell
end run