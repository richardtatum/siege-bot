import discord
import random
import bs4
import requests
from settings import users

TOKEN = 'NDkwMTIyNjY1MzM2NTA0MzIy.Dn0uGQ.uokwSV1FgO39Id7exalxEB2AvE0'

client = discord.Client()


def data_request(message, author, id):
    # global casual
    # global waifu
    # global waifupicture
    # global profileurl
    # global username_web

    r = requests.get('https://r6stats.com/stats/{}/'.format(id)).text
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
            for row in card.select('.desktop-only'):
                for text in row.select('.stat-label'):
                    label.append(text.get_text())

                for text in row.select('.stat-count'):
                    count.append(text.get_text())
            data.append(dict(zip(label, count)))

    # for user in scrape.select('.username'):
    #     username_web = user.get_text()

    for mostplayed in scrape.select('.player-header__left-side'):
        waifu = str(mostplayed)
        waifupicture = str(waifu[waifu.find('src="')+5:waifu.find('"/><')])
        waifu = str(waifu[waifu.find('t="')+3:waifu.find('" src=')])

    for profile in scrape.select('.profile'):
        profile = str(profile)
        profileurl = str(profile[profile.find('src="')+5:profile.find('"/>')])

    total.append(dict(zip(cas_rank, data)))

    try:
        casual = total[0]['Casual Stats']
        kd = round(float(casual['K/D Ratio']), 2)
        wl = round(float(casual['W/L Ratio']), 2)
        return embed_creator(message, author, profileurl, casual['Time Played'], casual['Kills'], casual['Deaths'],
                             kd, wl, waifu, waifupicture)
    except:
        return error_message(message, author)


async def error_message(message, author):
    msg = 'I can\'t access the R6Stats site right now so I\'ll just guess your K/D instead.'
    msg2 = 'User {} has a KD of {} on Rainbow 6: Siege'.format(author, round(random.uniform(1, 5), 2))
    await client.send_message(message.channel, msg)
    await client.send_message(message.channel, msg2)


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
    await client.send_message(message.channel, embed=embed)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!insult'):
        msg = 'What the *fuck* is wrong with you {0.author.mention}?'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!stats'):
        msg = 'I checked your stats and honestly {0.author.mention}, they are so bad I don\'t want to print them...'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!test'):
        msg = 'Test message'
        await client.send_message(message.channel, msg)

    if message.content.startswith('!r6') or message.content.startswith('!R6'):
        print('>Stats check by ' + str(message.author))
        u = str(message.author)
        if u in users:
            username_local = users[u][0]
            id = users[u][2]
            await data_request(message, username_local, id)
        else:
            msg = 'I\'m afraid I don\'t have your ID stored for Rainbow 6. Please speak to Richard to get you added to the list.'
            await client.send_message(message.channel, msg)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
