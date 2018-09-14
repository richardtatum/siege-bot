import discord
from settings import users
import json
import requests
import random

TOKEN = 'NDkwMTIyNjY1MzM2NTA0MzIy.Dn0uGQ.uokwSV1FgO39Id7exalxEB2AvE0'

client = discord.Client()

def data_request(username, platform):
    x = yield from requests.get('https://api.r6stats.com/api/v1/players/{}?platform={}'.format(username, platform))
    json = yield from x.json()

    if x.status_code == 404:
        return None
    else:
        return json

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!insult'):
        msg = 'What the fuck is wrong with you {0.author.mention}?'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!stats'):
        msg = 'I checked your stats and honestly {0.author.mention}, they are so bad I don\'t want to print them...'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!test'):
        msg = 'Test message'
        client.send_message(message.channel, msg)

    if message.content.startswith('!r6'):
        print(message.author)
        u = str(message.author)
        if u in users:
            username = users[u][0]
            platform = users[u][1]
            try:
                msg2 = 'Stand by for kill data!'
                stats = data_request(username, platform)
                kd = str(stats['player']['stats']['casual']['kd'])
                msg = 'User {} has a KD of {} on Rainbow 6: Siege.'.format(username.title(), kd)
                await client.send_message(message.channel, msg2)
                await client.send_message(message.channel, msg)
            except:
                msg = 'I can\'t access the R6Stats API right now so I\'ll just guess your K/D instead.'
                msg2 = 'User {} has a KD of {} on Rainbow 6: Siege'.format(username.title(), round(random.uniform(1, 5), 3))
                await client.send_message(message.channel, msg)
                await client.send_message(message.channel, msg2)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
