import discord
import json
import requests
import random
import bs4
from robobrowser import RoboBrowser
from settings import users

TOKEN = 'NDkwMTIyNjY1MzM2NTA0MzIy.Dn0uGQ.uokwSV1FgO39Id7exalxEB2AvE0'

client = discord.Client()


def data_request(author, id):
    br = RoboBrowser()
    br.open('https://r6stats.com/stats/{}/'.format(id))
    r = str(br.parsed)

    scrape = bs4.BeautifulSoup(r, 'html.parser')

    label = []
    count = []
    data = []
    cas_rank = []
    total = []

    for element in scrape.select('.stats-center'):
        for stats_type in element.select('.card__title'):
            if stats_type.get_text() == 'Casual Stats' or \
                    stats_type.get_text() == 'Ranked Stats':
                cas_rank.append(stats_type.get_text())
        for card in element.select('.card__content'):
            # print(card)
            for row in card.select('.desktop-only'):
                for text in row.select('.stat-label'):
                    label.append(text.get_text())

                for text in row.select('.stat-count'):
                    count.append(text.get_text())
            data.append(dict(zip(label, count)))

    total.append(dict(zip(cas_rank, data)))
    ranked_stats = total[0]['Ranked Stats']
    casual_stats = total[0]['Casual Stats']
    print(casual_stats)

    message_format(author, casual_stats)


def message_format(author, casual):
    try:
        msg = 'Standby for kill data!'
        msg2 = 'User {} has the following stats: \n \
                Time played: {} \n \
                Kills: {} \n \
                Deaths: {} \n \
                K/D: {} \n \
                W/l: {}'.format(user, casual[0], casual[1], casual[2], casual[3], casual[6])

        return msg
        return msg2

    except:
        msg = 'I can\'t access the R6Stats API right \
               now so I\'ll just guess your K/D instead.'
        msg2 = 'User {} has a KD of {} on Rainbow 6: Siege'.format(author, round(random.uniform(1, 5), 3))
        return msg
        return msg2


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
            id = users[u][2]
            data_request(message.author, id)
            msg, msg2 =
            await client.send_message(message.channel, msg)
            await client.send_message(message.channel, msg2)




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
