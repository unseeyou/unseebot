__author__ = 'unseeyou'

import random
import os
import io
import discord
import aiohttp
import asyncio
import time
from dotenv import load_dotenv
from discord.ext import commands
from discord_together import DiscordTogether

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='>', help_command=None, case_insensitive=True, intents=intents)

load_dotenv()
TOKEN = os.getenv("UNSEEBOT_TOKEN")


async def activity_warn(ctx):
    await ctx.send("this is either because the server does not have activities enabled or you don't have nitro.")


@bot.event
async def on_ready():
    bot.togetherControl = DiscordTogether(TOKEN)
    print('loading slash commands...')
    try:
        await bot.tree.sync(guild=None)
    except Exception as e:
        print(e)
    await bot.change_presence(activity=discord.Game('With your mind - >help'), status=discord.Status.online)
    print("If you are seeing this then unseeyou's epic bot is working!")
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, this command does not exist. Contact unseeyou#2912 if you think this should be added.")
    elif isinstance(error, discord.errors.NotFound):
        pass


@bot.listen()
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="join-leave")
    if channel is not None:
        embed = discord.Embed(color=0x4a3d9a)
        embed.add_field(name="Welcome", value=f"{member.mention} has joined {member.guild.name}", inline=False)
        await channel.send(embed=embed)
    else:
        pass


@bot.listen()
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name="join-leave")
    if channel is not None:
        embed = discord.Embed(color=0x4a3d9a)
        embed.add_field(name="Goodbye", value=f"{member.mention} has left {member.guild.name}", inline=False)
        await channel.send(embed=embed)
    else:
        pass


@bot.hybrid_command(aliases=['trigger', 'trig'], help='generate a gif of a triggered user')
async def triggered(ctx, user: discord.User = None):
    if user is None:
        user = ctx.message.author
    else:
        pass
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://some-random-api.ml/canvas/triggered?avatar={user.avatar.url}') as response:
            buffer = io.BytesIO(await response.read())

    await ctx.send(file=discord.File(buffer, filename='triggered.gif'))


@bot.command(pass_context=True)
async def unseebot(ctx):
    await ctx.send('Check your dms!')
    await ctx.message.author.send(
        "Hi! I'm unseebot, a bot made by unseeyou. Please feel free to report any issues to unseeyou via dms. Thanks!")


@bot.hybrid_command(help='launches the youtube watch together discord activity if you are in a vc')
async def yt(ctx):
    try:
        link = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        await ctx.send(f"Click on the blue link to start the event!\n{link}")
    except Exception as err:
        print(err)
        await ctx.send(err)
        await activity_warn(ctx)


@bot.hybrid_command(aliases=['doggo', 'dogs', 'dogfacts', 'dogfact', 'pup', 'pupper', 'puppy'], help='doggy pics!')
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


@bot.command()
async def anal(ctx):
    await ctx.send('https://tenor.com/view/sheep-anal-sheep-bum-bum-stab-from-behind-gif-19411863')


@bot.hybrid_command(aliases=['kitty', 'kitten', 'meow', 'catfact', 'catfacts'], help='kitty pics!')
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


@bot.hybrid_command(help='launches the poker activity')
async def poker(ctx):
    try:
        invite = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'poker')
        await ctx.send(f'click on this link to start the game!\n{invite}')
    except Exception as err:
        print(err)
        await ctx.send(err)
        await activity_warn(ctx)


@bot.hybrid_command(aliases=['draw', 'skribbl', 'scribble', 'skribbl.io'], help='skribbl.io but in a discord vc')
async def doodle(ctx):
    try:
        invite = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'sketch-heads')
        await ctx.send(f'click on this link to start the game!\n{invite}')
    except Exception as err:
        print(err)
        await ctx.send(err)
        await activity_warn(ctx)


@bot.hybrid_command(help='discord vc game which involves words I guess')
async def word(ctx):
    try:
        invite = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'awkword')
        await ctx.send(f'click on this link to start the game!\n{invite}')
    except Exception as err:
        print(err)
        await ctx.send(err)
        await activity_warn(ctx)


@bot.hybrid_command(help='golf but in a discord voice chat')
async def golf(ctx):
    try:
        invite = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'putt-party')
        await ctx.send(f'click on this link to start the game!\n{invite}')
    except Exception as err:
        print(err)
        await ctx.send(err)
        await activity_warn(ctx)


@bot.command()
async def bwstats(ctx, message=None):
    embed1 = discord.Embed(title='Hypixel Bedwars Statistics', url='https://bwstats.shivam.pro',
                           description='click the link to view stats', colour=discord.Colour.dark_gold())
    embed2 = discord.Embed(title='Hypixel Bedwars Statistics', url=f'https://bwstats.shivam.pro/user/{message}',
                           description=f'click the link to view the stats of {message}',
                           colour=discord.Colour.dark_gold())

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
    for i in range(12):
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


@bot.hybrid_command(help='repeats your message')
async def echo(ctx, *, message: str):
    try:
        await ctx.message.delete()
    except Exception:
        pass
    await ctx.send(message)


@bot.hybrid_command(name='8ball', help='classic 8ball. or is it?')
async def _8ball(ctx, message: str):
    if message is not None or False:
        ans = ['my sources say yes', 'hell no', 'ask again later', "idk man you're on your own", 'sure, why not?',
               'how about... no?']
        await ctx.reply(random.choice(ans))
    else:
        await ctx.reply('ask me a question')  # TODO: fix issue where this message isn't sending


@bot.hybrid_command(help='generates an invite link for unseebot. please use this and not my profile.')
async def invite(ctx):
    embed = discord.Embed(title='click here', description='to invite unseebot to your server',
                          url='https://discord.com/api/oauth2/authorize?client_id=915182238239449099&permissions=8&scope=bot%20applications.commands')
    await ctx.send(embed=embed)


@bot.hybrid_command(help='my github!')
async def github(ctx):
    git = discord.Embed(title='link', url='https://github.com/unseeyou/unseebot',
                        description="click on the link to open unseebot'b github page",
                        colour=discord.Colour.dark_gray())
    git.set_image(
        url='https://images-ext-2.discordapp.net/external/pe2rnxtS-petcef7jYVHtm1ncabRKulTvDV70G1F5O8/https/repository-images.githubusercontent.com/435063686/e6f3942e-98dd-407b-9fbc-4ba1dbe89849')
    await ctx.send(embed=git)


@bot.hybrid_command(help='probably my ping')
async def ping(ctx: commands.Context):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong! My ping is `{int(ping)}ms`")
    print(f'Ping: `{int(ping)} ms`')


async def main():
    async with bot:
        await bot.load_extension("cogs.meme")
        await bot.load_extension("cogs.tictactoe")
        await bot.load_extension("cogs.hystats")
        await bot.load_extension("cogs.help")
        await bot.load_extension("cogs.epic")
        await bot.load_extension("cogs.pplength")
        await bot.load_extension("cogs.urban")
        await bot.load_extension("cogs.fakehack")
        await bot.load_extension("cogs.tts")
        await bot.load_extension("cogs.xkcd")
        await bot.load_extension("cogs.poll")
        await bot.load_extension("cogs.music")
        await bot.load_extension("cogs.twitch")

        await bot.load_extension("utils.log")
        await bot.start(TOKEN)


asyncio.run(main())
