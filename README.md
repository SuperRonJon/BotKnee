# BotKnee
Discord queue bot for sub games in QuartKnee's stream discord

## Commands
!q - Adds the sending user to the current queue of players

!remove - Removes the sending user from the current queue of players

!list - Lists the usernames of all players currently in the queue, in order

!swap @[user] - Initiates a swap with the tagged user. Both users must tag eachother with this command to swap spots

## Moderator commands
!next - Gets the next [number] players out of the queue, displays and mentions them in the channel

!number [value] - Sets the number of players to remove from the queue with the !next command, defaults to 3

!reset - Clears the current queue

!adduser @[mention] - adds the mentioned user to the current queue

!removeuser @[mention] - removes the mentioned user from the current queue

!tofront @[mention] - Moves the mentioned user to the front of the queue
