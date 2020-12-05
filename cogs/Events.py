import asyncio
import discord
from discord.ext import commands
from orv_bot._orv_bot import db

class Events (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('\n------')
        print('Logged in as')
        print(self.bot.user.name)
        print('------\n')
        print('Bot is now working!')
        await self.bot.change_presence(
            activity=discord.Streaming(name="the scenarios", url="https://www.twitch.tv/someepicgamer22"))


    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        if self.bot.user.mentioned_in(message):
            try:
                with db.cursor() as cursor:
                    sql = "SELECT `prefix` FROM `prefixes` WHERE `guild_id`=%s"
                    cursor.execute(sql, (message.guild.id,))
                    prefix = cursor.fetchone()
                    current_prefix = prefix['prefix']
                    await message.channel.send(f"This server's prefix is `{current_prefix}` type `{current_prefix}prefix <new prefix here>` to change it")
            except Exception as e:
                print(f'Error looking up prefix 3: {e}')

    @commands.command(command_prefix=commands.when_mentioned)
    async def on_mention(self, ctx):
        print("mentioned")



def setup(bot):
    bot.add_cog(Events(bot))