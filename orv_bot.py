import discord
import asyncio
from discord.ext import commands
from settings import TOKEN

BOT_PREFIX = ("?", "!")
bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')
    print('Bot is now working!')
    await bot.change_presence(activity=discord.Streaming(name="the scenarios", url="https://www.twitch.tv/someepicgamer22"))

@bot.command()
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

async def list_servers():
    await bot.wait_until_ready()
    while not bot.is_closed():
        print("\nCurrent servers:")
        for server in bot.guilds:
            print(server.name+'\n')
        await asyncio.sleep(600)



bot.loop.create_task(list_servers())
bot.run(TOKEN)