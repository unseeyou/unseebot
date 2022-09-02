import os
import discord
from aiohttp import ClientSession
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
rapidapi = os.getenv("RAPIDAPI")


class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        aliases=["urban", "urband", "urb"], help='gets the first definition from urban dictionary')
    async def urbandictionary(self, ctx, *, term: str):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term": term}
        headers = {
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
            'x-rapidapi-key': rapidapi
        }
        async with ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as response:
                r = await response.json()
                result = r['list'][0]
                desc = result['definition'].replace('[', '')
                desc = desc.replace(']', '')
                res = result["example"].replace('[', '')
                res = res.replace(']', '')
                embed = discord.Embed(title=f"First result for: {term}", description=desc,
                                      colour=discord.Colour.green(), url=result["permalink"])
                embed.add_field(name='Example', value=res)
                embed.set_footer(text=f'Likes: {str(result["thumbs_up"])}  Dislikes: {str(result["thumbs_down"])}')
                embed.set_author(name=f'Posted by {result["author"]}')
            await session.close()
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Dictionary(bot))
