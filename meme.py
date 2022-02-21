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

            #TODO: next meme interaction button here:
            next_meme = Button(label='Next Meme', style=discord.ButtonStyle.green)
            async def callback(interaction):
                async with aiohttp.ClientSession() as session2:
                    rng2 = random.randrange(0, 3)
                    if rng2 == 1:
                        request2 = await session2.get("https://meme-api.herokuapp.com/gimme/memes")
                    elif rng2 == 0:
                        request2 = await session2.get("https://meme-api.herokuapp.com/gimme/dankmemes")
                    elif rng2 == 2:
                        request2 = await session2.get("https://meme-api.herokuapp.com/gimme/me_irl")
                    json2 = await request2.json()
                    newembed = discord.Embed(title=json2['title'], colour=discord.Colour.brand_red(), url=json2['postLink'])
                    newembed.set_image(url=json2['url'])
                    newembed.set_footer(text='r/' + json2['subreddit'] + ' posted by u/' + json2['author'])
                await interaction.response.edit_message(embed=newembed, view=view)
            next_meme.callback = callback
            view = View()
            view.add_item(next_meme)
            #Do I really need an end interaction button?
            #TODO THE ANSWER IS YES I DO NEED AN END INTERACTION
            end_button = Button(label='End Interaction', style=discord.ButtonStyle.danger)
            async def end_callback(interaction):
                view2 = View()
                await interaction.response.edit_message(embed=discord.Embed(title='INTERACTION ENDED', colour=discord.Colour.brand_red()), view=view2)

            end_button.callback = end_callback
            view.add_item(end_button)
            await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Meme(bot))