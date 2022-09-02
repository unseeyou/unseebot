import random
import discord
from discord.ext import commands

class commandsE(commands.Cog):
    @commands.hybrid_command(help='how long is pp?')
    async def pp(self, ctx, *, msg: str):
        balls = '8'
        tip = 'D'
        mid = '='
        length = random.randint(0, 20)
        embed = discord.Embed(title="pp length :0", description=f'{msg} has this pp: {balls}{mid * length}{tip}', color=discord.Colour.yellow())
        embed.set_author(name='😳')
        embed.set_footer(text='😳')
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(commandsE(bot))
