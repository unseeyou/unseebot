import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import aiohttp


class Meme(commands.Cog):
    @commands.hybrid_command(aliases=['m'], help='yoink memes from reddit')
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            rng = random.randrange(0, 3)
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
            next_meme = Button(label='Next Meme', style=discord.ButtonStyle.green)

            async def callback(interaction):
                async with aiohttp.ClientSession() as session2:
                    global newembed
                    rng2 = random.randrange(0, 3)
                    if rng2 == 1:
                        request2 = await session2.get("https://meme-api.herokuapp.com/gimme/memes")
                    elif rng2 == 0:
                        request2 = await session2.get("https://meme-api.herokuapp.com/gimme/dankmemes")
                    elif rng2 == 2:
                        request2 = await session2.get("https://meme-api.herokuapp.com/gimme/me_irl")
                    json2 = await request2.json()
                    newembed = discord.Embed(title=json2['title'], colour=discord.Colour.brand_red(),
                                             url=json2['postLink'])
                    newembed.set_image(url=json2['url'])
                    newembed.set_footer(text='r/' + json2['subreddit'] + ' posted by u/' + json2['author'])
                next_meme = Button(label='Next Meme', style=discord.ButtonStyle.green)
                view = View()
                view.add_item(next_meme)
                next_meme.callback = callback
                end_button.callback = end_callback
                view.add_item(end_button)
                await interaction.response.edit_message(embed=newembed, view=view)

            next_meme.callback = callback
            view = View()
            view.add_item(next_meme)
            end_button = Button(label='End Interaction', style=discord.ButtonStyle.danger)

            async def end_callback(interaction):
                view2 = View()
                await interaction.response.edit_message(view=view2)

            end_button.callback = end_callback
            view.add_item(end_button)
            await session.close()
            await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(aliases=['r', 'redditsearch'], help='yoink images and gifs from any subreddit')
    async def reddit(self, ctx, subreddit: str):
        try:
            async with aiohttp.ClientSession() as session:
                request = await session.get(f"https://meme-api.herokuapp.com/gimme/{subreddit}")
                json = await request.json()
                embed = discord.Embed(title=json['title'], colour=discord.Colour.brand_red(), url=json['postLink'])
                embed.set_image(url=f"{json['url']}")
                embed.set_footer(text='r/' + json['subreddit'] + ' posted by u/' + json['author'])
                next_meme = Button(label='Next Post', style=discord.ButtonStyle.green)

                async def callback(interaction):
                    global newembed

                    async def make_request(subreddit):
                        async with aiohttp.ClientSession() as session2:
                            request2 = await session2.get(f"https://meme-api.herokuapp.com/gimme/{subreddit}")
                            json2 = await request2.json()
                            return json2

                    try:
                        json2 = await make_request(subreddit)

                    except Exception as err:
                        print(err)
                        error = True
                        while error:
                            try:
                                json2 = await make_request(subreddit)
                            except Exception as error:
                                continue

                    try:
                        newembed = discord.Embed(title=json2['title'], colour=discord.Colour.brand_red(),
                                                 url=json2['postLink'])
                        newembed.set_image(url=json2['url'])
                        newembed.set_footer(text='r/' + json2['subreddit'] + ' posted by u/' + json2['author'])
                        next_meme = Button(label='Next Post', style=discord.ButtonStyle.green)
                        view2 = View()
                        view2.add_item(next_meme)
                        next_meme.callback = callback
                        end_button.callback = end_callback
                        view2.add_item(end_button)
                        await interaction.response.edit_message(embed=newembed, view=view2)
                    except Exception:
                        pass

                next_meme.callback = callback
                view = View()
                view.add_item(next_meme)
                end_button = Button(label='End Interaction', style=discord.ButtonStyle.danger)

                async def end_callback(interaction):
                    view2 = View()
                    await interaction.response.edit_message(view=view2)

                end_button.callback = end_callback
                view.add_item(end_button)
                await session.close()
                await ctx.send(embed=embed, view=view)
        except Exception as err:
            await ctx.send("`Error making request: subreddit has insufficient data`")


async def setup(bot):
    await bot.add_cog(Meme(bot))
