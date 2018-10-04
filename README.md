# R6 Discord Bot

The bot scrapes user data from r6.tracker.network and provides it in a nice embed within Discord.

## Installation

Simply clone the repository.

## Discord Prerequisites

### Create a Discord server.

If you don't already have a server, create one free one at https://discordapp.com. Simply log in, and then click the plus sign on the left side of the main window to create a new server.

### Create an app

Go to https://discordapp.com/developers/applications/me and create a new app. On your app detail page, save the Client ID. You will need it later to authorize your bot for your server.

### Create a bot account

After creating app, on the app details page, scroll down to the section named bot, and create a bot user. Save the token, you will need it later to run the bot.

### Authorise the bot account

Visit the URL https://discordapp.com/oauth2/authorize?client_id=XXXXXXXXXXXX&scope=bot but replace XXXX with your app client ID. Choose the server you want to add it to and select authorize.

## Code Prerequisites

### Modules

Install all the modules in `requirements.txt`:

```
pip install -r /path/to/requirements.txt
```

### Authorised users

Add any server members and their uPlay account names the `Users` section in `settings.py`:

```
users = {
    'discordusername#2312': ['uPlayusername'],
    'CSL619#8493': ['CSL619'],
    'FluffBunker#1757': ['FluffBunker'],
    'Arcanice#1327': ['Sharkie668']
}
```

### Server Token
Add the previously saved server token in `settings.py`:

```
production_token = 'xxxXxxXxx.xxxxx.xxxxxXXxxXXxXXXXx'
```

## Running the script & use within Discord

### Script

Run `discord_bot.py` once the prerequisites have been completed and you should be greeted with the following:

```
Logged in as:
BOTNAME
BOTID6337995776
------
```

Go to your server and make sure the bot is correctly logged in:

![Bot online](https://imgur.com/SJZuRQ0)

When the bot is activated by a user it will list a helpful message:

```
Logged in as:
BOTNAME
BOTID6337995776
------
>Stats check by user Tatumkhamun#2312 | Casual
```

Including if something didn't go to plan:

```
>Stats check by user Tatumkhamun#2312 | Idiot
>Check failed. 404 on the username.
```

### Discord

If the bot is correctly up and running you can activate it the following:

```
!r6 or !stats
```
Takes the users name and checks it against the list. If the name matches it will return casual stats based on the uPlay username submitted.
This defaults to casual stats.

![!stats](https://imgur.com/Xaa9WLP)

```
!r6/!stats followed by casual or ranked
```
Once again checks the username against the list and if it matches it will return the requested statistics.

![!stats ranked](https://imgur.com/JV6pbqx)

```
!r6/!stats followed by a username
```
Searches for the username on the stats website, and returns their casual stats if possible. Otherwise returns an error message.

![!stats CSL619](https://imgur.com/KE7I8dg)


## Built With
* [Discord](https://discordpy.readthedocs.io/en/latest/index.html) - The framework used
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - For working through scraped HTML



## Authors

* **Richard Tatum** - *Initial work* - [TTKMHN](https://gitlab.com/TTKMHN)
* **Josh Edney** - *Server scripts* - [FluffBunker](https://gitlab.com/FluffBunker)
* **Chris Lowe** - *Code Review* - [CSL619](https://gitlab.com/CSL619)

## License

This project is licensed under the MIT License.


## Acknowledgments

* Devdungeon for instructions on setting up the bot - [Dev_Dungeon](https://www.devdungeon.com)
* Countless other Rainbow Six: Siege bots out there
* etc
