import discord
from discord.ext import commands


async def has_permissions(ctx):
    return ctx.message.author.guild_permissions.administrator



class Help (commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def help(self, ctx, *, cmd: str=None):
        # as long as nothing is passes through args this block should run
        admin = await has_permissions(ctx=ctx)
        if cmd is None:
            embed = discord.Embed(title="Bot commands", color=discord.Color.from_rgb(236, 64, 64))
            embed.add_field(name="Testing", value="testembed", inline=True)
            # this block should only run if they have admin
            if admin is True:
                embed.add_field(name="Settings", value="prefix", inline=True)
            embed.add_field(name="No Category", value="help", inline=True)
            await ctx.send(embed=embed)
        print(cmd)



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