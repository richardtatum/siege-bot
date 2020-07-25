# R6 Discord Bot

The bot pulls data from the [r6.leaderboards.io](https://r6.leaderboards.io) API and provides it in a nice embed within Discord.

## Prior Note
This is my first Discord Bot. There are many other R6 Stats bots out there that are probably infinitely better. This was simply a learning exercise and a cool little project.

For the API to correctly provide statistics, the user needs to have an account at [r6.leaderboards.io](https://r6.leaderboards.io). You will also require an API key which you can request through the [contact form](https://r6.leaderboards.io/contact).


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
    'Tatumkhamun#2312': ['Tatumkhamun']
}
```

### Server Token
Add the previously saved token into the `settings.py` file:

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
python3 run.py
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
>Stats check by user Tatumkhamun#2312

>Challenges request by user Tatumkhamun#2312
```

### Discord

If the bot is correctly up and running you can activate it with the following command:

```
!stats
```
Takes the users name and checks it against the list. If the name matches it will return stats based on the uPlay username submitted.

![](https://i.imgur.com/aGqwFIs.png)

```
!challenge/challenges
```
This provides a list of the current weeks challenges and their description.

![](https://i.imgur.com/2Lqcbls.png)


## Built With
* [Discord](https://discordpy.readthedocs.io/en/latest/index.html) - The framework used


## Authors

* **Richard Tatum** - *Initial work* - [RichardTatum](https://github.com/richardtatum)
* **Josh Edney** - *System architecture* - [JoshEdney](https://github.com/joshedney)
* **Chris Lowe** - *Code review* - [CSL619](https://github.com/csl619)

## License

This project is licensed under the MIT License.


## Acknowledgments

* Devdungeon for instructions on setting up the bot - [Dev_Dungeon](https://www.devdungeon.com)
* Countless other Rainbow Six: Siege bots out there that are infinitely better.
