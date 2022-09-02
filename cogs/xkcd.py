import requests
import random
import discord
from discord.ext import commands
from discord.ui import Button, View


def get_comic(number):
    url = f"https://xkcd.com/{number}/info.0.json"
    req = requests.get(url)
    json = req.json()
    return json


def create_embed(t, i, u, d):
    embed = discord.Embed(title=t, colour=discord.Colour.yellow(), url=u)
    embed.set_image(url=i)
    embed.set_footer(text=d)
    embed.set_author(name='made by unseeyou - powered by xkcd.com', url='https://xkcd.com')
    return embed


class XKCD(commands.Cog):
    @commands.hybrid_command(aliases=["comic"], help='gets a comic from xkcd')
    async def xkcd(self, ctx, number: str = None):
        try:
            if number is None:
                request = requests.get("https://xkcd.com/info.0.json")
                data = request.json()
                num = data["num"]
                number = random.randint(1, num)
            else:
                number = number

            data = get_comic(number)
            title = data["title"]
            img = data["img"]
            url = f"https://xkcd.com/{number}"
            desc = data["alt"]
            e = create_embed(title, img, url, desc)

            view = View()
            nextb = Button(label="New XKCD", style=discord.ButtonStyle.green)
            end = Button(label="End Interaction", style=discord.ButtonStyle.danger)
            view.add_item(nextb)
            view.add_item(end)

            async def nextc(interaction):
                view2 = View()
                view2.add_item(nextb)
                view2.add_item(end)
                n = random.randint(1, num)
                d = get_comic(n)
                em = create_embed(d["title"], d["img"], f"https://xkcd.com/{n}", d["alt"])
                await interaction.response.edit_message(embed=em, view=view2)

            async def endc(interaction):
                view3 = View()
                await interaction.response.edit_message(view=view3)

            nextb.callback = nextc
            end.callback = endc

            await ctx.send(embed=e, view=view)

        except Exception as err:
            await ctx.send(f"`Error: {err}`")
            print(err)


async def setup(bot):
    await bot.add_cog(XKCD(bot))
