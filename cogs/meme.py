import discord
from discord.ext import commands
from discord.ui import Button, View
import os
import praw
from dotenv import load_dotenv

load_dotenv()
praw_id = os.getenv('UNSEEBOT_PRAW_ID')
praw_secret = os.getenv('UNSEEBOT_PRAW_SECRET')
praw_user_agent = "unseebot by u/donotmindmenoobalert"
reddit = praw.Reddit(client_id=praw_id, client_secret=praw_secret, user_agent=praw_user_agent, check_for_async=False)


def get_post(subreddit: str):
    try:
        sub = reddit.subreddit(subreddit.lower()).random()
        result = {'title': sub.title,
                  'postLink': "https://www.reddit.com" + sub.permalink,
                  "url": sub.url,
                  "subreddit": ''.join(sub.permalink.replace('https://www.reddit.com/','').split(r'/')[2:3]),
                  "author": sub.author.name,
                  "upvotes": sub.score,
                  "author_url": "https://reddit.com/u/"+sub.author.name}
        return result
    except Exception as err:
        print(err)


class Meme(commands.Cog):
    @commands.hybrid_command(aliases=['m'], help='yoink memes from reddit')
    async def meme(self, ctx):
        await ctx.typing()
        json = get_post('memes+dankmemes+meme')
        embed = discord.Embed(title=json['title'], colour=discord.Colour.brand_red(), url=json['postLink'])
        embed.set_image(url=json['url'])
        embed.set_footer(text='r/' + json['subreddit'] + f", {json['upvotes']} upvotes")
        embed.set_author(name='posted by u/' + json['author'], url=json["author_url"])
        next_meme = Button(label='Next Meme', style=discord.ButtonStyle.green)

        async def callback(interaction):
            json2 = get_post('memes+dankmemes+meme')
            newembed = discord.Embed(title=json2['title'], colour=discord.Colour.brand_red(),
                                     url=json2['postLink'])
            newembed.set_image(url=json2['url'])
            newembed.set_footer(text='r/' + json2['subreddit'] + f", {json2['upvotes']} upvotes")
            newembed.set_author(name='posted by u/' + json2['author'], url=json2["author_url"])
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
            for child in view.children:
                child.disabled = True
            await interaction.response.edit_message(view=view)

        end_button.callback = end_callback
        view.add_item(end_button)
        await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(aliases=['r', 'redditsearch'], help='yoink images and gifs from any subreddit')
    async def reddit(self, ctx, subreddit: str):
        await ctx.typing()
        try:
                request = get_post(subreddit.lower())
                embed = discord.Embed(title=request["title"], colour=discord.Colour.brand_red(), url=request['postLink'])
                embed.set_image(url=f"{request['url']}")
                embed.set_footer(text='r/' + request['subreddit'] + f", {request['upvotes']} upvotes")
                embed.set_author(name='posted by u/' + request['author'], url=request["author_url"])
                next_meme = Button(label='Next Post', style=discord.ButtonStyle.green)

                async def callback(interaction):
                    json2 = get_post(subreddit)
                    try:
                        newembed = discord.Embed(title=json2['title'], colour=discord.Colour.brand_red(),
                                                 url=json2['postLink'])
                        newembed.set_image(url=json2['url'])
                        newembed.set_footer(text='r/' + json2['subreddit'] + f", {json2['upvotes']} upvotes")
                        newembed.set_author(name='posted by u/' + json2['author'], url=json2["author_url"])
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
                    for child in view.children:
                        child.disabled = True
                    await interaction.response.edit_message(view=view)

                end_button.callback = end_callback
                view.add_item(end_button)
                await ctx.send(embed=embed, view=view)
        except Exception as err:
            await ctx.send(f"`Error making request: subreddit has insufficient data`: ```[{err}]```")


async def setup(bot):
    await bot.add_cog(Meme(bot))
