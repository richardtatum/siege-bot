""" This bot checks stats from the R6Stats website and pastes them into Discord
when called.

Options:
    > !help - Provides a list of available commands.

Note:
The stats are accessed from R6Stats by using the unique identifier assigned to
each user (see 'id'). This is stored in the settings.py file.
"""

import discord
import random
import bs4
import requests
from settings import users
from discord.ext.commands import Bot
from discord import Game

BOT_PREFIX = ('!')
client = Bot(command_prefix=BOT_PREFIX)

# This is the Bot Token from Discord.
TOKEN = 'NDkwMTIyNjY1MzM2NTA0MzIy.Dn0uGQ.uokwSV1FgO39Id7exalxEB2AvE0'


# Webscraper function, with required arguments passed from the call.
def data_request(context, casual_ranked, author):
    # Here the unique identifier is input into the URL to get the correct page
    # r = requests.get('https://r6.tracker.network/profile/pc/sharkie668')
    r = requests.get('https://r6.tracker.network/profile/pc/{}'.format(author.lower()))
    scrape = bs4.BeautifulSoup(r.text, 'html.parser')

    label = []  # Blank list for the stat labels
    count = []  # Blank list for the stat numbers
    data = []  # Blank list for the combination of the two previous
    cas_rank = []  # Blank list stores casual/ranked stats
    total = []  # Blank list for the zip total of all lists

    # Webscraper passes through classes picking up the correct information
    # And assigns them to the blank lists for manipulation later.
    for element in scrape.select('.r6-pvp-grid'):
        for c_r in element.select('.trn-card__header'):
            cas_rank.append(c_r.get_text(strip=True))

        for stats_type in element.select('.trn-card__content'):
            for stats_list in stats_type.select('.trn-defstats'):
                for stat_label in stats_list.select('.trn-defstat__name'):
                    label.append(stat_label.get_text(strip=True))
                for stat_count in stats_list.select('.trn-defstat__value'):
                    count.append(stat_count.get_text(strip=True))
                    # strip=True removes the '\n' new lines present in the list
            data.append(dict(zip(label, count)))

    # Takes all the data and zips into one easy to use dict.
    total.append(dict(zip(cas_rank, data)))

    # Pulls the users uPlay profile image
    for profile in scrape.select('.trn-profile-header__avatar'):
        for link in profile.find_all('img', src=True):
            link = str(link)
            # Strips the string of unnecessary characters and leaves the image url
            profileurl = str(link[link.find('src="')+5:link.find('"/>')])

    # Pulls the name of the most played character from inside an image link.
    for mostplayed in scrape.select('.trn-defstat__value'):
        for source in mostplayed.find_all('img', src=True, limit=1):
            source = str(source)
            # Strips the string of unnecessary characters and leaves the Operator name
            waifu = str(source[source.find('title="')+7:source.find('"/>')]).title()
            # Takes the operator name and adds it to a URL to pull a picture of that Op
            waifupicture = 'https://cdn.r6stats.com/figures/{}_figure.png'.format(waifu.lower())

    try:
        # Pulls the request for casual or ranked stats. Defaulting to casual
        # if no argument is provided
        requested_cas_rank = total[0]['{}'.format(casual_ranked.title())]
        # If the user has not played ranked/casual then the 'Time Played' stat
        # is blank. This checks the length and makes it 0 if nothing is there
        if len(requested_cas_rank['Time Played']) == 0:
            requested_cas_rank['Time Played'] = 0

        # Passes all information to the embed_creator for message creation.
        return embed_creator(context, casual_ranked, author, profileurl,
                             requested_cas_rank['Time Played'], requested_cas_rank['Kills'],
                             requested_cas_rank['Deaths'], requested_cas_rank['KD'],
                             requested_cas_rank['Win %'], waifu, waifupicture)

    except:
        # If the webscraper hasn't collect the correct information, return error.
        print('>Check failed. Make sure username is correct?')
        return error_message(context, author)


