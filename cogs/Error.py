import discord
from discord.ext import commands

class Error(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.get = self.bot.get_cog("Get")

    @commands.Cog.listener()
    async def on_command_error(self, ctx , error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.CheckFailure):
            msg = await ctx.send("You don't have the permission to do that!")
            await msg.delete(delay=3)
        print(error)

    async def get_error(self, ctx, error, cmd):
        embed = discord.Embed(title="Error 🛑", description=f"{error}", color=discord.Color.red())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"Use <{self.get.get_prefix(ctx)}help {cmd}> if you need help with this command")
        await ctx.send(embed = embed)

    async def not_registered_error(self, ctx, cmd):
        await self.get_error(ctx, f"You are not registered with this bot. Type <{self.get.get_prefix(ctx)}start> to enter the scenarios!", cmd)

def setup(bot):
    bot.add_cog(Error(bot))