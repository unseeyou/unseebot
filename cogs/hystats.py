import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
import math

load_dotenv()
TOKEN = os.getenv("HYPIXEL_API")

class stats(commands.Cog):
    @commands.command()
    async def hystats(self, ctx, msg=None):
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://api.hypixel.net/player?name={msg}&key={TOKEN}')
            json = await request.json()

        if json["success"] and json["player"] != None:
            playerdata = json["player"]
            stats = playerdata["stats"]
            duels = stats["Duels"]
            bedwars = stats["Bedwars"]
            skywars = stats["SkyWars"]
            network_experience = int(playerdata["networkExp"])
            network_level = (math.sqrt((2 * network_experience) + 30625) / 50) - 2.5
            level = round(network_level, 2)
            uuid = playerdata["uuid"]
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
            embed.add_field(name='Duels Stats',value=f'Games Played: {duels["games_played_duels"]}, Games Won: {duels["wins"]}',inline=False)
            embed.add_field(name="Bedwars Stats",value=f'Games Played: {bedwars["games_played_bedwars"]}, Games Won: {bedwars["wins_bedwars"]}',inline=False)
            embed.add_field(name="Skywars Stats",value=f'Games Played: {skywars["games_played_skywars"]}, Games Won: {skywars["games_played_skywars"] - skywars["losses"]}, Souls: {skywars["souls"]}')
            embed.set_image(url=f'http://crafatar.com/renders/body/{uuid}.jpg?overlay')
            await ctx.send(embed=embed)

        elif json["success"] and json["player"] == None:
            await ctx.send('Error: Player not found')

        else:
            await ctx.send(f'Error: {json["cause"]}')

def setup(bot):
    bot.add_cog(stats(bot))