import discord
from discord.ext import commands
import random


class Epicness(commands.Cog):
    @commands.hybrid_command(aliases=["howepic", "epicness"], help='how epic are you?')
    async def epic(self, ctx, *, message: str = None):
        if message is None:
            await ctx.send('Who/What are you trying to measure?')
        else:
            number = random.randint(-1, 100)
            if number >= 75:
                text = 'Damn... THATS EPIC'
                image = 'https://i.imgflip.com/66u3xe.jpg'
            elif 75 > number >= 50:
                text = 'That is pretty epic'
                image = 'https://i.imgflip.com/674omn.jpg'
            else:
                text = 'Imagine not epic XD'
                image = 'https://i.imgflip.com/66u4m9.jpg'
            embed1 = discord.Embed(title=f'How epic?', colour=discord.Colour.dark_purple())
            embed1.add_field(name='Epicness Meter', value=f"{message} is {str(number)}% **EPIC**", inline=False)
            embed1.set_footer(text=text)
            embed1.set_image(url=image)
            await ctx.send(embed=embed1)


async def setup(bot):
    await bot.add_cog(Epicness(bot))
