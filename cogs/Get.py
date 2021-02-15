from discord.ext import commands
from orv_bot._orv_bot import db
class Get (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_general_skills(self, user_id):
        try:
            with db.cursor() as cursor:
                sql = "SELECT stamina, strength, agility, magic FROM `general_skills` WHERE `user_id`=%s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                general_skills = list(result.values())
                if not result:
                    print(f"User does not exist: {user_id}")
                else:
                    return general_skills
        except Exception as e:
            print(f"Error looking up userid {user_id}\n{e}")

    def get_nebula(self, user_id):
        try:
            with db.cursor() as cursor:
                sql = "SELECT nebula FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                nebula = result["nebula"]
                if not result:
                    print(f"User is not in a nebula: {user_id}")
                else:
                    return nebula
        except Exception as e:
            print(f"Error looking up userid {user_id}\n{e}")

    def get_user_type(self, user_id):
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

    def get_user(self, user_id):
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

    def get_skills(self, user_id):
        try:
            with db.cursor() as cursor:
                sql = "SELECT personal_skills, skill_level FROM `personal_skills` WHERE `user_id`=%s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                personal_skills = result["personal_skills"].split(", ")
                skill_level = result["skill_level"].split(", ")
                temp = personal_skills
                personal_skills = ""
                for i in range(0, len(temp)):
                    if i % 2 == 1:
                        personal_skills += f"[{temp[i]} Lv.{skill_level[i]}],\n"
                    else:
                        personal_skills += f"[{temp[i]} Lv.{skill_level[i]}], "
                return personal_skills
        except Exception as e:
            print(f"Error looking up attributes of: {user_id}\n{e}")

    def get_attributes(self, user_id):
        try:
            with db.cursor() as cursor:
                sql = "SELECT attribute, attribute_rating FROM `personal_attributes` WHERE `user_id`=%s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                attribute = result["attribute"].split(", ")
                attribute_rating = result["attribute_rating"].split(", ")
                temp = attribute
                attribute = ""
                for i in range(0, len(temp)):
                    if i % 2 == 1:
                        attribute += f'{temp[i]} ({attribute_rating[i]}),\n'
                    else:
                        attribute += f'{temp[i]} ({attribute_rating[i]}), '
                return attribute
        except Exception as e:
            print(f"Error looking up attributes of: {user_id}\n{e}")

    def get_level(self, user_id):
        try:
            with db.cursor() as cursor:
                sql = "SELECT level, exp_points FROM `general_skills` WHERE `user_id`=%s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()

                level = f'{result["level"]}, [{result["exp_points"]}/2680 EXP]'
                return level
        except Exception as e:
            print(f"Error looking up coins of: {user_id}\n{e}")

    def get_coins(self, user_id):
        try:
            with db.cursor() as cursor:
                sql = "SELECT coins FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                coins = result["coins"]
                return coins
        except Exception as e:
            print(f"Error looking up coins of: {user_id}\n{e}")

    def get_evaluation(self, user_id):
        try:
            with db.cursor() as cursor:
                sql = "SELECT overall_evaluation FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                evaluation = result["overall_evaluation"]
                return evaluation
        except Exception as e:
            print(f"Error looking up coins of: {user_id}\n{e}")

    def get_prefix(self, ctx):
        try:
            with db.cursor() as cursor:
                sql = "SELECT `prefix` FROM `prefixes` WHERE `guild_id`=%s"
                cursor.execute(sql, (ctx.guild.id,))
                prefix = cursor.fetchone()
                current_prefix = prefix['prefix']
                return current_prefix
        except Exception as e:
            print(f'Error looking up prefix 2: {e}')

    async def get_member(self, ctx, inp):
        try:
            members = await ctx.guild.fetch_members(limit=None).flatten()
            for i in range(len(members)):

                # Find the minimum element in remaining
                # unsorted array
                min_idx = i
                for j in range(i + 1, len(members)):
                    if members[min_idx].name.lower() > members[j].name.lower():
                        min_idx = j

                        # Swap the found minimum element with
                # the first element
                members[i], members[min_idx] = members[min_idx], members[i]
            member = [i for i in members if i.display_name.lower().startswith(inp.lower())][0]
            return member
        except Exception as e:
            return

def setup(bot):
    bot.add_cog(Get(bot))