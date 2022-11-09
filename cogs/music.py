import discord
import uuid
import os
from time import sleep
from pathlib import Path
from pytube import YouTube
from discord.ext import commands


def download_file(url):
    video_object = YouTube(url=url)
    downloaded_file = video_object.streams.get_audio_only().download()
    name = uuid.uuid4()
    new_file = str(name) + '.mp3'
    os.rename(downloaded_file, new_file)
    Path(new_file).rename('cogs/music-storage/'+new_file)
    return 'cogs/music-storage/'+new_file


def delete_file(path):
    os.remove(path)


def generate_embed(url):
    try:
        video_object = YouTube(url=url)
        title = video_object.title
        author = video_object.author
        length = video_object.length

        embed = discord.Embed(title=f"Now Playing: `{title}`", url=video_object.watch_url, description=f"duration: {round(length / 60, 2)} min")
        embed.set_thumbnail(url=video_object.thumbnail_url)
        embed.set_author(name=author, url=video_object.channel_url)

        return embed

    except BaseException as err:
        print(err)
        return err


class MusicStuff(commands.Cog):
    @commands.hybrid_command(name='play', help='plays music from a yt link, fuck you yt TOS')
    async def play(self, ctx, url: str):
        await ctx.send(embed=generate_embed(url))
        try:
            await ctx.message.author.voice.channel.connect()
            file = download_file(url)
            try:
                audio_source = discord.PCMVolumeTransformer(
                    discord.FFmpegPCMAudio(source=file, options="-loglevel panic"), volume=60)
                ctx.voice_client.play(audio_source)
                while ctx.voice_client.is_playing():
                    if not ctx.voice_client.is_playing():
                        print('something wrong')
                        break
                    else:
                        pass
                delete_file(file)  # deletes the file after playing

            except Exception as err:
                print(err)
                await ctx.send(str(type(err)) + ':', err)
        except Exception as err:
            print(err)
            await ctx.send(str(type(err)) + ':', err)

    @commands.hybrid_command(name='leave', help='leaves the vc')
    async def leave(self, ctx):
        await ctx.guild.voice_client.disconnect()
        m = await ctx.send('left your vc!')
        sleep(2)
        await m.delete()

    @commands.hybrid_command(name='join', help='joins the vc')
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()
        m = await ctx.send('joined your vc!')
        sleep(2)
        await m.delete()


async def setup(bot):
    await bot.add_cog(MusicStuff(bot))
