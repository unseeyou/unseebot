import os
import requests
import discord
import json
from dotenv import load_dotenv
from discord.ext import commands, tasks

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

    endpoint = f'https://api.twitch.tv/helix/streams?user_login={channel_name.lower()}'
    channel = requests.get(endpoint, headers={'Authorization': 'Bearer ' + authcode,
                                              'Client-Id': client_id})
    data = channel.json()

    if not data["data"]:
        return False

    elif data['data'][0]['type'] == 'live':
        userdata = data['data'][0]
        return userdata


async def create_embed(result: dict, notif_channels: list):
    notif_msg = f'https://twitch.tv/{result["user_login"]} '+'@everyone {} is live! [stream started at {}]'.format(result["user_name"], result["started_at"].replace("-", "/").replace("T", ", ").replace("Z", "") + " UTC +0")
    embed = discord.Embed(title=result["title"], url=f'https://twitch.tv/{result["user_login"]}',
                          colour=discord.Colour.dark_purple())
    embed.set_image(url=result["thumbnail_url"].replace("-{width}x{height}", ""))
    embed.set_author(name=result["user_name"])
    embed.set_footer(
        text=f'made by unseeyou • stream started at {result["started_at"].replace("-", "/").replace("T", ", ").replace("Z", "") + " UTC +0"}')
    embed.set_thumbnail(url=f"https://static-cdn.jtvnw.net/ttv-boxart/{result['game_id']}.jpg")
    embed.add_field(name=f'Playing', value=result["game_name"])
    for ctx in notif_channels:
        try:
            messages = [msg.content async for msg in ctx.history(limit=50)]
            if messages:
                if notif_msg in messages:
                    return False
                else:
                    await ctx.send(notif_msg)
                    return True
            else:
                await ctx.send(notif_msg)
                return True
        except Exception as err:
            print("OOPSIES! {}".format(err))


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
                notif_channels = []
                streamers = json.loads(file.read())
                # Makes sure the json isn't empty before continuing.
                if streamers is not None:
                    for guild in self.bot.guilds:
                        if str(guild.id) in streamers:
                            for channel in guild.channels:
                                if 'live-notifications' in channel.name:
                                    notif_channels.append(channel)
                else:
                    pass
                # iterate over each server
                for streamer in streamers:
                    for user in streamers[streamer]:
                        output = check_live(user)
                        if output:
                            await create_embed(result=output, notif_channels=notif_channels)
                        else:
                            pass
                file.close()

        except Exception as err:
            print('BIG FAT ERROR:', err)

    @live_notifs_loop.before_loop
    async def before_live_notifs(self):
        print('waiting...')
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(TwitchStuff(bot))
