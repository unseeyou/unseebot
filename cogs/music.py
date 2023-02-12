import asyncio
import time
import discord
import youtube_dl
import os
from time import strftime, gmtime, sleep
from moviepy.audio.io.AudioFileClip import AudioFileClip
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
        self.volume = volume

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
                                  description=f"duration: {strftime('%H:%M:%S', gmtime(length))}")
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
        await ctx.typing(ephemeral=True)
        msg = await ctx.send('**LOG:**')
        video_object = YouTube(url)
        log = """```
        created video object```"""
        print(log)
        log_msg = await ctx.send(log)
        downloaded_file = video_object.streams.get_audio_only().download()
        log = """```
        created video object
        downloaded mp4 file```"""
        print(log)
        await log_msg.edit(content=log)
        clip = AudioFileClip(downloaded_file)
        log = """```
        created video object
        downloaded mp4 file
        created moviepy clip```"""
        print(log)
        await log_msg.edit(content=log)
        clip.write_audiofile(downloaded_file.replace(".mp4", ".mp3"))
        log = """```
        created video object
        downloaded mp4 file
        created moviepy clip
        succesfully encoded mp3 file with audio data```"""
        print(log)
        await log_msg.edit(content=log)
        clip.close()
        log = """```
        created video object
        downloaded mp4 file
        created moviepy clip
        succesfully encoded mp3 file with audio data
        saved audio file```"""
        print(log)
        await log_msg.edit(log)
        os.remove(downloaded_file)
        log = """```
        created video object
        downloaded mp4 file
        created moviepy clip
        succesfully encoded mp3 file with audio data
        saved audio file
        deleted video file```"""
        print(log)
        await log_msg.edit(log)
        music_file = clip.filename.replace(".mp4", ".mp3")
        audio_source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(source=clip.filename, options="-loglevel panic"), volume=15)
        log = """```
        created video object
        downloaded mp4 file
        created moviepy clip
        succesfully encoded mp3 file with audio data
        saved audio file
        deleted video file
        created audio source```"""
        print(log)
        await log_msg.edit(log)
        await ctx.send(embed=self.generate_embed(url))
        await log_msg.delete()
        await msg.delete()
        ctx.voice_client.play(audio_source, after=lambda e: print(f'Player error: {e}') if e else None)  # TODO: fix this
        while ctx.voice_client.is_playing():
            print('i am playing audio')
        print('played audio')
        os.remove(music_file)
        print('removed mp3 file')

    @commands.hybrid_command(help='plays the video as it loads - faster than loadplay')
    async def play(self, ctx, *, url: str):
        """Streams from an url (same as yt, but doesn't predownload)"""

        if ctx.voice_client is None:
            channel = ctx.message.author.voice_channel
            await channel.connect()

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
