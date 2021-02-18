from discord.ext import commands
import time

class Misc (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite",
                      enabled=True,
                      brief="Invite Omniscient Reader's Viewpoint bot to your own server")
    async def invite(self, ctx):
        await ctx.send("Link to invite bot: https://discord.com/api/oauth2/authorize?client_id=782370431600558120&permissions=0&scope=bot\nJoin the official support server if you need help: https://discord.gg/GPAphQWQCr")
        pass

    @commands.command(name="ping",
                      brief="Pong!")
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        message = await ctx.send("🏓 Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 Pong! {int(ping)}ms")


def setup(bot):
    bot.add_cog(Misc(bot))