import discord
from discord.ext import commands

class Events (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print('------')
        print('Bot is now working!')
        await self.bot.change_presence(activity=discord.Streaming(name="the scenarios", url="https://www.twitch.tv/someepicgamer22"))


def setup(bot):
    bot.add_cog(Events(bot))