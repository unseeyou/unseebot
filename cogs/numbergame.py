import discord
import random
from discord import app_commands
from discord.ext import commands


class NumberGameQuitButton(discord.ui.Button):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.red, label="QUIT", row=y)
        self.x = x
        self.y = y
        self.gameover = False

    async def callback(self, interaction: discord.Interaction):
        view: NumberGameGrid = self.view
        content = f"Game Over! YOU QUIT!!!"
        view.disable_all_buttons()
        await interaction.response.edit_message(content=content, view=view)


class NumberGameButton(discord.ui.Button):
    def __init__(self, x: int, y: int, num: int):
        super().__init__(style=discord.ButtonStyle.grey, label='\u200b', row=y)
        self.x = x
        self.y = y
        self.num = num
        self.gameover = False

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: NumberGameGrid = self.view
        total = view.add_num(self.num)
        index = self.x
        winner = view.check_board_winner(total)

        if random.choice([0, 1]) == 1:
            if self.num < 9:
                if index == 2 and not -10 < self.num < 0:
                    self.num -= 1
                else:
                    self.num += 1
            else:
                self.num -= 1
        else:
            if self.num > -9:
                if index == 0 and not 0 < self.num < 10:
                    self.num += 1
                else:
                    self.num -= 1
            else:
                self.num += 1

        self.style = discord.ButtonStyle.grey
        self.label = '\u200b'
        self.disabled = False
        content = f"**SUM:** {total}"

        if winner:
            self.gameover = True
        if self.gameover:
            content = f"Game Over! You Win!"
            view.disable_all_buttons()

        await interaction.response.edit_message(content=content, view=view)


class NumberGameGrid(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.total = 0
        self.board = [
            [0, 0, 0]
        ]

        for x in range(3):
            for y in range(1):
                if x == 0:
                    # always negative
                    self.add_item(NumberGameButton(x, y, random.randint(1, 9)))
                if x == 1:
                    self.add_item(NumberGameButton(x, y, random.randint(-9, 9)))
                if x == 2:
                    # always positive
                    self.add_item(NumberGameButton(x, y, random.randint(-9, -1)))

        self.add_item(NumberGameQuitButton(3, 0))

    def check_board_winner(self, tot):
        self.total = tot
        if self.total == 100:
            return True
        else:
            return False

    def add_num(self, num):
        self.total += num
        return self.total

    def disable_all_buttons(self):
        for child in self.children:
            child.disabled = True


class NumberGameCommand(commands.Cog):
    @commands.hybrid_command(help='a very scuffed tic tac toe game')
    async def numbergame(self, ctx):
        how_to_play = """
        **__HOW TO PLAY THE NUMBER GAME__**
1.  The aim of the game is to add numbers up to 100
2. There are three buttons, all with hidden values between -10 and 10. The leftmost is always positive, the middle is random, and the rightmost is always negative or 0.
3. Each time you press the button, the value of each button will change by +1 or -1, with a maximum range of 10 to -10.


*Good Luck!*
        """
        await ctx.send(how_to_play, view=NumberGameGrid())


async def setup(bot):
    await bot.add_cog(NumberGameCommand(bot))
