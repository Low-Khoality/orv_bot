import discord
from discord.ext import commands
from orv_bot.cogs.Settings import get_prefix
import os

async def has_permissions(ctx):
    return ctx.message.author.guild_permissions.administrator


class Help (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_help(self, ctx, command: str):
        cmd = self.bot.get_command(command)
        aliases = ""

        brief = ". . ."
        if cmd.brief:
            brief = cmd.brief

        title = f"Command: {cmd}"
        if cmd.aliases:
            for i in cmd.aliases:
                aliases += f"{i}, "
            title += f' [Other names: {aliases[:-2]}]'

        usage = ""
        if cmd.usage:
            for i in cmd.usage:
                usage += f"\n{i}"


        if cmd is None:
            await ctx.send(f'No command called "{command}" found')
            return
        else:
            embed = discord.Embed(title=title, description=f"{brief}{usage}", color=discord.Color.from_rgb(130, 234, 255))
            embed.set_footer(text=f"Use {get_prefix(ctx)}help <command or command group name> for more info on a command")
            await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, *, cmd: str=None):
        # as long as nothing is passes through args this block should run
        cogs = []
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                try:
                    cog = f"{cog.replace('.py', '')}"
                    if cog not in ["Events", "Help"]:
                        cogs.append([self.bot.get_cog(cog), cog])
                except Exception as e:
                    print(f'{cog} cannot be loaded:')
                    raise e
        print(cogs)
        print(cogs[0][1])

        owner = await has_permissions(ctx=ctx)
        if cmd is None:
            embed = discord.Embed(title="Bot commands", color=discord.Color.from_rgb(130, 234, 255))
            embed.add_field(name="Profile", value="stats profile start", inline=True)
            embed.add_field(name="Testing", value="testembed", inline=True)
            # this block should only run if they have admin
            if owner is True:
                embed.add_field(name="Settings", value="prefix", inline=True)
            embed.add_field(name="Misc", value="invite", inline=True)
            embed.add_field(name="No Category", value="help", inline=True)
            await ctx.send(embed=embed)
        elif cmd:
            await self.get_help(ctx, cmd)



    # @help.error
    # async def help_error(self, ctx, error, *, cmd: str=None):
    #     if isinstance(error, commands.CheckFailure) and cmd is None:
    #         embed = discord.Embed(title="Bot commands", color=discord.Color.from_rgb(236, 64, 64))
    #         embed.add_field(name="Testing", value="testembed", inline=True)
    #         embed.add_field(name="No Category", value="help", inline=True)
    #         print(cmd)
    #         await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))