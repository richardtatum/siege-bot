# R6 Discord Bot

The bot scrapes user data from r6.tracker.network and provides it in a nice embed within Discord.

## Prior Note
This is my first Discord Bot. There are many other R6 Stats bots out there that are probably infinitely better. This was simply a learning exercise and a cool little project.


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

This script requires Python 3.6 or above.

### Modules

Install all the modules in `requirements.txt`:

```
pip3 install -r /path/to/requirements.txt
```

### Authorised users

Add any server members and their uPlay account names the `users` dictionary in `users.py`:

```python
users = {
    'discordusername#2312': ['uPlayusername'],
    'CSL619#8493': ['CSL619'],
    'FluffBunker#1757': ['FluffBunker'],
    'Arcanice#1327': ['Sharkie668']
}
```

### Server Token
Add the previously saved token into the top of the `discord_bot.py` file:

```python
TOKEN = 'add_server_token_here'
```
Becomes something like this:

```python
TOKEN = 'motzzJezVPNZyF2NTA0MzIy.Dn0uGQ.rtrAEZIZNSZfWasAtrSDWJkaBIB'
```
(Do not use the above token, it's a dud! Make sure it is the one you copied from the `Bot` page from the Discord developer website.)


## Running the script & use within Discord

### Script

Run:

```
python3 discord_bot.py
```
in the terminal, once the prerequisites have been completed, and you should be greeted with the following:

```
Logged in as:
BOTNAME
BOTID6337995776
------
```

Go to your server and make sure the bot is correctly logged in:

![](https://imgur.com/SJZuRQ0.png)

When the bot is activated by a user it will print a helpful message in the terminal:

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

If the bot is correctly up and running you can activate it with the following command:

```
!r6 or !stats
```
Takes the users name and checks it against the list. If the name matches it will return stats based on the uPlay username submitted.
This defaults to `general` stats.

![](https://imgur.com/p8TR7Qr.png)

```
!r6/!stats followed by general, casual or ranked
```
Once again checks the username against the list and if it matches it will return the requested statistics.

![](https://imgur.com/JV6pbqx.png)

```
!r6/!stats followed by a username
```
Searches for the username on the stats website, and returns their `general` stats if possible. Otherwise returns an error message.

![](https://imgur.com/7SY1oaw.png)

```
!r6/!stats followed by a username, followed by general, casual or ranked
```
Once again checks the username on the stats website,and if it matches it will return the requested statistics.

![](https://imgur.com/BHIZrOv.png)

## Built With
* [Discord](https://discordpy.readthedocs.io/en/latest/index.html) - The framework used
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - For working through scraped HTML



## Authors

* **Richard Tatum** - *Initial work* - [RichardTatum](https://github.com/richardtatum)
* **Josh Edney** - *System architecture* - [JoshEdney](https://github.com/joshedney)
* **Chris Lowe** - *Code review* - [CSL619](https://github.com/csl619)

## License

This project is licensed under the MIT License.


## Acknowledgments

* Devdungeon for instructions on setting up the bot - [Dev_Dungeon](https://www.devdungeon.com)
* Countless other Rainbow Six: Siege bots out there that are infinitely better.
