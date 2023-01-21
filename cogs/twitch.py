import os
import requests
import discord
import json
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import utils, app_commands

load_dotenv()
client_id = os.getenv('TWITCH_CLIENT_ID')
secret = os.getenv('TWITCH_SECRET')


def check_live(channel_name: str):
    # get OAUTH2
    data = {'code': 'channel:view:*',
            'grant_type': 'client_credentials',
            'redirect_uri': 'http://localhost',
            'client_id': client_id,
            'client_secret': secret}
    endpoint = 'https://id.twitch.tv/oauth2/token'

    request = requests.post(endpoint, data=data)
    authcode = request.json()['access_token']

    params = {"user_login": channel_name.lower()}
    endpoint = f'https://api.twitch.tv/helix/streams'
    channel = requests.get(endpoint, headers={'Authorization': 'Bearer ' + authcode, 'Client-Id': client_id}, params=params)
    data = channel.json()

    if not data["data"]:
        return False

    elif data['data'][0]['type'] == 'live':
        userdata = data['data'][0]
        return userdata


async def create_embed(result: dict):
    embed = discord.Embed(title=result["title"], url=f'https://twitch.tv/{result["user_login"]}',
                          colour=discord.Colour.dark_purple())
    embed.set_image(url=result["thumbnail_url"].replace("-{width}x{height}", ""))
    embed.set_author(name=result["user_name"])
    embed.set_footer(
        text=f'made by unseeyou | stream started at {result["started_at"].replace("-", "/").replace("T", ", ").replace("Z", "") + " UTC +0"}')
    embed.set_thumbnail(url=f"https://static-cdn.jtvnw.net/ttv-boxart/{result['game_id']}.jpg")
    embed.add_field(name=f'Playing', value=result["game_name"])

    return embed


async def send_message(embed, guild_id, channel, jsonfile, result):
    notif_msg = jsonfile[str(guild_id)]["message"].replace("[USER]", result["user_name"]).replace("[PING]", f"{'<@&'+str(jsonfile[str(guild_id)]['ping-role'])+'>' if jsonfile[str(guild_id)]['ping-role'] is not None else '@everyone'}")
    notif_msg = notif_msg + f' [stream started at {result["started_at"].replace("-", "/").replace("T", ", ").replace("Z", "") + " UTC +0"}]'
    try:
        messages = [msg.content async for msg in channel.history(limit=50)]
        if messages:
            if notif_msg in messages:
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

    def cog_unload(self):
        self.live_notifs_loop.cancel()

    @tasks.loop(seconds=20)
    async def live_notifs_loop(self):
        try:
            with open('streamers.json', 'r') as file:
                guild_ids = []
                channel_ids = []
                json_file = json.load(file)
                # Makes sure the json isn't empty before continuing.
                if json_file is not None:
                    for i in json_file:
                        guild_ids.append(i)
                        channel_ids.append(json_file[i]["notif-channel"])
                else:
                    print("File is empty")
                # iterate over each server
                for server in json_file:
                    for i in json_file[server]["streamers"]:
                        output = check_live(i)
                        if output:
                            embed = await create_embed(result=output)
                            guild = self.bot.get_guild(int(server))
                            channel = utils.get(guild.text_channels, id=json_file[server]["notif-channel"])
                            await send_message(embed=embed, result=output, guild_id=server, jsonfile=json_file, channel=channel)
                        else:
                            pass
                file.close()
        except Exception as err:
            print('BIG FAT ERROR:', err)
            pass

    @live_notifs_loop.before_loop
    async def before_live_notifs(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    @app_commands.command(description="custom twitch notifications")
    @app_commands.describe(streamer_names="all the streamers you want notifications for seperated by commas",
                           notif_channel="the text channel the notificatoin will be sent to",
                           message="the message sent, using [USER] as where the name goes & [PING] as where the ping goes",
                           ping_role="the role being pinged in the notification [optional, otherwise @everyone ping]")
    async def add_live_alerts(self, ctx: discord.Interaction, streamer_names: str, notif_channel: discord.TextChannel, message: str, ping_role: discord.Role = None):
        try:
            await ctx.response.defer(ephemeral=True)
            with open('streamers.json', 'r') as file:
                json_file = json.load(file)
                json_file[str(ctx.guild.id)] = {"streamers": [name.lower() for name in streamer_names.replace(" ","").split(',')], "notif-channel": int(notif_channel.id), "ping-role": int(ping_role.id) if ping_role else None, "message": message}
                file.close()
            with open('streamers.json', 'w') as write_file:
                json_file = json.dumps(json_file, indent=4)  # makes the json pretty (gives proper formatting)
                write_file.write(str(json_file).replace("'", '"'))
                write_file.close()
            await ctx.followup.send('Alert added! Try going live as a test if possible and create an issue on the support server if it does not work.')
        except BaseException as err:
            print(err)

    @app_commands.command(description='clears the live notifications for current server')
    async def clear_live_notifications(self, ctx: discord.Interaction):
        await ctx.response.defer(ephemeral=True)
        try:
            await ctx.response.defer(ephemeral=True)
            with open('streamers.json', 'r') as file:
                json_file = json.load(file)
                del json_file[str(ctx.guild.id)]
                file.close()
            with open('streamers.json', 'w') as write_file:
                json_file = json.dumps(json_file, indent=4)  # makes the json pretty (gives proper formatting)
                write_file.write(str(json_file).replace("'", '"'))  # python uses "'"s in dicts
                write_file.close()
            await ctx.followup.send('Alert added! Try going live as a test if possible and create an issue on the support server if it does not work.')
        except BaseException as err:
            print(err)


async def setup(bot):
    await bot.add_cog(TwitchStuff(bot))
