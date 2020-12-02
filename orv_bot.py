import discord
import asyncio
from discord.ext import commands
from settings import TOKEN, DB_HOST, DB_PASS, DB_USER
import os
import mysql.connector
import json

mydb = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
)


def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("o", "O")(bot, message)

    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or("o", "O")(bot, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix, prefix.lower(), prefix.upper(), "o", "O")(bot, message)


bot = commands.Bot(command_prefix=get_prefix, help_command=None, case_insensitive=True)
# command for testing embeds
@bot.command(hidden=True,
             aliases=["embedt"])
async def testembed(ctx):
    embed = discord.Embed(title="Title", description="Description", color=discord.Color.red())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_image(url="https://s3.amazonaws.com/images.seroundtable.com/google-css-images-1515761601.jpg")
    embed.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/p01ezbiuDHgRFQ-htBCd7QxaYxo=/0x105:2012x1237/1600x900/cdn.vox-cdn.com/uploads/chorus_image/image/47070706/google2.0.0.jpg")

    embed.add_field(name="Field 1",value="value 1", inline=True)
    embed.add_field(name="Field 2", value="value 2", inline=True)

    embed.add_field(name="Field 3", value="value 3", inline=False)
    embed.add_field(name="Field 4", value="value 4", inline=False)

    await ctx.send(embed=embed)

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
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f'{cog} cannot be loaded:')
            raise e


# loops the list_servers function
bot.loop.create_task(list_servers())


bot.run(TOKEN)