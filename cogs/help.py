import discord
from discord.ext import commands
from discord.ui import Button, View

class HelpCommand(commands.Cog):
    @commands.command()
    async def help(self, ctx, message=None):
        embed = discord.Embed(title="Help", description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
        embed.add_field(name='help', value='usage: `>help`', inline=False)
        embed.add_field(name='hello', value='usage: `hello`', inline=False)
        embed.add_field(name='invite', value='usage: `>invite`',inline=False)
        embed.add_field(name='yt', value='usage: `>yt` then click on the link', inline=False)
        embed.add_field(name='betrayal', value='usage: `>betrayal` then click on the link', inline=False)
        embed.add_field(name='fish', value='usage: `>fish` then click on the link', inline=False)
        embed.add_field(name='pp', value='usage: `>pp {keyword or @user}`', inline=False)
        embed.set_footer(text='page 1 of 4')

        embed2 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
        embed2.add_field(name='doodle', value='usage: `>doodle` then click on the link', inline=False)
        embed2.add_field(name='word', value='usage: `>word` then click on the link',inline=False)
        embed2.add_field(name='bwstats', value='usage: `>bwstats {playername}` then click on the link',inline=False)
        embed2.add_field(name='sudo', value='usage: `>sudo {@user} {message}`',inline=False)
        embed2.add_field(name='unseebot', value='usage: `>unseebot` then check your dms', inline=False)
        embed2.add_field(name='github', value='usage: `>github` then click on the link', inline=False)
        embed2.add_field(name='urban or urb', value='usage: `>urban {keyword}`', inline=False)
        embed2.set_footer(text='page 2 of 4')

        embed3 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
        embed3.add_field(name='8ball', value='usage: `>8ball {question}`', inline=False)
        embed3.add_field(name='cat', value='usage: `>cat`',inline=False)
        embed3.add_field(name='dog', value='usage: `>dog`', inline=False)
        embed3.add_field(name='meme', value='usage: `>meme` and then buttons', inline=False)
        embed3.add_field(name='tictactoe or XO', value='usage: `>XO` then play', inline=False)
        embed3.add_field(name='epic', value='usage: `>epic {keyword or @user}`', inline=False)
        embed3.add_field(name='hystats', value='usage: `>hystats {playername}` **requires you to have played games of bedwars, skywars and duels to work**',inline=False)
        embed3.set_footer(text='page 3 of 4')

        embed4 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
        embed4.add_field(name='Special Announcement', value='Additional Hypixel Statistics Commands will be added to unseebot SOON!!!')
        embed4.add_field(name='Thank You for using unseebot', value='<3')
        embed4.add_field(name='Any Ideas?', value='Please DM unseeyou#2912 if you have an idea you want to add to unseebot')
        embed4.add_field(name='Update Announcements', value='It is recommended that you follow the dev annoucements channel in this server (https://discord.gg/qShcaXXhaj) to get updates on unseebot development and upcoming features', inline=False)
        embed4.set_footer(text='page 4 of 4')

        if message == None:
            button = Button(label='Page 2', style=discord.ButtonStyle.blurple)
            button2 = Button(label='Page 1', style=discord.ButtonStyle.blurple)
            button3 = Button(label='Page 3', style=discord.ButtonStyle.blurple)
            button4 = Button(label='Page 4', style=discord.ButtonStyle.blurple)

            async def button_callback(interaction):
                await interaction.response.edit_message(embed=embed2)

            async def buttoncallback(interaction):
                await interaction.response.edit_message(embed=embed)

            async def butcal(interaction):
                await interaction.response.edit_message(embed=embed3)

            async def callback3(interaction):
                await interaction.response.edit_message(embed=embed4)

            button.callback = button_callback
            button2.callback = buttoncallback
            button3.callback = butcal
            button4.callback = callback3
            view = View()
            view.add_item(button2)
            view.add_item(button)
            view.add_item(button3)
            view.add_item(button4)
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.send('this page does not exist. please run >help')

def setup(bot):
    bot.add_cog(HelpCommand(bot))