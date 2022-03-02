import os
import discord
from aiohttp import ClientSession
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
rapidapi = os.getenv("RAPIDAPI")

class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(
        name="Urban dictionary", aliases=["urban", "urband", "urb"])
    async def urbandictionary(self, ctx, *, term):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term":term}
        headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': rapidapi
        }
        async with ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as response:
                r = await response.json()
                result = r['list'][0]
                desc = result['definition'].replace('[','')
                desc = desc.replace(']','')
                res = result["example"].replace('[','')
                res = res.replace(']','')
                embed = discord.Embed(title=f"First result for: {term}", description=desc, colour=discord.Colour.green(), url= result["permalink"])
                embed.add_field(name='Example', value=res)
                embed.set_footer(text=f'👍 {str(result["thumbs_up"])}       👎 {str(result["thumbs_down"])}')
                embed.set_author(name=f'Posted by {result["author"]}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Dictionary(bot))