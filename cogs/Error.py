import discord
from discord.ext import commands
from orv_bot._orv_bot import get_prefix2

class Error(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx , error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.CheckFailure):
            msg = await ctx.send("You don't have the permission to do that!")
            await msg.delete(delay=3)
        print(error)

    async def get_error(self, ctx, error, cmd):
        embed = discord.Embed(title="Error 🛑", description=error, color=discord.Color.red())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"Use <{get_prefix2(ctx)}help {cmd}> if you need help with this command")
        await ctx.send(embed = embed)

    async def not_registered_error(self, ctx, cmd):
        await self.get_error(ctx, f"You are not registered with this bot. Type `{get_prefix2(ctx)}start` to enter the scenarios!", cmd)

def setup(bot):
    bot.add_cog(Error(bot))