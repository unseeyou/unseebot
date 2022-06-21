import json
import discord
import os
import time
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
import math

load_dotenv()
TOKEN = os.getenv("HYPIXEL_API")

async def request_stats(name):
    async with aiohttp.ClientSession() as session:
        request = await session.get(f'https://api.hypixel.net/player?name={name}&key={TOKEN}')
        json = await request.json()
    if json["success"] is not False and json["player"] is not None:
        cache_stats(name, json) # only saves data if there is no error code
    return json

def cache_stats(playername,stats):
    filename = f'{playername.lower()}-stats.txt'
    folder = 'hystats-data'
    with open(f'cogs/{folder}/{filename}','w') as file:
        file.write(json.dumps(stats)) # saves each player's data in their own file
    return filename

def get_cache_data(playername):
    filename = f'{playername.lower()}-stats.txt'
    folder = 'hystats-data'
    with open(f'cogs/{folder}/{filename}','r') as file:
        return json.load(file) # opens player's data file and gets the json inside

def delete_old_data(ctx):
    print('requested old data delete')
    try:
        files = os.listdir('cogs/hystats-data/')
        for file in files:
            x = os.stat('cogs/hystats-data/'+file)
            age = (time.time() - x.st_mtime)
            if int(age) >= 60:
                os.remove('cogs/hystats-data/'+file)
                print(f'deleted {file}')
            else:
                pass

    except BaseException as err:
        await ctx.send(f"Unexpected {err=}, {type(err)=}")

    print('deleted data')
    return True

def create_embed(data):
    json = data # creates embed
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
    embed.add_field(name=f'{username}', value='Hypixel Achievement Points: ' + str(player["achievementPoints"]),
                    inline=False)
    embed.add_field(name='Hypixel Rank', value=f"{username}'s Rank: {rank}")
    embed.add_field(name='Hypixel Level', value=f" Hypixel Level: {level}")
    embed.add_field(name='Duels Stats',
                    value=f'Games Played: {duels["games_played_duels"]}, Games Won: {duels["wins"]}', inline=False)
    embed.add_field(name="Bedwars Stats",
                    value=f'Games Played: {bedwars["games_played_bedwars"]}, Games Won: {bedwars["wins_bedwars"]}',
                    inline=False)
    embed.add_field(name="Skywars Stats",
                    value=f'Games Played: {skywars["games_played_skywars"]}, Games Won: {skywars["wins"]}, Souls: {skywars["souls"]}')
    embed.set_image(url=f'http://crafatar.com/renders/body/{uuid}.jpg?overlay')
    return embed


class stats(commands.Cog):
    @commands.command()
    async def hystats(self, ctx, msg=None):
        json = await request_stats(msg)
        if json["success"] and json["player"] is not None:
            try:
                embed = create_embed(json)
                await ctx.send(embed=embed)

            except Exception:
                await ctx.send('Error: Insufficient Data or Player does not exist/have a premium account')

        elif not json["success"] and "recently" in json["cause"]:
            embed = create_embed(get_cache_data(msg))
            await ctx.send(embed=embed)

        elif json["success"] and json["player"] is None:
            await ctx.send('Error: Player not found')

        else:
            await ctx.send(f'Error: {json["cause"]}')

        delete_old_data(ctx)

def setup(bot):
    bot.add_cog(stats(bot))
