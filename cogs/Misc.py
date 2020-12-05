import asyncio
import discord
from discord.ext import commands

class Misc (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite",
                      enabled=True,
                      brief="Invite Omniscient Reader's Viewpoint bot to your own server")
    async def invite(self, ctx):
        await ctx.send("Link to invite bot: https://discord.com/api/oauth2/authorize?client_id=782370431600558120&permissions=0&scope=bot\nJoin the official support server if you need help: ")
        pass

def setup(bot):
    bot.add_cog(Misc(bot))