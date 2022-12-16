import discord
from discord.ext.commands import has_permissions
from discord.ext import commands
from discord.ui import Button, View
import os
import asyncio
import time
from dotenv import load_dotenv

load_dotenv()

# helpcommand = commands.HelpCommand.

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=[';', '//'], case_insensitive=True, intents=intents)
TOKEN = os.getenv('MODBOT_TOKEN')


@bot.event
async def on_ready():
    print('loading slash commands')
    await bot.tree.sync()
    print('MODERATION BOT ONLINE')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_member_join(member):
    try:
        r = discord.utils.get(member.guild.roles, name='member')
        await member.add_roles(r)
    except Exception:
        pass


@bot.event
async def on_message(message):
    if message.channel.name == 'github-updates':
        await message.publish()
    
    
@bot.command(aliases=['bc'], help='still working on it')
@has_permissions(administrator=True)
async def broadcast(ctx, *, message=None):
    channels = ctx.guild.text_channels
    for channel in channels:
        await channel.send(f'**Server Broadcast:** {message}')


@bot.hybrid_command(help='run this if mute role isnt working')
@has_permissions(administrator=True)
async def setupmute(ctx):
    msg = await ctx.send('`this may take a while if you have lots of text channels...`')
    mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
    for channel in ctx.guild.text_channels:
        await channel.set_permissions(mutedRole, send_messages=False)
    embed = discord.Embed(title='COMPLETED!', colour=discord.Colour.green())
    await msg.delete()
    await ctx.reply(embed=embed)


@bot.command(help='usage: `sudo @mention {message}`')
@has_permissions(administrator=True)
async def sudo(ctx, member: discord.Member, *, message: str = None):
    await ctx.message.delete()
    if message is None:
        await ctx.send(f'SyntaxError: a person and message must be specified')
        return

    webhook = await ctx.channel.create_webhook(name=member.name)
    await webhook.send(
        str(message), username=member.nick, avatar_url=member.avatar)

    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        await webhook.delete()


@bot.hybrid_command(help='usage: `;ping`, gets the current ping of bot')
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong! My ping is `{int(ping)}ms`")
    print(f'Ping: {int(ping)} ms')


@bot.hybrid_command(pass_context=True, nick='usage: `;id`, gets the server/guild ID')
@has_permissions(administrator=True)
async def id(ctx):
    id = ctx.message.guild.id
    await ctx.send(id)


@bot.command(name='clear', aliases=['purge', 'delete', 'del'], help='usage: `;clear {quantity}`')  # clear command
@commands.has_permissions(administrator=True)
async def clear(ctx, quantity: int):
    await ctx.send(f"clearing {quantity} messages")
    channel = ctx.channel
    await channel.purge(limit=int(quantity) + 2)  # clears command usage as well as amount of messages
    time.sleep(0.2)
    msg = await ctx.send(f"cleared {quantity} messages!")
    msg2 = await ctx.send("just a reminder that this bot cannot delete messages more then 2 weeks old")
    time.sleep(2)
    await msg.delete()
    await msg2.delete()


@bot.hybrid_command(help='gives a role', aliases=['giverole'])
@has_permissions(administrator=True)
async def role(ctx, user: discord.Member = None, role: discord.Role = None):
    if user is None:
        user = ctx.message.author
    else:
        pass
    role = discord.utils.get(ctx.guild.roles, name=role.name)
    await user.add_roles(role)


@bot.command(help='totally not sussy!!!')
@has_permissions(administrator=True)
async def roleall(ctx, role: discord.Role):
    role = discord.utils.get(ctx.guild.roles, name=role.name)
    users = ctx.guild.members
    for user in users:
        await user.add_roles(role)


@bot.command(help='the ultimate undo')
@has_permissions(administrator=True)
async def undoroleall(ctx, role: discord.Role):
    role = discord.utils.get(ctx.guild.roles, name=role.name)
    users = ctx.guild.members
    for user in users:
        if 'unseeyou' in user.username:
            pass
        else:
            await user.remove_roles(role)


@bot.hybrid_command(aliases=['rr'], help='trololol')
@has_permissions(administrator=True)
async def removerole(ctx, role: discord.Role, user: discord.Member = None):
    if user is None:
        user = ctx.message.author
    else:
        pass
    await user.remove_roles(role)


