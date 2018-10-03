
from discord.ext.commands import Bot
import random
import discord
import requests
import bs4
from settings import users

TOKEN = 'NDkyMjYyMjM2MzM3OTk1Nzc2.DoT2kw.sb5pzw18Icds8uqszA4Y1plUfiM'
BOT_PREFIX = ('!')

client = Bot(command_prefix=BOT_PREFIX)


def data_request(message, casual_ranked, author, id):
    # Here the unique identifier is input into the URL to get the correct page
    r = requests.get('https://r6stats.com/stats/{}/'.format(id)).text
    scrape = bs4.BeautifulSoup(r, 'html.parser')

    label = []  # Blank list for the stat labels
    count = []  # Blank list for the stat numbers
    data = []  # Blank list for the combination of the two previous
    cas_rank = []  # Blank list stores casual/ranked stats
    total = []  # Blank list for the zip total of all lists

    # Webscraper passes through classes picking up the correct information
    # And assigns them to the blank lists for manipulation later.
    for element in scrape.select('.stats-center'):
        for stats_type in element.select('.card__title'):
            if stats_type.get_text() == 'Casual Stats' or \
                    stats_type.get_text() == 'Ranked Stats':
                cas_rank.append(stats_type.get_text())
        for card in element.select('.card__content'):
            for row in card.select('.desktop-only'):
                for text in row.select('.stat-label'):
                    label.append(text.get_text())

                for text in row.select('.stat-count'):
                    count.append(text.get_text())
            data.append(dict(zip(label, count)))

    # Takes all the data and zips into one easy to use dict.
    total.append(dict(zip(cas_rank, data)))

    # Grabs the username from the website, for use in checking against the
    # stored username taken earlier. This helps prevent a bug where the website
    # would display someone elses information if the ID was unaccessable.
    for user in scrape.select('.username'):
        username_web = user.get_text()

    # Pulls the name of the most played character from inside an image link.
    for mostplayed in scrape.select('.player-header__left-side'):
        waifu = str(mostplayed)

        # Strips the string of unnecessary characters and leaves the image link
        waifupicture = str(waifu[waifu.find('src="')+5:waifu.find('"/><')])

        # Strips the string of unnecessary characters and leaves the Operator name
        waifu = str(waifu[waifu.find('t="')+3:waifu.find('" src=')])

    # Pulls the users uPlay profile image
    for profile in scrape.select('.profile'):
        profile = str(profile)

        # Again strips unnecessary characters and leaves the image link
        profileurl = str(profile[profile.find('src="')+5:profile.find('"/>')])

    try:
        # Checks the username scraped from the website against the locally stored
        # name in settings.py to make sure we aren't posting someone elses details
        if author.lower() == username_web.lower():
            # If the usernames are the same, pick the casual stats from the total dict
            stats_CR = total[0]['{} Stats'.format(casual_ranked.title())]

            # Rounds the K/D & W/L numbers to 2 decimal points for easy digestion
            kd = round(float(stats_CR['K/D Ratio']), 2)
            wl = round(float(stats_CR['W/L Ratio']), 2)

            # Passes all information to the embed_creator for message creation.
            return embed_creator(message, author, profileurl, stats_CR['Time Played'],
                                 stats_CR['Kills'], stats_CR['Deaths'], kd, wl, waifu,
                                 waifupicture)
        else:
            # If the usernames don't match, return an error message
            return error_message(message, author)

    except:
        # If the webscraper hasn't collect the correct information, return error.
        return error_message(message, author)


async def error_message(message, author):
    msg = 'I can\'t access the R6Stats site right now so I\'ll just guess your K/D instead.'
    msg2 = 'User {} has a KD of {} on Rainbow 6: Siege'.format(author, round(random.uniform(1, 5), 2))
    await client.send_message(message.channel, msg)
    await client.send_message(message.channel, msg2)


@client.command(name='8ball',
                brief='Answers with 8Ball answer',
                description='Use this to ask stupid questions',
                aliases=['eight_ball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ', ' + context.message.author.mention)


@client.command(pass_context=True,
                aliases=['R6', 'stats', 'Stats'],
                brief='Use the variable casual/ranked',
                description='Provides stats from the R6Stats website')
async def r6(context, casual_ranked='casual'):
    u = str(context.message.author)
    print('>Stats check by user ' + u)
    if casual_ranked.lower() == 'casual' or casual_ranked.lower() == 'ranked':
        if u in users:
            username_local = users[u][0]
            id = users[u][2]
            await data_request(context, casual_ranked, username_local, id)
    else:
        print('>Stats check failed')
        msg = 'Ahh, not quite {}. Please try again.'.format(context.message.author.mention)
        msg2 = 'Please note `!R6` takes only `casual` or `ranked` as arguments.'
        await client.say(msg)
        await client.say(msg2)


async def embed_creator(message, username, profileurl, timeplayed, kills, deaths, kd, wl, waifu, waifupicture):
    embed=discord.Embed(title="R6 Stats Checker", color=0xe3943c)
    embed.set_thumbnail(url=profileurl)
    embed.add_field(name="Username", value=username, inline=True)
    embed.add_field(name="Time Played", value=timeplayed, inline=True)
    embed.add_field(name="Kills", value=kills, inline=True)
    embed.add_field(name="Deaths", value=deaths, inline=True)
    embed.add_field(name="K/D Ratio", value=kd, inline=True)
    embed.add_field(name="W/L Ratio", value=wl, inline=True)
    embed.add_field(name="Waifu", value=waifu, inline=False)
    embed.set_image(url=waifupicture)
    embed.set_footer(text="*Is there something wrong with this bot? Please let us know by emailing tough.shit@codeishard.com.*")
    await client.send_message(message.message.channel, embed=embed)


@client.event
async def on_message_delete(message):
    msg = 'Woah, woah, woah. You think you can just change the official records round here {0.author.mention}?'.format(message)
    msg2 = 'If I catch you deleting things again, me and you are going to have words.'
    await client.send_message(message.channel, msg)
    await client.send_message(message.channel, msg2)


@client.command(pass_context=True)
async def square(context, number):
    square_number = int(number) * int(number)
    await client.say('It\'s ' + str(square_number) + ' ' + context.message.author.mention)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
client.run(TOKEN)
