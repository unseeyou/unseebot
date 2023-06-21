import datetime
import os
from json import JSONDecodeError

import requests
import discord
import json
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import utils, app_commands
from asyncio import sleep

load_dotenv()
client_id = os.getenv('TWITCH_CLIENT_ID')
secret = os.getenv('TWITCH_SECRET')


def get_auth_token():
    data = {'code': 'channel:view:*',
            'grant_type': 'client_credentials',
            'redirect_uri': 'http://localhost',
            'client_id': client_id,
            'client_secret': secret}
    endpoint = 'https://id.twitch.tv/oauth2/token'

    request = requests.post(endpoint, data=data)
    authcode = request.json()['access_token']

    with open('twitch_0Auth2_code.txt', 'w') as file:
        file.write(authcode)
        file.close()

    return True


async def check_live(channel_name: str):
    try:
        # get OAUTH2
        with open('twitch_0Auth2_code.txt', 'r') as file:
            authcode = file.read()
            file.close()

        params = {"user_login": channel_name.lower()}
        endpoint = f'https://api.twitch.tv/helix/streams'
        channel = requests.get(endpoint, headers={'Authorization': 'Bearer ' + authcode, 'Client-Id': client_id}, params=params)
        data = channel.json()

        if not data["data"]:
            False

        elif data['data'][0]['type'] == 'live':
            userdata = data['data'][0]
            return userdata
    except Exception:
        await sleep(1)
        await check_live(channel_name)


async def create_embed(result: dict):
    embed = discord.Embed(title=result["title"], url=f'https://twitch.tv/{result["user_login"]}',
                          colour=discord.Colour.dark_purple())
    embed.set_image(url=result["thumbnail_url"].replace("-{width}x{height}", ""))
    embed.set_author(name=result["user_name"])  # url=result["profile_url"]
    embed.set_footer(
        text=f'made by unseeyou | stream started at {result["started_at"].replace("-", "/").replace("T", ", ").replace("Z", "") + " UTC +0"}')
    embed.set_thumbnail(url=f"https://static-cdn.jtvnw.net/ttv-boxart/{result['game_id']}.jpg")
    embed.add_field(name=f'Playing', value=result["game_name"])
    # date stuff
    stream_time = result["started_at"]
    year = int(stream_time[:4])
    month = int(stream_time[5:7])
    day = int(stream_time[8:10])
    hour = int(stream_time[11:13])
    second = int(stream_time[14:16])
    date = int(datetime.datetime(year=year, month=month, day=day, hour=hour, second=second).timestamp())

    embed.add_field(name='Stream Started', value=f'<t:{date}:R>')
    return embed


async def send_message(embed, channel, message, result, ping_role, user):
    uid = result["started_at"].replace("-", "/").replace("T", ", ").replace("Z", "")  # unique identifier
    notif_msg = message.replace('[PING]', f"{ping_role.mention}").replace('[USER]', user)
    try:
        embeds = [msg.embeds async for msg in channel.history(limit=50)]
        messages = []

        for i in embeds:
            try:
                messages.append(str(i[0].footer))
            except IndexError:
                pass

        if messages:
            if f"EmbedProxy(text='made by unseeyou | stream started at {uid} UTC +0')" in messages:
                pass
            else:
                await channel.send(notif_msg, embed=embed)
        else:
            await channel.send(notif_msg, embed=embed)
    except Exception as err:
        print("Brej: "+str(err))


class TwitchStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.live_notifs_loop.start()
        self.update_auth.start()

    def cog_unload(self):
        self.live_notifs_loop.cancel()
        self.update_auth.cancel()

    @tasks.loop(seconds=24)
    async def live_notifs_loop(self):
        try:
            with open('streamers.json', 'r') as file:
                json_file = json.load(file)
                # Makes sure the json isn't empty before continuing.
                if json_file is not None:
                    pass
                else:
                    print("File is empty")
                # iterate over each server
                for streamer in json_file:
                    print('checking', streamer)
                    output = await check_live(streamer)
                    if output:
                        embed = await create_embed(result=output)
                        for guild in json_file[streamer]:
                            server = self.bot.get_guild(int(guild['serverID']))
                            channel = utils.get(server.text_channels, id=guild["ChannelID"])
                            await send_message(embed=embed, channel=channel, ping_role=utils.get(
                                server.roles, id=guild["pingroleID"]), result=output,
                                               message=guild["message"], user=output["user_name"])

                    else:
                        pass
                file.close()
        except Exception as err:
            print('BIG FAT ERROR:', err)
            pass

    @tasks.loop(seconds=120)
    async def update_auth(self):
        get_auth_token()

    @live_notifs_loop.before_loop
    async def before_live_notifs(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(description="custom twitch notifications")
    @app_commands.describe(streamer_names="all the streamers you want notifications for seperated by commas",
                           notif_channel="the text channel the notificatoin will be sent to",
                           message="the message sent, using [USER] as where the name goes & [PING] as where the ping goes",
                           ping_role="the role being pinged in the notification [optional, otherwise @everyone ping]")
    async def add_live_alerts(self, ctx: discord.Interaction, streamer_names: str, notif_channel: discord.TextChannel, message: str, ping_role: discord.Role = None):
        try:
            await ctx.response.defer(ephemeral=True)
            server_details = {
                "serverID": ctx.guild_id,
                "ChannelID": notif_channel.id,
                "message": message,
                "pingroleID": ping_role.id if ping_role is not None else None,
            }  # new structure only searches for each streamer once per cycle instead of multiple times
            with open('streamers.json', 'r') as file:
                try:
                    json_file = json.load(file)
                except JSONDecodeError:
                    json_file = {}
                for streamer in list(set([l.strip() for l in streamer_names.split(',')])):  # if a user puts a streamer more than once we don't want
                    try:  # messages getting sent, so this prevents it.
                        json_file[streamer] = json_file[streamer].append(server_details)  # if it already exists just append to the list
                    except KeyError:
                        json_file[streamer] = [server_details]  # otherwise just make a new list
            with open('streamers.json', 'w') as write_file:
                json_file = json.dumps(json_file, indent=4)  # makes the json pretty (gives proper formatting)
                write_file.write(str(json_file).replace("'", '"'))  # same here
                write_file.close()
            await ctx.followup.send('Alert/s added successfully!')
        except BaseException as err:
            print(err)
            await ctx.followup.send(f'Error while creating alerts: {str(err)}')

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(description='clears the live notifications for current server')
    async def clear_live_notifications(self, ctx: discord.Interaction):
        await ctx.response.defer(ephemeral=True)
        try:
            with open('streamers.json', 'r') as file:
                json_file = json.load(file)
                for streamer in json_file:
                    for server in json_file[streamer]:
                        if server["serverID"] == ctx.guild_id:
                            del server
                file.close()
            with open('streamers.json', 'w') as write_file:
                json_file = json.dumps(json_file, indent=4)  # makes the json pretty (gives proper formatting)
                write_file.write(str(json_file).replace("'", '"'))  # python uses "'"s in dicts
                write_file.close()
            await ctx.followup.send('Alerts removed! Please create a post in the forum of my help server if it did not work. (/server for invite)')
        except BaseException as err:
            print(err)


async def setup(bot):
    await bot.add_cog(TwitchStuff(bot))