@bot.hybrid_command(help='locks down a channel, only admins can talk and unlock it', aliases=['lock', 'ld'])
@has_permissions(administrator=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(ctx.channel.mention + " ***is now in lockdown.***")


@bot.hybrid_command(help='unlocks a channel', aliases=['unlockdown', 'uld', 'ul'])
@has_permissions(administrator=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked.***")


@bot.command(help='changes all the nicknames')
@has_permissions(administrator=True)
async def nickall(ctx, *, nick=None):
    for user in ctx.guild.members:
        try:
            await user.edit(nick=nick)
        except discord.Forbidden:
            pass


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(error)
        await ctx.send(error)


@bot.command(help='B I G   R E D   B U T T O N')
async def button(ctx):
    view = View()
    embed = discord.Embed(title='USE WITH CAUTION', colour=discord.Colour.red())

    async def callback(interaction):
        if ctx.message.author.id == 650923352097292299:
            await interaction.response.send_message('__**SERVER WILL GO BOOM BOOM IN 30 SECONDS**__')
        else:
            await interaction.response.send_message('`Error 69420: you are not unseeyou`', ephemeral=True)

    button = Button(label='DANGER', style=discord.ButtonStyle.danger)
    button.callback = callback
    view.add_item(button)
    await ctx.send(embed=embed, view=view)


@bot.command()
@has_permissions(administrator=True)
async def disguise(ctx, member: discord.Member = None):
    def get_msg(msg):
        if msg.author.id == ctx.message.author.id:
            return msg.content
        else:
            pass

    if member is None:
        await ctx.send('please specify someone to disguise')

    else:
        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name=member.name)
        msg = ctx.message

        while msg.content != '.stop':
            msg = await bot.wait_for("message", check=get_msg)
            await msg.delete()
            if msg.content != '.stop':
                await webhook.send(str(msg.content), username=member.nick, avatar_url=member.avatar)
            else:
                pass
            time.sleep(1)

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()


@bot.command(help='makes an admin role with custom name')
@has_permissions(administrator=True)
async def createadmin(ctx, *, role_name=None):
    if role_name is None:
        role_name = 'ඞ'
        await ctx.send(role_name)
    else:
        pass
    guild = ctx.guild
    perms = discord.Permissions(administrator=True)
    msg = await ctx.send(embed=discord.Embed(title=f'CREATING ADMIN ROLE WITH NAME: @{role_name}',
                                             colour=discord.Colour.dark_blue()).set_footer(text='made by unseeyou'))
    await guild.create_role(name=role_name, permissions=perms)
    await msg.edit(
        embed=discord.Embed(title=f'SUCCESS!', colour=discord.Colour.green()).set_footer(text='made by unseeyou'))


@bot.hybrid_command(help='mute someone!')
@has_permissions(administrator=True)
async def mute(ctx, user: discord.Member = None, *, reason=None):
    if user is None:
        await ctx.send('`Incorrect Usage: No user specified`')
    else:
        mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
        embed = discord.Embed(title="MUTE", description=f"muted {user.mention} for reason: `{reason}`",
                              colour=discord.Colour.red())
        await user.add_roles(mutedRole)
        await user.send(embed=embed)
        await ctx.send(embed=embed)


@bot.hybrid_command(help='unmute someone!')
@has_permissions(administrator=True)
async def unmute(ctx, user: discord.Member = None, *, reason=None):
    if user is None:
        await ctx.send('`Incorrect Usage: No user specified`')
    else:
        mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
        embed = discord.Embed(title="UNMUTE", description=f"unmuted {user.mention} for reason: `{reason}`",
                              colour=discord.Colour.red())
        await user.remove_roles(mutedRole)
        await user.send(embed=embed)
        await ctx.send(embed=embed)


@bot.hybrid_command(name='ban', help='bans a user')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if member is None:
        author = ctx.author
        embed2 = discord.Embed(title='', description=f'{author}, you must mention a valid user')
        await ctx.send(embed2=embed2)
    else:
        embed = discord.Embed(title=f"{member.name} has been banned")
        embed.add_field(name=f"Reason", value=f"{reason}")
        try:
            await member.ban(reason=reason, delete_message_days=0)
        except BaseException as err:
            print(err)
        await ctx.send(embed=embed)
        chnl = discord.utils.get(ctx.guild.channels, name='logs')
        await chnl.send(embed=embed)


async def main():
    async with bot:
        await bot.start(TOKEN)


asyncio.run(main())