# A fun way of distracting the user if the webscrape fails.
# round(random) function used to pick a float between 1-5 and round to 2 decimal points.
async def error_message(context, author):
    msg = 'I can\'t access the R6Tracker site right now so I\'ll just guess your K/D instead.'
    msg2 = 'User {} has a KD of {} on Rainbow 6: Siege'.format(author, round(random.uniform(1, 5), 2))
    await client.send_message(context.message.channel, msg)
    await client.send_message(context.message.channel, msg2)


# Embed creator takes the variables established in the webscraper
# prettyfies the results and sends them as a message.
async def embed_creator(context, casual_ranked, username, profileurl, timeplayed, kills, deaths, kd, wl, waifu, waifupicture):
    embed=discord.Embed(title="R6 Stats Checker | {}".format(casual_ranked.title()), color=0xe3943c)
    embed.set_thumbnail(url=profileurl)
    embed.add_field(name="Username", value=username, inline=True)
    embed.add_field(name="Time Played", value=timeplayed, inline=True)
    embed.add_field(name="Kills", value=kills, inline=True)
    embed.add_field(name="Deaths", value=deaths, inline=True)
    embed.add_field(name="K/D Ratio", value=kd, inline=True)
    embed.add_field(name="W/L %", value=wl, inline=True)
    embed.add_field(name="Waifu", value=waifu, inline=False)
    embed.set_image(url=waifupicture)
    embed.set_footer(text="*Is there something wrong with this bot? Please let us know by \
    emailing tough.shit@codeishard.com.*")
    await client.send_message(context.message.channel, embed=embed)


# Fun 8Ball call that pulls from a random set of responses.
@client.command(name='8ball',  # Sets the value to call
                brief='Answers Yes/No questions',  # Brief supplied when !help is called
                description='Returns an 8Ball answer',  # Extended explaination when !help 8ball is called
                aliases=['eight_ball', '8-ball'],  # Alternative values that can be used
                pass_context=True)  # Passes the client information (username etc)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    # Picks a random option from the respose and posts that along with the users name.
    await client.say(random.choice(possible_responses) + ', ' + context.message.author.mention)


# R6 stats checker
@client.command(pass_context=True,
                aliases=['R6', 'stats', 'Stats'],
                brief='Use the variable casual/ranked',
                description='Provides stats from the R6Stats website')
async def r6(context, casual_ranked='casual'):
    # Turns the author name into a string so it can be checked against the list.
    u = str(context.message.author)
    # Console print for the log, so you can see who has triggered the bot.
    print('>Stats check by user ' + u + ' | ' + casual_ranked.title())
    # Checks if the argument called is either of the accepted ones.
    if casual_ranked.lower() == 'casual' or casual_ranked.lower() == 'ranked':
        # If the author is present in the list, continue with codeself.
        # Otherwise this author hasn't been created. Prompt contact with admin.
        if u in users:
            username_local = users[u][0]  # Username_local stored for checking later
            # Pass this information to the data_request() func.
            await data_request(context, casual_ranked, username_local)
        else:
            print('>Check failed. Is the username on the list?')
            msg = 'I\'m afraid I don\'t have your ID stored for Rainbow 6. Please speak to Richard to get you added to the list.'
            await client.say(msg)
    # If the argument is not one of the two accepted, throws a helpful error message.
    else:
        print('>Stats check failed. Incorrect argument')
        msg = 'Ahh, not quite {}. Please try again.'.format(context.message.author.mention)
        msg2 = '`!R6` takes only `casual` or `ranked` as arguments.'
        await client.say(msg)
        await client.say(msg2)


# Helpful message printed when the code is first run
@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(client.get_channel('476357549126582272'), 'R6 BOT UPDATED.')
    await client.send_message(client.get_channel('476357549126582272'), 'INITIALISING...')
    await client.send_message(client.get_channel('476357549126582272'), 'https://giphy.com/gifs/style-power-mech-4Kn78njYS85W0')
    await client.send_message(client.get_channel('476357549126582272'), 'R6BOT IS BACK BABY. CHECK YO\' SELF.')

client.run(TOKEN)
