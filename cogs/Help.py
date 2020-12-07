import discord
from discord.ext import commands

async def has_permissions(ctx):
    return ctx.message.author.guild_permissions.administrator


class Help (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.get = self.bot.get_cog("Get")

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
            embed.set_footer(text=f"Use {self.get.get_prefix(ctx)}help <command or command group name> for more info on a command")
            await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, *, cmd: str=None):
        if cmd is None:
            owner = await has_permissions(ctx=ctx)
            # as long as nothing is passes through args this block should run
            cogs = []
            cog_names = []
            commands = []
            command_names = []

            cog_list = ["Profile",
                        "Test",
                        "Settings",
                        "Misc"]

            for cog in cog_list:
                cog_names.append(cog)
                cogs.append(self.bot.get_cog(cog))
                commands.append(self.bot.get_cog(cog).get_commands())

            for i in range(len(commands)):
                temp = ""
                for c in commands[i]:
                    temp += f"{c.name} | "
                command_names.append(temp)

            embed1 = discord.Embed(title="Bot commands", color=discord.Color.from_rgb(130, 234, 255))
            for i in range(len(cogs)):
                if owner is True and i == 2:
                    embed1.add_field(name=cog_names[i], value=(command_names[i])[:-2])
                elif i != 2:
                    embed1.add_field(name=cog_names[i], value=(command_names[i])[:-2])
            await ctx.send(embed=embed1)

        elif cmd:
            await self.get_help(ctx, cmd)

def setup(bot):
    bot.add_cog(Help(bot))