#!/bin/bash
# Script used to update code from the Gitlab repo.

# Change working directory.
cd /opt/r6stats-discord-bot

# Check to see if the log directory exists.
if [[ ! -d /opt/r6stats-discord-bot/log/ ]]; then
	# Create the log directory
	mkdir /opt/r6stats-discord-bot/log
fi

# Old version
OLD_HEAD=`git rev-parse HEAD`

# Do a git pull with the correct key and log the response.
ssh-agent bash -c 'ssh-add /opt/id_rsa; OUTCOME=$(git pull); TIMESTAMP=$(date); echo ${TIMESTAMP} "-" ${OUTCOME}' >> /opt/r6stats-discord-bot/log/update.log

# New version
NEW_HEAD=`git rev-parse HEAD`

# Check to see if it is newer.
if [ "$NEW_HEAD" != "$OLD_HEAD" ]; then
	# Restart the client
	systemctl stop r6bot
	systemctl start r6bot
fi
