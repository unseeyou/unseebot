import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
import math

load_dotenv()
TOKEN = os.getenv("HYPIXEL_API")
BASE = 10_000
GROWTH = 2_500
REVERSE_PQ_PREFIX = -(BASE - 0.5 * GROWTH) / GROWTH
REVERSE_CONST = REVERSE_PQ_PREFIX
GROWTH_DIVIDES_2 = 2 / GROWTH

class stats(commands.Cog):
    @commands.command()
    async def hystats(self,ctx,msg=None):
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://api.hypixel.net/player?name={msg}&key={TOKEN}')
            json = await request.json()
            'print(json)'
        playerdata = json["player"]
        stats = playerdata["stats"]
        duels = stats["Duels"]
        bedwars = stats["Bedwars"]
        skywars = stats["SkyWars"]
        xp = int(playerdata["networkExp"])
        level = str(math.floor(1 + REVERSE_PQ_PREFIX + math.sqrt(REVERSE_CONST + GROWTH_DIVIDES_2 * xp)))
        uuid = playerdata["uuid"]
        'print(json["player"])'
        player = json["player"]
        if "rank" in player:
            rank = player["rank"]
        elif 'monthlyPackageRank' in player and player['monthlyPackageRank'] == "SUPERSTAR":
            rank = 'MVP++'
        elif "newPackageRank" in player and player["newPackageRank"] == 'VIP_PLUS' or 'MVP_PLUS':
            rank = player["newPackageRank"].replace('_PLUS', '+')
        else:
            rank = 'Normal'
        username = player["displayname"]
        embed = discord.Embed(title='HyStats', colour=discord.Colour.dark_gold())
        embed.add_field(name=f'{username}', value='Hypixel Achievement Points: ' + str(player["achievementPoints"]),inline=False)
        embed.add_field(name='Hypixel Rank', value=f"{username}'s Rank: {rank}")
        embed.add_field(name='Hypixel Level', value=f" Hypixel Level: {level}")
        embed.add_field(name='Duels Stats', value=f'Games Played: {duels["games_played_duels"]}, Games Won: {duels["wins"]}',inline=False)
        embed.add_field(name="Bedwars Stats", value=f'Games Played: {bedwars["games_played_bedwars"]}, Games Won: {bedwars["wins_bedwars"]}',inline=False)
        embed.add_field(name="Skywars Stats", value=f'Games Played: {skywars["games_played_skywars"]}, Games Won: {skywars["games_played_skywars"] - skywars["losses"]}, Souls: {skywars["souls"]}')
        embed.set_image(url=f'http://crafatar.com/renders/body/{uuid}.jpg?overlay')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(stats(bot))