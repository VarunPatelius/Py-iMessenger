(*
This file is used for sending files via AppleScript, it simply needs to be 
given the phone number and the absolute path of the file to send to.
This uses GUI programming to get around the fact that Applescript
is broken in MacOS Monterey.
*)

on run {targetPhoneNumber, targetFileToSend}    #When the file is called, ask for the phone number and absolute file path
	tell application "System Events" to set targetMessage to (targetFileToSend as POSIX file)
	
	tell application "Messages"                 #Open Messages application to type in details
		activate
	end tell
	
	tell application "System Events" to tell application process "Messages"
		keystroke "n" using {command down}	    #This command opens a new message tab
		delay 0.8
		keystroke targetPhoneNumber			    #The reciepient's number is typed in
		delay 0.2
		keystroke return
		delay 0.2
		keystroke tab
		delay 0.2
		set the clipboard to targetMessage	    #The file is then pasted in
		keystroke "v" using {command down}
		delay 0.3
		keystroke return					    #Message is sent
	end tell
end run