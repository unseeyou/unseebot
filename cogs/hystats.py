import json
import discord
import os
import time
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
import math
import datetime

load_dotenv()
TOKEN = os.getenv("HYPIXEL_API")


async def request_stats(name):
    async with aiohttp.ClientSession() as session:
        request = await session.get(f'https://api.hypixel.net/player?name={name}&key={TOKEN}')
        json = await request.json()
    if json["success"] is not False and json["player"] is not None:
        cache_stats(name, json)  # only saves data if there is no error code
    return json


def cache_stats(playername, stats):
    filename = f'{playername.lower()}-stats.txt'
    folder = 'hystats-data'
    with open(f'cogs/{folder}/{filename}', 'w') as file:
        file.write(json.dumps(stats))  # saves each player's data in their own file
    return filename


def get_cache_data(playername):
    filename = f'{playername.lower()}-stats.txt'
    folder = 'hystats-data'
    with open(f'cogs/{folder}/{filename}', 'r') as file:
        return json.load(file)  # opens player's data file and gets the json inside


def delete_old_data():
    try:
        files = os.listdir('cogs/hystats-data/')
        for file in files:
            x = os.stat('cogs/hystats-data/' + str(file))
            age = (time.time() - x.st_mtime)
            if int(age) >= 60:
                os.remove('cogs/hystats-data/' + str(file))
            else:
                pass

    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")

    return True


def create_embed(data):
    json = data  # creates embed
    try:
        playerdata = json["player"]
    except BaseException:
        playerdata = None
    try:
        stats = playerdata["stats"]
    except BaseException:
        stats = None

    try:
        achievement_points = str(json["player"]["achievementPoints"])
    except BaseException:
        achievement_points = 0
    try:
        duels = stats["Duels"]
        try:
            duels_games = duels["games_played_duels"]
        except BaseException:
            duels_games = 0
        try:
            duels_wins = duels["wins"]
        except BaseException:
            duels_wins = 0
    except BaseException:
        duels_wins = 0
        duels_games = 0

    try:
        bedwars = stats["Bedwars"]
        try:
            bedwars_games = bedwars["games_played_bedwars"]
        except BaseException:
            bedwars_games = 0
        try:
            bedwars_wins = bedwars["wins_bedwars"]
        except BaseException:
            bedwars_wins = 0

    except BaseException:
        bedwars_games = 0
        bedwars_wins = 0

    try:
        skywars = stats["SkyWars"]
        try:
            skywars_games = skywars["games_played_skywars"]
        except BaseException:
            skywars_games = 0
        try:
            skywars_wins = skywars["wins"]
        except BaseException:
            skywars_wins = 0
        try:
            souls = skywars["souls"]
        except BaseException:
            souls = 0

    except BaseException:
        skywars_wins = 0
        skywars_games = 0
        souls = 0
    try:
        network_experience = int(playerdata["networkExp"])
        network_level = (math.sqrt((2 * int(network_experience)) + 30625) / 50) - 2.5
        level = round(network_level, 2)
    except BaseException:
        level = 0
    uuid = playerdata["uuid"]
    player = json["player"]
    try:
        lastlog = datetime.datetime.fromtimestamp(int(player["lastLogin"] / 1000)).strftime("%d/%m/%Y %H:%M:%S")
    except Exception as err:
        lastlog = str(err)
    try:
        firstLog = datetime.datetime.fromtimestamp(int(player["firstLogin"] / 1000)).strftime("%d/%m/%Y %H:%M:%S")
    except Exception as err:
        firstLog = str(err)
    try:
        if player["displayname"] == 'Technoblade':
            rank = 'PIG+++'
        elif "rank" in player:
            rank = player["rank"]
        elif 'monthlyPackageRank' in player and player['monthlyPackageRank'] == "SUPERSTAR":
            rank = 'MVP++'
        elif "newPackageRank" in player and player["newPackageRank"] == 'VIP_PLUS' or 'MVP_PLUS':
            rank = player["newPackageRank"].replace('_PLUS', '+')
        else:
            rank = 'Normal'
    except BaseException:
        rank = 'Normal'
    username = player["displayname"]
    embed = discord.Embed(title='HyStats', colour=discord.Colour.dark_gold())
    embed.add_field(name=f'{username}', value='Hypixel Achievement Points: ' + str(achievement_points),
                    inline=False)
    embed.add_field(name='Hypixel Rank', value=f"{username}'s Rank: {rank}")
    embed.add_field(name='Hypixel Level', value=f" Hypixel Level: {level}")
    embed.add_field(name='Last Login', value=f"{username} last logged on at: {lastlog}", inline=False)
    embed.add_field(name='First Login', value=f"{username} first logged at: {firstLog}", inline=False)
    embed.add_field(name='Duels Stats',
                    value=f'Games Played: {duels_games}, Games Won: {duels_wins}', inline=False)
    embed.add_field(name="Bedwars Stats",
                    value=f'Games Played: {bedwars_games}, Games Won: {bedwars_wins}',
                    inline=False)
    embed.add_field(name="Skywars Stats",
                    value=f'Games Played: {skywars_games}, Games Won: {skywars_wins}, Souls: {souls}')
    if username == 'Technoblade':
        embed.set_image(url='https://hypixel.net/attachments/image-26-png.3025155/')
    else:
        embed.set_image(url=f'https://crafthead.net/armor/bust/{uuid}')
    return embed


class stats(commands.Cog):
    @commands.hybrid_command(help='hypixel stats! very cool.')
    async def hystats(self, ctx, username: str):
        json = await request_stats(username)
        if json["success"] and json["player"] is not None:
            try:
                embed = create_embed(json)
                await ctx.send(embed=embed)

            except BaseException as error:
                await ctx.send(f'Exception: {error}, are you searching up a cracked minecraft account?')

        elif not json["success"] and "recently" in json["cause"]:
            try:
                embed = create_embed(get_cache_data(username))
                await ctx.send(embed=embed)
            except BaseException as error:
                await ctx.send(f'Exception from cache: {error}')

        elif json["success"] and json["player"] is None:
            await ctx.send('Error: Player not found')

        else:
            await ctx.send(f'Error: {json["cause"]}')

        delete_old_data()


async def setup(bot):
    await bot.add_cog(stats(bot))
