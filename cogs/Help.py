import discord
from discord.ext import commands

async def has_permissions(ctx):
    return ctx.message.author.guild_permissions.administrator

def is_khoa(ctx):
    return ctx.author.id == 122837007834677251

def is_admin(ctx):
    return ctx.author.id in [423674541886406656, 122837007834677251, 526152115140427782]

class Help (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.get = self.bot.get_cog("Get")
        self.error = self.bot.get_cog("Error")

    async def get_help(self, ctx, command: str):
        cmd = self.bot.get_command(command)

        if cmd is None:
            return await self.error.get_error(ctx, f'No command called "{command}" found', "help")

        if cmd.hidden==True and not is_admin(ctx):
            return await self.error.get_error(ctx, f'No command called "{command}" found', "help")

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

        embed = discord.Embed(title=title, description=f"{brief}{usage}", color=discord.Color.from_rgb(130, 234, 255))
        embed.set_footer(text=f"Use {self.get.get_prefix(ctx)}help <command or command group name> for more info on a command")
        try:
            for command in cmd.commands:
                brief = ". . ."
                if command.brief:
                    brief = command.brief
                embed.add_field(name=f"{command} {command.description}", value=brief, inline=False)
        except:
            pass
        await ctx.send(embed=embed)

    @commands.command(brief="Shows this message")
    async def help(self, ctx, *, cmd: str=None):
        if cmd is None:
            owner = await has_permissions(ctx=ctx)
            # as long as nothing is passes through args this block should run
            cogs = []
            cog_names = []
            commands = []
            command_names = []

            cog_list = ["Profile",
                        "Settings",
                        "Misc",
                        "Nebulas",
                        "Admin"]

            for cog in cog_list:
                cog_names.append(cog)
                cogs.append(self.bot.get_cog(cog))
                commands.append(self.bot.get_cog(cog).get_commands())

            for i in range(len(commands)):
                temp = ""
                for c in commands[i]:
                    if c.hidden==False or is_admin(ctx):
                        temp += f"{c.name} | "
                command_names.append(temp)

            embed1 = discord.Embed(title="Bot commands", color=discord.Color.from_rgb(130, 234, 255))

            # if owner is true then show the Settings cog (i == 2) else dont show it
            for i in range(len(cogs)):
                if owner and i == 1:
                    embed1.add_field(name=cog_names[i], value=(command_names[i])[:-2], inline=True)
                if is_admin(ctx) and i == 4:
                    embed1.add_field(name=cog_names[i], value=(command_names[i])[:-2], inline=True)
                elif i != 1:
                    embed1.add_field(name=cog_names[i], value=(command_names[i])[:-2], inline=True)
            await ctx.send(embed=embed1)

        elif cmd:
            await self.get_help(ctx, cmd)

def setup(bot):
    bot.add_cog(Help(bot))