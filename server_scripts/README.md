# Server Scripts
This folder contains scripts needed to maintain the working environment for the r6stats discord bot.

## Scripts

### git-update.sh
This script is used to update the code from the GitLab repo using a deployment key and is run on a cron ever 5 minutes.
```bash
3-59/5 * * * * root sudo bash /opt/r6stats-discord-bot/server_scripts/git-update.sh
```
## Usage
To run this script manually, run the below command.
```bash
sudo bash /opt/r6stats-discord-bot/server_scripts/git-update.sh
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
