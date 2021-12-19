import asyncio
import discord
import requests
import youtube_dl
from dcactivity import DCActivity
from discord.ext import commands
from discord_together import DiscordTogether

client = commands.Bot(command_prefix = '>', help_command=None)

youtube_dl.utils.bug_reports_message = lambda: ''
dcactivity = DCActivity(client)
players = {}
_ = False

TOKEN = 'OTE1MTgyMjM4MjM5NDQ5MDk5.YaX34A.BrO_s8lIjXwJCOkU1cTk-QbakRs'

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@client.event
async def on_ready():
    client.togetherControl = await DiscordTogether('OTE1MTgyMjM4MjM5NDQ5MDk5.YaX34A.BrO_s8lIjXwJCOkU1cTk-QbakRs')
    print("If you are seeing this then unseeyou's epic bot is working!")
    await client.change_presence(activity=discord.Game('With your mind - >help'))

@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        await client.send_message(ctx.message.channel, "Sorry, this command does not exist. Contact unseeyou#2912 if you think this should be added.")

@client.command()
async def yt(ctx):
    link = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
    await ctx.send(f"Click on the blue link to start the event!\n{link}")

@client.command()
async def betrayal(ctx):
    invite = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'betrayal')
    await ctx.send(f'click on this link to start the game!\n{invite}')

@client.command()
async def doodle(ctx):
    invite = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'doodle-crew')
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
async def help(ctx):
    embed = discord.Embed(title="Help", description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
    embed.add_field(name='COMMAND 1: help', value='this is the help command you just used.', inline=False)
    embed.add_field(name='COMMAND 2: join', value='this makes the bot join your current voice channel.', inline=False)
    embed.add_field(name='COMMAND 3: leave', value='this makes the bot leave your current voice channel.', inline=False)
    embed.add_field(name='COMMAND 4: play', value='this plays a single video, from a youtube URL. - **NOT WORKING**', inline=False)
    embed.add_field(name='COMMAND 5: pause', value='this pauses what the bot is currently playing. - **NOT WORKING**', inline=False)
    embed.add_field(name='COMMAND 6: resume', value='this resumes what you just paused. - **NOT WORKING**', inline=False)
    embed.add_field(name='COMMAND 7: hello', value='this lets you say hi to the bot.', inline=False)
    embed.add_field(name='COMMAND 8: spam', value='I think this is pretty self explanatory. A word of warning: it uses @everyone.- **OFFICIALLY REMOVED**', inline=False)
    embed.add_field(name='COMMAND 9: stop', value='this stops the current audio being played by the bot.', inline=False)
    embed.add_field(name='COMMAND 10: yt', value='this creates a youtube together event in your current voice channel.')
    embed.add_field(name='COMMAND 11: betrayal', value='this starts a betrayal.io activity in your voice channel.', inline=False)
    embed.add_field(name='COMMAND 12: fish', value='this generates a fishington.io activity in your voice channel', inline=False)
    embed.add_field(name='COMMAND 12: doodle', value='this generates a doodle crew activity in your voice channel',inline=False)
    embed.add_field(name='COMMAND 12: word', value='this generates an awkword activity in your voice channel',inline=False)
    embed.add_field(name='COMMAND 13: bwstats', value='this gives a link to the bedwars stats website', inline=False)

    await ctx.send(embed=embed)

@client.command()
async def bwstats(ctx):
    embed = discord.Embed(title='Hypixel Bedwars Statistics', url='https://bwstats.shivam.pro',description='click the link to view stats', colour=discord.Colour.dark_gold())

    await ctx.send(embed=embed)

@client.command()
async def hello(ctx):
    await ctx.send('Hello!')

#@client.command()
#async def spam(ctx):
   # await ctx.send('@everyone hi')
   # await ctx.send('@everyone hi')
    #await ctx.send('@everyone hi')
   # await ctx.send('@everyone hi')
   # await ctx.send('@everyone hi')
  #  await ctx.send('@everyone hi')
  #  await ctx.send('@everyone hi')
   # await ctx.send('@everyone hi')
  #  await ctx.send('@everyone hi')
    #await ctx.send('@everyone hi')
    #await ctx.send('@everyone hi')
  #  await ctx.send('@everyone hi')

@client.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        _ = True
    await channel.connect()


@client.command()
async def leave(ctx):
    _ = False
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def play(ctx,url):
    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        filename = await YTDLSource.from_url(url)
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
    await ctx.send('**Now playing:** {}'.format(filename))

@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@client.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@client.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

client.run('OTE1MTgyMjM4MjM5NDQ5MDk5.YaX34A.BrO_s8lIjXwJCOkU1cTk-QbakRs')
