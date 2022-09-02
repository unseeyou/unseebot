import discord
from discord.ext import commands
import asyncio
import random


class Hack(commands.Cog):
    @commands.hybrid_command(help="*in epic hacker voice*: I'm in. ")
    async def hack(self, ctx, user: discord.User):
        await ctx.reply("`INITATING UserHack.exe`")
        await ctx.send(f"hacking {user.name}")
        await asyncio.sleep(1)
        # print('finished sleeping')
        await ctx.send(f"{user.name}'s server nick is: `{user.display_name}`")
        await ctx.send(f"getting ip address...")
        await asyncio.sleep(1)
        # print('finished sleeping')
        await ctx.send("getting ip address... COMPLETE")
        await ctx.send(
            f'OUTPUT: {random.randint(10, 99)}.{random.randint(100, 999)}.{random.randint(1, 10)}.{random.randint(6, 9)}:{random.randint(11111, 33333)}')
        await asyncio.sleep(0.5)
        await ctx.send('Getting email address...')
        await asyncio.sleep(1)
        await ctx.send("getting email address... COMPLETE")
        emails = ['isStinky', 'kfc', 'myDaddy', 'isStupid', 'gotHacked', 'isBad']
        passwords = ['stinkyballs321', 'hairyballs798', 'iLikeMen', 'Password', 'password',
                     'youwillneverguessmypassword']
        await ctx.send(f"OUTPUT: `{user.name}@{random.choice(emails)}.com`")
        await ctx.send("getting discord login information...")
        await ctx.send("getting discord login information... SUCCESS")
        await asyncio.sleep(1)
        await ctx.send(f"Username: {user.name}")
        await ctx.send(f"Password: {random.choice(passwords)}")
        await ctx.send(f"successfully hacked {user.name} [User ID: {user.id}]")
        await ctx.send('`selling user data to government and global businesses...`')
        await asyncio.sleep(1)
        await ctx.send('`OPERATION COMPLETE`')
        await ctx.send('`Deactivating Hacking Software`')


async def setup(bot):
    await bot.add_cog(Hack(bot))
