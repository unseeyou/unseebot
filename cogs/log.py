from discord.ext import commands

class Cog(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('>'):
            print(f"{message.guild}/{message.channel}/{message.author.name}:{message.content}")
            if message.embeds:
                print(message.embeds[0].to_dict())

def setup(bot):
    bot.add_cog(Cog(bot))