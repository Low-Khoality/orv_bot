import discord
import asyncio
from discord.ext import commands
from settings import TOKEN

BOT_PREFIX = ("?", "!")
bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    print('Bot is now working!')
    await bot.change_presence(activity=discord.Streaming(name="the scenarios", url="https://www.twitch.tv/someepicgamer22"))

async def list_servers():
    await bot.wait_until_ready()
    while not bot.is_closed():
        print("\nCurrent servers:")
        for server in bot.guilds:
            print(server.name+'\n')
        await asyncio.sleep(600)



bot.loop.create_task(list_servers())
bot.run(TOKEN)