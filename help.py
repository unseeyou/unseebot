import discord
from discord.ext import commands
from discord.ui import Button, View

class HelpCommand(commands.Cog):
    @commands.command()
    async def help(self, ctx, message=None):
        embed = discord.Embed(title="Help", description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
        embed.add_field(name='COMMAND 1: help', value='this is the help command you just used.', inline=False)
        embed.add_field(name='COMMAND 2: join', value='this makes the bot join your current voice channel.',inline=False)
        embed.add_field(name='COMMAND 3: leave', value='this makes the bot leave your current voice channel.',inline=False)
        embed.add_field(name='COMMAND 4: play', value='this plays a single video, from a youtube URL.', inline=False)
        embed.add_field(name='COMMAND 5: pause', value='this pauses what the bot is currently playing.', inline=False)
        embed.add_field(name='COMMAND 6: resume', value='this resumes what you just paused.', inline=False)
        embed.add_field(name='COMMAND 7: hello', value='this lets you say hi to the bot.', inline=False)
        embed.add_field(name='COMMAND 8: invite', value='generates a link for you to invite unseebot to your server',inline=False)
        embed.add_field(name='COMMAND 9: stop', value='this stops the current audio being played.', inline=False)
        embed.set_footer(text='page 1 of 4')

        embed2 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
        embed2.add_field(name='COMMAND 10: yt', value='this creates a youtube together event in your current voice channel.',inline=False)
        embed2.add_field(name='COMMAND 11: betrayal', value='this starts a betrayal.io activity in your voice channel.',inline=False)
        embed2.add_field(name='COMMAND 12: fish', value='this generates a fishington.io activity in your voice channel.', inline=False)
        embed2.add_field(name='COMMAND 13: doodle', value='this generates a doodle crew activity in your voice channel.', inline=False)
        embed2.add_field(name='COMMAND 14: word', value='this generates an awkword activity in your voice channel.',inline=False)
        embed2.add_field(name='COMMAND 15: bwstats', value='this gives a link to the bedwars stats website.',inline=False)
        embed2.add_field(name='COMMAND 16: sudo', value='impersonate your friends and foes. **CAUSE CHAOS**',inline=False)
        embed2.add_field(name='COMMAND 17: unseebot', value='essentially an about me sent in your dms', inline=False)
        embed2.set_footer(text='page 2 of 4')

        embed3 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou",
                               colour=discord.Colour.dark_gold())
        embed3.add_field(name='COMMAND 18: github', value='gives a link to the unseebot github page', inline=False)
        embed3.add_field(name='COMMAND 19: 8ball', value='ask unseebot as yes or no question', inline=False)
        embed3.add_field(name='COMMAND 20: nick', value='changes the nickname of the selected user', inline=False)
        embed3.add_field(name='COMMAND 21: cat', value='shows a picture of cure kitty and tells you about pussies',inline=False)
        embed3.add_field(name='COMMAND 22: dog', value='shows a doggo and gives doggo facts', inline=False)
        embed3.add_field(name='COMMAND 23: playing', value='generates an embed showing audio that is currently being played', inline=False)
        embed3.add_field(name='COMMAND 24: queue', value='lists the current song queue', inline=False)
        embed3.add_field(name='COMMAND 25: loop', value='loops the current song', inline=False)
        embed3.set_footer(text='page 3 of 4')

        embed4 = discord.Embed(title='Help', description="this page sucks lol if you really need help dm unseeyou", colour=discord.Colour.dark_gold())
        embed4.add_field(name='COMMAND 26: skip', value='skips current song in the queue', inline=False)
        embed4.add_field(name='COMMAND 27: meme', value='gets a meme from reddit', inline=False)
        embed4.add_field(name='COMMAND 28: tictactoe or XO', value='launches a game of tic tac toe!', inline=False)
        embed4.add_field(name='COMMAND 29: hystats', value='shows hypixel stats for bedwars, skywars and duels. **Requires you to have played gamemodes to work**',inline=False)
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