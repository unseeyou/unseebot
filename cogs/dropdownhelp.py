import discord
from discord.ext import commands

class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Page 1",description="This is help page 1!"),
            discord.SelectOption(label="Page 2",description="This is help page 2!"),
            discord.SelectOption(label="Page 3",description="This is help page 3!"),
            discord.SelectOption(label="Page 4",description="This is help page 4!"),
            discord.SelectOption(label="Page 5",description="This is the annoucement page!"),
            ]
        super().__init__(placeholder="please choose an option",max_values=1,min_values=1,options=options)

    global embed,embed2,embed3,embed4,embed5

    embed = discord.Embed(title="Help", description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
    embed.add_field(name='help', value='usage: `>help`', inline=False)
    embed.add_field(name='hello', value='usage: `>hello`', inline=False)
    embed.add_field(name='invite', value='usage: `>invite`',inline=False)
    embed.add_field(name='yt', value='usage: `>yt` then click on the link', inline=False)
    embed.add_field(name='betrayal', value='usage: `>betrayal` then click on the link', inline=False)
    embed.add_field(name='fish', value='usage: `>fish` then click on the link', inline=False)
    embed.add_field(name='pp', value='usage: `>pp {keyword or @user}`', inline=False)
    embed.set_footer(text='page 1 of 5')

    embed2 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
    embed2.add_field(name='doodle', value='usage: `>doodle` then click on the link', inline=False)
    embed2.add_field(name='word', value='usage: `>word` then click on the link',inline=False)
    embed2.add_field(name='bwstats', value='usage: `>bwstats {playername}` then click on the link',inline=False)
    embed2.add_field(name='sudo', value='usage: `>sudo {@user} {message}`',inline=False)
    embed2.add_field(name='unseebot', value='usage: `>unseebot` then check your dms', inline=False)
    embed2.add_field(name='github', value='usage: `>github` then click on the link', inline=False)
    embed2.add_field(name='urban or urb', value='usage: `>urban {keyword}`', inline=False)
    embed2.set_footer(text='page 2 of 5')

    embed3 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
    embed3.add_field(name='8ball', value='usage: `>8ball {question}`', inline=False)
    embed3.add_field(name='cat', value='usage: `>cat`',inline=False)
    embed3.add_field(name='dog', value='usage: `>dog`', inline=False)
    embed3.add_field(name='meme', value='usage: `>meme` and then buttons', inline=False)
    embed3.add_field(name='tictactoe or XO', value='usage: `>XO` then play', inline=False)
    embed3.add_field(name='epic', value='usage: `>epic {keyword or @user}`', inline=False)
    embed3.add_field(name='hystats', value='usage: `>hystats {playername}` **requires you to have played games of bedwars, skywars and duels to work**',inline=False)
    embed3.set_footer(text='page 3 of 5')

    embed4 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
    embed4.add_field(name='Special Announcement', value='Additional Hypixel Statistics Commands will be added to unseebot SOON!!!')
    embed4.add_field(name='unseebot extra feature!', value='name a text channel `join-leave` and unseebot will post welcome messages there!', inline=False)
    embed4.add_field(name='Thank You for using unseebot', value='<3')
    embed4.add_field(name='Any Ideas?', value='Please DM unseeyou#2912 if you have any ideas you want to add to unseebot')
    embed4.add_field(name='Update Announcements', value='It is recommended that you follow the dev annoucements channel in this server (https://discord.gg/qShcaXXhaj) to get updates on unseebot development and upcoming features', inline=False)
    embed4.set_footer(text='page 5 of 5')

    embed5 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
    embed5.add_field(name='echo', value='usage: `>echo {message}`',inline=False)
    embed5.add_field(name='triggered', value='usage: `>triggered {username}`', inline=False)
    embed5.set_footer(text='page 4 of 5')
    async def callback(self,interaction):
        if self.values[0] == "Page 1":
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "Page 2":
            await interaction.response.edit_message(embed=embed2)
        elif self.values[0] == "Page 3":
            await interaction.response.edit_message(embed=embed3)
        elif self.values[0] == "Page 4":
            await interaction.response.edit_message(embed=embed5)
        elif self.values[0] == "Page 5":
            await interaction.response.edit_message(embed=embed4)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(Select())

class Commands(commands.Cog):
    @commands.command()
    async def help(self,ctx):
        await ctx.send(embed=embed,view=SelectView())

def setup(bot):
    bot.add_cog(Commands(bot))