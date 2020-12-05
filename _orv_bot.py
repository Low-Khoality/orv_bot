import discord
import asyncio
from discord.ext import commands
from settings import TOKEN, DB_HOST, DB_PASS, DB_USER, DB_NAME
import os
import pymysql.cursors
import random
# Connect to the database
def connect_database():
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASS,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


db = connect_database()

def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("o", "O", "o ", "O ")(bot, message)
    try:
        with db.cursor() as cursor:
            sql = "SELECT `prefix` FROM `prefixes` WHERE `guild_id`=%s"
            cursor.execute(sql, (message.guild.id,))
            prefix = cursor.fetchone()
            if not prefix:
                with db.cursor() as cursor:
                    sql = "INSERT INTO `prefixes` (`guild_id`, `prefix`) VALUES (%s, %s)"
                    cursor.execute(sql, (message.guild.id, "o"))
                db.commit()
                return commands.when_mentioned_or("o", "O", "o ", "O ")(bot, message)
            else:
                pre = prefix['prefix']
                return commands.when_mentioned_or(pre, pre.lower(), pre.upper(), f"{pre.lower()} ", f"{pre.upper()} ", "o", "O", "o ", "O ")(bot, message)
    except Exception as e:
        print(f'Error looking up prefix 1: {e}')


bot = commands.Bot(command_prefix=get_prefix, help_command=None, case_insensitive=True)


def get_user(user_id):
    try:
        with db.cursor() as cursor:
            sql = "SELECT `user_id` FROM `players` WHERE `user_id`=%s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            if not result:
                print(f"User does not exist: {user_id}")
            else:
                return result
    except Exception as e:
        print(f"Error looking up userid {user_id}\n{e}")


def get_user_type(user_id):
    try:
        with db.cursor() as cursor:
            sql = "SELECT player_type FROM `players` WHERE `user_id`=%s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            user_type = result["player_type"]
            if not result:
                print(f"User does not exist: {user_id}")
            else:
                return user_type
    except Exception as e:
        print(f"Error looking up userid {user_id}\n{e}")


def add_user_to_db(member):
    if get_user(member.id):
        user_type = get_user_type(member.id)
        embed = discord.Embed(title="Error", description=f"{user_type} **{member.name}**, you are already registered with the bot!", color=discord.Color.red())
        embed.set_footer(text="if you need help, please type ohelp")
        return embed
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `players` (user_id, first_seen, player_type, nebula, overall_evaluation) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (member.id, member.joined_at, "Incarnation", None, None))
            
        db.commit()
    except Exception as e:
        print(f"Error adding user: {e}")


# lists the servers
async def list_servers():
    await bot.wait_until_ready()
    print("\nCurrent servers:\n")
    while not bot.is_closed():
        for server in bot.guilds:
            print(server.name)
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

bot.loop.create_task(list_servers())
bot.run(TOKEN)
