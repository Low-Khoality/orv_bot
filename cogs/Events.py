import discord
from discord.ext import commands
import json


class Events (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        if self.bot.user.mentioned_in(message):
            with open("prefixes.json", 'r') as f:
                prefixes = json.load(f)
            if str(message.guild.id) not in prefixes:
                prefix = "o"
            else:
                prefix = prefixes[str(message.guild.id)]
            await message.channel.send(f"This server's prefix is `{prefix}` type `{prefix}prefix <new prefix here>` if you wish to change it")

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print('------')
        print('Bot is now working!')
        await self.bot.change_presence(activity=discord.Streaming(name="the scenarios", url="https://www.twitch.tv/someepicgamer22"))

    @commands.command(command_prefix=commands.when_mentioned)
    async def on_mention(self, ctx):
        print("mentioned")


    @commands.Cog.listener()
    async def on_command_error(self, ctx , error):
        # if isinstance(error, commands.CheckFailure):
        #     msg = await ctx.send("You don't have the permission to do that!")
        #     await msg.delete(delay=3)

        print(error)


        # if isinstance(error, commands.CommandNotFound):
        #     msg = await ctx.send("This is not a command")
        #     await msg.delete(delay=3)

def setup(bot):
    bot.add_cog(Events(bot))