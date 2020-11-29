import discord
from discord.ext import commands

class Help:
    def __init__(self,bot):
        self.bot=bot,bot

    @commands.command(name="help")
    async def help_(self, ctx):
        embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)

def setup(bot):
    bot.add_cog(Help(bot))