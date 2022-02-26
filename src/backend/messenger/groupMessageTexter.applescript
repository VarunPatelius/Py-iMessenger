on run {targetGroupChatGUID, targetMessageToSend}
    tell application "Messages"
	    send targetMessageToSend to chat id targetGroupChatGUID
    end tell
end run