""" This bot checks stats from the r6.leaderboards.io website and pastes them into Discord
when called.

Options:
    > !help - Provides a list of available commands.

Note:
The stats are accessed from r6.leaderboards.io by using the uPlay username,
an account with the website is required. Local usernames can be stored in
the 'users.py' file as a dictionary.
"""

import discord
import requests
from users import users
from discord.ext.commands import Bot
import os

client = Bot(command_prefix='!')  # The prefix used to summon the bot

# This is the Bot Token from Discord dev page
TOKEN = 'add_server_token_here'
API_URL = 'https://api.r6.leaderboards.io/user'


# API call to r6.leaderboards.io
# API Authorisation provided by the Leaderboards admin team
async def api_request(context, username):
    params = {
        'username': username,
        'authorization': os.environ['API_AUTH']
    }
    r = requests.get(url=API_URL, params=params)
    if r.status_code == 200:
        await embed_creator(context, r.json())
    else:
        if r.status_code == 404:
            msg = 'Stat request failed.'
            msg2 = 'It is likely you do not have an account at r6.leaderboards.io'
        else:
            msg = 'Stat request failed.'
            msg2 = f'Reason: {r.json()["message"]} - Status Code: {r.status_code}'
        await context.send(msg)
        await context.send(msg2)


# Embed creator takes the data from the JSON
# prettyfies the results and sends them as a message.
async def embed_creator(context, data):
    embed=discord.Embed(color=0xe3943c)
    embed.set_thumbnail(url=data['profile'])
    embed.add_field(name="Username", value=data['Username'], inline=True)
    embed.add_field(name="Time Played", value=data['Overall']['Time Played'], inline=True)
    embed.add_field(name="Kills", value=data['Overall']['Kills'], inline=True)
    embed.add_field(name="Deaths", value=data['Overall']['Deaths'], inline=True)
    embed.add_field(name="K/D Ratio", value=data['Overall']['K/D Ratio'], inline=True)
    embed.add_field(name="W/L %", value=data['Overall']['W/L Ratio'], inline=True)
    embed.add_field(name="Waifu", value=data['Overall']['Waifu'], inline=True)
    embed.add_field(name="Rank", value=data['Rank'], inline=True)
    embed.set_image(url=data['waifu_img'])
    embed.set_footer(text="*Want to see how your stats compare to your friends? \
    Head to r6.leaderboards.io*")
    await context.send(embed=embed)


# Callable command
@client.command(pass_context=True, aliases=['stats', 'Stats'])
async def r6(context):
    # Turns the author name into a string so it can be checked against the list
    u = str(context.message.author)  # Print for the log showing who triggered the bot.
    print(f'>Stats check by user {u}')
    if u in users:
        username_local = users[u][0]  # username_local stored for checking later
        await api_request(context, username_local)
    else:
        print('>Check failed. Is the username on the list?')
        msg = ('I\'m afraid I don\'t have your ID stored for Rainbow 6.'
               ' Please speak to the admin to get you added to the list.')
        await context.send(msg)


# Helpful message printed when the code is first run
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("with humans"))
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
