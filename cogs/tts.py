import discord
import uuid
import os
from time import sleep
from gtts import gTTS
from discord.ext import commands


class TTSCommands(commands.Cog):
    @commands.hybrid_command(help='sends a tts message into your current vc')
    async def tts(self, ctx, *, msg: str = None):
        if msg is not None:
            m = await ctx.send('sending your msg!')
            sleep(0.2)
            await m.delete()
            name = uuid.uuid4()
            try:
                await ctx.message.author.voice.channel.connect()
                try:
                    language = 'en'
                    speech = gTTS(text=f'{ctx.author.name} says '+msg, lang=language, slow=False)
                    speech.save(f"cogs/tts-files/{name}.mp3")
                    try:
                        audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=f'cogs/tts-files/{name}.mp3',options = "-loglevel panic"), volume=90)
                        ctx.voice_client.play(audio_source)
                        while ctx.voice_client.is_playing():
                            if not ctx.voice_client.is_playing():
                                break
                            else:
                                pass
                        os.remove(f"cogs/tts-files/{name}.mp3")
                        await ctx.voice_client.disconnect()

                    except BaseException as err:
                        print(err)
                except BaseException as e:
                    await ctx.send(f'Error: {e}')
                    print(e)
            except BaseException as err:
                print(err)
                await ctx.send(f'Error: you are not in a voice channel ({err})')

        else:
            await ctx.send('Error: no message provided')


async def setup(bot):
    await bot.add_cog(TTSCommands(bot))
