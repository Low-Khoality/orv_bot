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
        return commands.when_mentioned_or("o", "O")(bot, message)
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
                return commands.when_mentioned_or("o", "O")(bot, message)
            else:
                pre = prefix['prefix']
                return commands.when_mentioned_or(pre, pre.lower(), pre.upper(), f"{pre.lower()} ", f"{pre.upper()} ", "o")(bot, message)
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

def add_user_to_db(member):
    if get_user(member.id):
        return False
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `players` (user_id, first_seen, player_type, nebula, overall_evaluation, coins) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (member.id, member.joined_at, "Incarnation", None, None, 0))

            sql = "INSERT INTO `personal_attributes` (user_id, attribute, attribute_rating) VALUES (%s, %s, %s)"
            cursor.execute(sql, (member.id, "PLACEHOLDER", "Ordinary"))

            sql = "INSERT INTO `personal_skills` (user_id, personal_skills, skill_level) VALUES (%s, %s, %s)"
            cursor.execute(sql, (member.id, "PLACEHOLDER", 1))

            sql = "INSERT INTO `general_skills` (user_id, stamina, strength, agility, magic, level, exp_points) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (member.id, 1, 1, 1, 1, 1, 0))
            db.commit()
        return True
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
bot.load_extension("cogs.Get")
bot.load_extension("cogs.Error")
for cog in os.listdir("./cogs"):
    if cog != "Get.py" and cog != "Error.py":
        if cog.endswith(".py"):
            try:
                cog = f"cogs.{cog.replace('.py', '')}"
                bot.load_extension(cog)
            except Exception as e:
                print(f'{cog} cannot be loaded:')
                raise e

bot.loop.create_task(list_servers())
bot.run(TOKEN)
