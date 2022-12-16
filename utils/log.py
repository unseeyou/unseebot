from discord.ext import commands


def clean(text):
    return ''.join(ch for ch in text if ch.isalnum())


def read_and_cache_logfile():
    lines = []
    with open('log.txt', 'r') as file:
        for line in file.readlines():
            lines.append(line)
        file.close()
    return lines


def write_new_logfile(old_info, new_info):
    # step 1: write in all the old information
    with open('log.txt', 'w') as file:
        for i in old_info:
            file.write(i)
    # step 2: write the new info
        file.write(new_info + '\n')
        file.close()

    # for debug purposes, read the file and print it
    # with open('log.txt', 'r') as file:
    #     print(file.read())
    #     file.close()

    return True


class Cog(commands.Cog):
    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            logline = f'{clean(ctx.guild.name)} > #{clean(ctx.message.channel.name)} > {clean(ctx.author.name)}[{ctx.author.id}]: {clean(ctx.message.content) if ctx.message.content is not None else ""}{r"/"+ctx.interaction.command.name + ", args: " + str(vars(ctx.interaction.namespace)) if ctx.interaction is not None else ""}'
        except Exception as err:
            logline = err
            print(err)
        logfile_cache = read_and_cache_logfile()
        write_new_logfile(old_info=logfile_cache, new_info=logline)


async def setup(bot):
    await bot.add_cog(Cog(bot))
