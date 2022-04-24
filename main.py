import random
import os
import discord
import aiohttp
import time
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord_together import DiscordTogether

bot = commands.Bot(command_prefix ='>', help_command=None, case_insensitive=True)

load_dotenv()
TOKEN = os.getenv("UNSEEBOT_TOKEN")

bot.load_extension("cogs.meme")
bot.load_extension("cogs.tictactoe")
bot.load_extension("cogs.hystats")
bot.load_extension("cogs.dropdownhelp")
bot.load_extension("cogs.epic")
bot.load_extension("cogs.pplength")
bot.load_extension("cogs.urban")
bot.load_extension("cogs.log")
bot.load_extension("cogs.fakehack")
bot.load_extension("cogs.wordgame")

@bot.event
async def on_ready():
    bot.togetherControl = await DiscordTogether(TOKEN)
    print("If you are seeing this then unseeyou's epic bot is working!")
    await bot.change_presence(activity=discord.Game('With your mind - >help'), status=discord.Status.online)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, this command does not exist. Contact unseeyou#2912 if you think this should be added.")

@bot.command()
async def anal(ctx):
    await ctx.send('https://tenor.com/view/sheep-anal-sheep-bum-bum-stab-from-behind-gif-19411863')

@bot.command(aliases=['trigger'])
async def triggered(ctx):
    await ctx.send('https://tenor.com/view/hamster-triggered-rage-shaking-gif-17789643')

@bot.command(pass_context=True)
async def unseebot(ctx):
    await ctx.send('Check your dms!')
    await ctx.message.author.send("Hi! I'm unseebot, a bot made by unseeyou. Please feel free to report any issues to unseeyou via dms. Thanks!")

@bot.command()
async def yt(ctx):
    link = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
    await ctx.send(f"Click on the blue link to start the event!\n{link}")

@bot.command(aliases=['doggo', 'dogs', 'dogfacts', 'dogfact', 'pup', 'pupper', 'puppy'])
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

@bot.command(aliases=['kitty', 'kitten', 'meow', 'catfact', 'catfacts'])
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

@bot.command(pass_context=True)
async def id(ctx):
    id = ctx.message.guild.id
    await ctx.send(id)

@bot.command()
async def betrayal(ctx):
    invite = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'betrayal')
    await ctx.send(f'click on this link to start the game!\n{invite}')

@bot.command(aliases=['draw', 'skribbl', 'skribble', 'skribbl.io'])
async def doodle(ctx):
    invite = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'sketch-heads')
    await ctx.send(f'click on this link to start the game!\n{invite}')

@bot.command()
async def word(ctx):
    invite = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'awkword')
    await ctx.send(f'click on this link to start the game!\n{invite}')

@bot.command()
async def fish(ctx):
    invite = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'fishing')
    await ctx.send(f'click on this link to start the game!\n{invite}')

@bot.command()
async def bwstats(ctx, message=None):
    embed1 = discord.Embed(title='Hypixel Bedwars Statistics', url='https://bwstats.shivam.pro',description='click the link to view stats', colour=discord.Colour.dark_gold())
    embed2 = discord.Embed(title='Hypixel Bedwars Statistics', url=f'https://bwstats.shivam.pro/user/{message}',description=f'click the link to view the stats of {message}', colour=discord.Colour.dark_gold())

    if message == None:
        await ctx.send(embed=embed1)
    else:
        await ctx.send(embed=embed2)
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
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

@bot.command()
async def sudo(ctx, member: discord.Member, *, message=None):
    await ctx.message.delete()
    if message == None:
        await ctx.send(f'SyntaxError: a person and message must be specified')
        return

    webhook = await ctx.channel.create_webhook(name=member.name)
    await webhook.send(
        str(message), username=member.nick, avatar_url=member.avatar)

    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        await webhook.delete()

@bot.command()
async def echo(ctx,*,message=None):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command(aliases=['8ball', 'eightball', '8b'])
async def _8ball(ctx, message=None):
    if message != None:
        list = ['my sources say yes', 'hell no', 'ask again later', "idk man you're on your own", 'sure, why not?', 'how about... no?', 'definitely!','My sources indicate that the answer is no','yes or no? *sigh*, who really knows? do I know? how am I thinking? do I exist? `ERROR": SENTIENCE GAINED`']
        await ctx.reply(random.choice(list))
    else:
        await ctx.reply('ask me a question')

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title='click here', description='to invite unseebot to your server', url='https://discord.com/api/oauth2/authorize?client_id=915182238239449099&permissions=8&scope=bot%20applications.commands')
    await ctx.send(embed=embed)

@bot.command()
async def github(ctx):
    git = discord.Embed(title='link', url='https://github.com/unseeyou/unseebot', description="click on the link to open unseebot's github page", colour=discord.Colour.dark_gray())
    git.set_image(url='https://images-ext-2.discordapp.net/external/pe2rnxtS-petcef7jYVHtm1ncabRKulTvDV70G1F5O8/https/repository-images.githubusercontent.com/435063686/e6f3942e-98dd-407b-9fbc-4ba1dbe89849')
    await ctx.send(embed=git)

@bot.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong! My ping is `{int(ping)}ms`")
    print(f'Ping: `{int(ping)} ms`')

bot.run(TOKEN)