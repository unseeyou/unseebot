import random
import discord
from discord.ext import commands

class commands(commands.Cog):
    @commands.command()
    async def pp(self,ctx,*,msg):
        balls = '8'
        tip = 'D'
        mid = '='
        length = random.randint(0, 20)
        embed = discord.Embed(title="pp length :0", description=f'{msg} has this pp: {balls}{mid * length}{tip}', color=discord.Colour.yellow())
        embed.set_author(name='😳')
        embed.set_footer(text='😳')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(commands(bot))