import random
import os
import discord
import aiohttp
from discord.ui import Button, View
from dotenv import load_dotenv
from dcactivity import DCActivity
from discord.ext import commands
from discord_together import DiscordTogether

client = commands.Bot(command_prefix = '>', help_command=None, case_insensitive=True)
dcactivity = DCActivity(client)

load_dotenv()
TOKEN = os.getenv("UNSEEBOT_TOKEN")

@client.event
async def on_ready():
    client.togetherControl = await DiscordTogether(TOKEN)
    print("If you are seeing this then unseeyou's epic bot is working!")
    await client.change_presence(activity=discord.Game('With your mind - >help'))

client.load_extension("cogs.bettermusic")
client.load_extension("cogs.meme")

@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, this command does not exist. Contact unseeyou#2912 if you think this should be added.")

@client.command(pass_context=True)
async def unseebot(ctx):
    await ctx.send('Check your dms!')
    await ctx.message.author.send("Hi! I'm unseebot, a bot made by unseeyou. Please feel free to report any issues to unseeyou via dms. Thanks!")

@client.command()
async def yt(ctx):
    link = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
    await ctx.send(f"Click on the blue link to start the event!\n{link}")

@client.command(aliases=['doggo', 'dogs', 'dogfacts', 'dogfact', 'pup', 'pupper', 'puppy'])
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()
        request2 = await session.get('https://some-random-api.ml/facts/dog')
        factjson = await request2.json()
    dogbed = discord.Embed(title='DOGGY', colour=discord.Colour.dark_gold())
    dogbed.set_image(url=dogjson['link'])
    dogbed.set_footer(text=factjson['fact'])
    await ctx.send(embed=dogbed)

@client.command(aliases=['kitty', 'kitten', 'meow', 'catfact', 'catfacts'])
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        request1 = await session.get('https://some-random-api.ml/img/cat')
        catjson = await request1.json()
        request22 = await session.get('https://some-random-api.ml/facts/cat')
        factjson1 = await request22.json()
    catty = discord.Embed(title='KITTY', colour=discord.Colour.dark_gold())
    catty.set_image(url=catjson['link'])
    catty.set_footer(text=factjson1['fact'])
    await ctx.send(embed=catty)

@client.command(pass_context=True)
async def id(ctx):
    id = ctx.message.guild.id
    await ctx.send(id)

@client.command()
async def betrayal(ctx):
    invite = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'betrayal')
    await ctx.send(f'click on this link to start the game!\n{invite}')

@client.command(aliases=['draw', 'skribbl', 'skribble', 'skribbl.io'])
async def doodle(ctx):
    invite = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'sketch-heads')
    await ctx.send(f'click on this link to start the game!\n{invite}')

@client.command()
async def word(ctx):
    invite = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'awkword')
    await ctx.send(f'click on this link to start the game!\n{invite}')

@client.command()
async def fish(ctx):
    invite = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'fishing')
    await ctx.send(f'click on this link to start the game!\n{invite}')

@client.command()
async def bwstats(ctx, message=None):
    embed1 = discord.Embed(title='Hypixel Bedwars Statistics', url='https://bwstats.shivam.pro',description='click the link to view stats', colour=discord.Colour.dark_gold())
    embed2 = discord.Embed(title='Hypixel Bedwars Statistics', url=f'https://bwstats.shivam.pro/user/{message}',description=f'click the link to view the stats of {message}', colour=discord.Colour.dark_gold())

    if message == None:
        await ctx.send(embed=embed1)
    else:
        await ctx.send(embed=embed2)
@client.command()
async def hello(ctx):
    await ctx.send('Hello!')

@client.command()
async def spam(ctx):
    await ctx.send('no')
    await ctx.message.author.send("naughty naughty you shouldn't spam people or the server.")
    await ctx.message.author.send('this is what you get')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')
    await ctx.message.author.send('spam')



@client.command()
async def sudo(ctx, member: discord.Member, *, message=None):
    if message == None:
            await ctx.send(f'SyntaxError: a person and message must be specified')
            return

    webhook = await ctx.channel.create_webhook(name=member.name)
    await webhook.send(
            str(message), username=member.nick, avatar_url=member.avatar)

    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
            await webhook.delete()
    await ctx.message.delete()
