from discord.ext import commands


def clean(text):
    return ''.join(ch for ch in text if ch.isalnum())


class Cog(commands.Cog):



    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('>'):  # TODO: log into log.txt
            logline = f"{clean(message.guild)}/{clean(message.channel)}/{clean(message.author.name)}:{clean(message.content)}/{clean(message.content)}"
            print(logline)
            if message.embeds:
                line2 = message.embeds[0].to_dict()
                logfile.write(line2)

            logfile.close()


async def setup(bot):
    await bot.add_cog(Cog(bot))
