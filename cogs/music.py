import asyncio
import time
import discord
import youtube_dl
from discord.ext import commands
from pytube import YouTube

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

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
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',  # no video
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=15):
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


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def generate_embed(url):
        try:
            video_object = YouTube(url=url)
            title = video_object.title
            author = video_object.author
            length = video_object.length

            embed = discord.Embed(title=f"Now Playing: `{title}`", url=video_object.watch_url,
                                  description=f"duration: {round(length / 60, 2)} min")
            embed.set_thumbnail(url=video_object.thumbnail_url)
            embed.set_author(name=author, url=video_object.channel_url)

            return embed

        except BaseException as err:
            err = str(err)
            print(err)
            return err

    @commands.hybrid_command(help='joins your vc')
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        """Joins a voice channel"""
        msg = await ctx.send('joining your vc')

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        if channel is not None:
            await channel.connect()
        elif channel is None:
            channel = ctx.message.author.voice.channel
            await channel.connect()

        time.sleep(3)
        await msg.delete()

    @commands.hybrid_command(help='loads the video first then plays it - less lag than play')
    async def loadplay(self, ctx, *, url: str):
        """Plays from an url (almost anything youtube_dl supports)"""
        msg = await ctx.send('loading audio from url...')

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(embed=self.generate_embed(url))
        await msg.delete()

    @commands.hybrid_command(help='plays the video as it loads - faster than loadplay')
    async def play(self, ctx, *, url: str):
        """Streams from an url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(embed=self.generate_embed(url))

    @commands.hybrid_command(help='leaves the vc and stops playing audio')
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        msg = await ctx.send('stopping audio and leaving voice channel')
        await ctx.voice_client.disconnect()
        time.sleep(3)
        await msg.delete()

    @play.before_invoke
    @loadplay.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("SkillIssue: You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


async def setup(bot):
    await bot.add_cog(Music(bot))
