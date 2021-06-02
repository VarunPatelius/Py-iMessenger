(*
This file is used for sending files via AppleScript, it simply needs to be 
given the phone number and the absolute path of the file to send to
*)

on run {targetPhoneNumber, targetFileToSend}                            #When the file is called, ask for the phone number and absolute file path
    tell application "Messages"             
        set targetService to 1st service whose service type = iMessage  #Enable iMessage as the messaging service of choice
        set targetBuddy to buddy targetPhoneNumber of targetService     #Set the phone number to the one the user passed in
        set targetMessage to (targetFileToSend as POSIX file)           #Set the inteded message as the file
        send targetMessage to targetBuddy                               #Send the message
    end tell
end run