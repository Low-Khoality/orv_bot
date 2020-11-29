import discord
import asyncio
from discord.ext import commands
from settings import TOKEN
import os


BOT_PREFIX = ("?", "!")
bot = commands.Bot(command_prefix=BOT_PREFIX)


# lists the servers
async def list_servers():
    await bot.wait_until_ready()
    while not bot.is_closed():
        print("\nCurrent servers:")
        for server in bot.guilds:
            print(server.name+'\n')
        await asyncio.sleep(600)

# removes the .py from files in the cog folder for loading
for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        try:
            bot.load_extension(f'cogs.{cog[:-3]}')
        except Exception as e:
            print(f'{cog[:-3]} cannot be loaded:')
            raise e


# loops the list_servers function
bot.loop.create_task(list_servers())


bot.run(TOKEN)