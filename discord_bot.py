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
import api
import settings
from users import users
from discord.ext.commands import Bot

client = Bot(command_prefix='!')  # The prefix used to summon the bot


async def user_request(context, username):
    response = api.user_request(username)
    if response["success"]:
        await compose_stats_message(context, reponse["message"])
    else:
        await context.send(response["message"])


async def challenge_request(context):
    response = api.challenge_request()
    if response["success"]:
        await compose_challenge_message(context, response["message"])
    else:
        await context.send(response["message"])


# Embed creator takes the data from the JSON
# prettyfies the results and sends them as a message.
async def profile_embed(context, data):
    embed = discord.Embed(color=0xe3943c)
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


# Embed creator takes the data from the JSON
# prettyfies the results and sends them as a message.
async def challenge_embed(context, data):
    embed = discord.Embed(title='This Weeks Challenges:', color=0xe3943c)
    embed.set_thumbnail(url=CHAL_ICON)
    for d in data:
        embed.add_field(name=d, value=data[d], inline=True)
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
        await user_request(context, username_local)
    else:
        print('>Check failed. Is the username on the list?')
        msg = ('I\'m afraid I don\'t have your ID stored for Rainbow 6.'
               ' Please speak to the admin to get you added to the list.')
        await context.send(msg)


# Callable command
@client.command(pass_context=True, aliases=['challenges', 'challenge'])
async def chall(context):
    # Turns the author name into a string so it can be checked against the list
    u = str(context.message.author)  # Print for the log showing who triggered the bot.
    print(f'>Challenges request by user {u}')
    await challenge_request(context)


# Helpful message printed when the code is first run
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("with humans"))
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