@client.command()
async def help(ctx, message=None):
    embed = discord.Embed(title="Help", description="this page sucks lol if you really need help dm unseeyou",colour=discord.Colour.dark_gold())
    embed.add_field(name='COMMAND 1: help', value='this is the help command you just used.', inline=False)
    embed.add_field(name='COMMAND 2: join', value='this makes the bot join your current voice channel.', inline=False)
    embed.add_field(name='COMMAND 3: leave', value='this makes the bot leave your current voice channel.', inline=False)
    embed.add_field(name='COMMAND 4: play', value='this plays a single video, from a youtube URL.', inline=False)
    embed.add_field(name='COMMAND 5: pause', value='this pauses what the bot is currently playing.', inline=False)
    embed.add_field(name='COMMAND 6: resume', value='this resumes what you just paused.', inline=False)
    embed.add_field(name='COMMAND 7: hello', value='this lets you say hi to the bot.', inline=False)
    embed.add_field(name='COMMAND 8: invite', value='generates a link for you to invite unseebot to your server', inline=False)
    embed.add_field(name='COMMAND 9: stop', value='this stops the current audio being played.', inline=False)
    embed.set_footer(text='page 1 of 4')

    embed2 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou",colour=discord.Colour.dark_gold())
    embed2.add_field(name='COMMAND 10: yt', value='this creates a youtube together event in your current voice channel.')
    embed2.add_field(name='COMMAND 11: betrayal', value='this starts a betrayal.io activity in your voice channel.', inline=False)
    embed2.add_field(name='COMMAND 12: fish', value='this generates a fishington.io activity in your voice channel.', inline=False)
    embed2.add_field(name='COMMAND 13: doodle', value='this generates a doodle crew activity in your voice channel.',inline=False)
    embed2.add_field(name='COMMAND 14: word', value='this generates an awkword activity in your voice channel.',inline=False)
    embed2.add_field(name='COMMAND 15: bwstats', value='this gives a link to the bedwars stats website.', inline=False)
    embed2.add_field(name='COMMAND 16: sudo', value='impersonate your friends and foes. **CAUSE CHAOS**', inline=False)
    embed2.add_field(name='COMMAND 17: unseebot', value='essentially an about me sent in your dms', inline=False)
    embed2.set_footer(text='page 2 of 4')

    embed3 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou",colour=discord.Colour.dark_gold())
    embed3.add_field(name='COMMAND 18: github', value='gives a link to the unseebot github page', inline=False)
    embed3.add_field(name='COMMAND 19: 8ball', value='ask unseebot as yes or no question', inline=False)
    embed3.add_field(name='COMMAND 20: nick', value='changes the nickname of the selected user', inline=False)
    embed3.add_field(name='COMMAND 21: cat', value='shows a picture of cure kitty and tells you about pussies', inline=False)
    embed3.add_field(name='COMMAND 22: dog', value='shows a doggo and gives doggo facts', inline=False)
    embed3.add_field(name='COMMAND 23: playing', value='generates an embed showing audio that is currently being played', inline=False)
    embed3.add_field(name='COMMAND 24: queue', value='lists the current song queue', inline=False)
    embed3.add_field(name='COMMAND 25: loop', value='loops the current song', inline=False)
    embed3.set_footer(text='page 3 of 4')

    embed4 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou",colour=discord.Colour.dark_gold())
    embed4.add_field(name='COMMAND 26: skip', value='skips current song in the queue', inline=False)
    embed4.add_field(name='COMMAND 27: meme', value='gets a meme from reddit', inline=False)
    embed4.set_footer(text='page 4 of 4')

    if message == None:
        button = Button(label='Page 2', style=discord.ButtonStyle.blurple)
        button2 = Button(label='Page 1', style=discord.ButtonStyle.blurple)
        button3 = Button(label='Page 3', style=discord.ButtonStyle.blurple)
        button4 = Button(label='Page 4', style=discord.ButtonStyle.blurple)
        async def button_callback(interaction):
            await interaction.response.edit_message(embed=embed2)
        async def buttoncallback(interaction):
            await interaction.response.edit_message(embed=embed)
        async def butcal(interaction):
            await interaction.response.edit_message(embed=embed3)
        async def callback3(interaction):
            await interaction.response.edit_message(embed=embed4)
        button.callback=button_callback
        button2.callback=buttoncallback
        button3.callback=butcal
        button4.callback=callback3
        view = View()
        view.add_item(button2)
        view.add_item(button)
        view.add_item(button3)
        view.add_item(button4)
        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send('this page does not exist. please run >help')

@client.command(aliases=['8ball'])
async def _8ball(ctx, message=None):
    if message != None:
        list = ['my sources say yes', 'hell no', 'ask again later', "idk man you're on your own", 'sure, why not?', 'how about... no?']
        await ctx.send(random.choice(list))
    else:
        await ctx.send('ask me a question')


@client.command()
async def nick(ctx, member: discord.Member, nick):
    await ctx.send('reminder: I can only change nicknames of people when I have the perms and also my role is higher than theirs in the settings.')
    if nick:
        await member.edit(nick=nick)
        await ctx.send(f'nickname changed!')
    else:
        await ctx.send('Invalid nickname')

@client.command()
async def invite(ctx):
    embed = discord.Embed(title='click here', description='to invite unseebot to your server', url='https://discord.com/api/oauth2/authorize?client_id=915182238239449099&permissions=8&scope=bot%20applications.commands')
    await ctx.send(embed=embed)

@client.command()
async def github(ctx):
    git = discord.Embed(title='link', url='https://github.com/unseeyou/unseebot', description="click on the link to open unseebot's github page", colour=discord.Colour.dark_gray())
    git.set_image(url='https://images-ext-2.discordapp.net/external/pe2rnxtS-petcef7jYVHtm1ncabRKulTvDV70G1F5O8/https/repository-images.githubusercontent.com/435063686/e6f3942e-98dd-407b-9fbc-4ba1dbe89849')
    await ctx.send(embed=git)

@client.command()
async def ping(ctx):
    await ctx.send('PONG! my latency is: `{0} seconds`'.format(round(client.latency, 3)))

client.run(TOKEN)
