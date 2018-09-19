#!/bin/bash
# Script used to update code from the Gitlab repo.

cd /opt/r6stats-discord-bot
OLD_HEAD=`git rev-parse HEAD`

# Do a git pull with the correct key
ssh-agent bash -c 'ssh-add /opt/id_rsa; git pull'

NEW_HEAD=`git rev-parse HEAD`

if [ "$NEW_HEAD" != "$OLD_HEAD" ]; then
	# Restart the client
	systemctl stop r6bot
	systemctl start r6bot

fi
