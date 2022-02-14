import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import aiohttp

class Meme(commands.Cog):
    @commands.command(aliases=['m'])
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            rng = random.randrange(0,3)
            if rng == 1:
                request = await session.get("https://meme-api.herokuapp.com/gimme/memes")
            elif rng == 0:
                request = await session.get("https://meme-api.herokuapp.com/gimme/dankmemes")
            elif rng == 2:
                request = await session.get("https://meme-api.herokuapp.com/gimme/me_irl")
            json = await request.json()

            embed = discord.Embed(title=json['title'], colour=discord.Colour.brand_red(), url=json['postLink'])
            embed.set_image(url=json['url'])
            embed.set_footer(text='r/' + json['subreddit'] + ' posted by u/' + json['author'])

            #TODO: next meme interaction here
            #lol theres nothing here for now
            #TODO: end interaction button code right here:

            interact_ended = discord.Embed(title='INTERACTION ENDED', colour=discord.Colour.brand_red())

            stop_button = Button(label='end interaction', style=discord.ButtonStyle.danger)
            async def stop_button_callback(interaction):
                await interaction.response.edit_message(embed=interact_ended)
            stop_button.callback = stop_button_callback
            view = View()
            view.add_item(stop_button)

            await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Meme(bot))