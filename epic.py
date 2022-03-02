import discord
from discord.ext import commands
import random

class Epicness(commands.Cog):
    @commands.command(aliases=["howepic", "epicness"])
    async def epic(self, ctx, *, message=None):
        if message == None:
            await ctx.send('Who/What are you trying to measure?')
        else:
            number = random.randint(-1,100)
            if number >= 80:
                text = 'Damn... THATS **EPIC**'
                image = 'https://i.imgflip.com/66u3xe.jpg'
            elif 80 > number >= 50:
                text = 'That is pretty epic'
                image = 'https://i.imgflip.com/66u4db.jpg'
            else:
                text = 'Imagine not epic XD'
                image = 'https://i.imgflip.com/66u4m9.jpg'
            embed1 = discord.Embed(title=f'How epic?', colour=discord.Colour.dark_purple())
            embed1.add_field(name='Epicness Meter', value=f"{message} is {str(number)}% **EPIC**", inline=False)
            embed1.set_footer(text=text)
            embed1.set_image(url=image)
            await ctx.send(embed=embed1)

def setup(bot):
    bot.add_cog(Epicness(bot))