import discord
from discord.ext import commands
from orv_bot._orv_bot import db, add_user_to_db, get_user_type
from datetime import datetime

class Profile(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.error = self.bot.get_cog("Error")

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

    @commands.command(name="coins",
                      aliases=["balance", "c", "bal"],
                      enabled=True,
                      brief="Shows how many coins you currently have",
                      usage=["[Example] oc"])
    async def balance(self, ctx):
        coins = self.get_coins(ctx.author.id)
        if coins:
            embed = discord.Embed(title=f"[{get_user_type(ctx.author.id)} **{ctx.author.name}** you have obtained __{coins}__ coins!]", color=discord.Color.from_rgb(130, 234, 255))
            await ctx.send(embed=embed)
        else:
            await self.error.not_registered_error(ctx, "coins")

    @commands.command(name="start",
                 enabled=True,
                 brief="Enter the scenarios")
    async def start_playing(self, ctx):
        new_player = add_user_to_db(ctx.author)

        if new_player is False:
            await self.error.get_error(ctx, f"{get_user_type(ctx.author.id)} **{ctx.author.name}**, you are already registered with this bot!", "start")
        else:
            embed = discord.Embed(title="#BI-7623 Channel is now open",
                                  description=f"Incarnation {ctx.author.mention}, the free service of planetary system 8612 has been terminated. The main scenario starts now.",
                                  color=discord.Color.from_rgb(130, 234, 255))
            embed.add_field(name="\u200b", value="*Note: alting, macroing, exploting bugs, and cross-trading are **bannable** offenses.* \n*If you need an explanation on any of those terms, please join the support server*", inline=False)
            await ctx.send(embed=embed)

    async def get_user_info(self, user_id):
        try:
            with db.cursor() as cursor:
                sql = "SELECT players.player_type, players.nebula, players.overall_evaluation, " \
                      "personal_attributes.attribute, personal_attributes.attribute_rating, " \
                      "personal_skills.personal_skills, personal_skills.skill_level, " \
                      "general_skills.stamina, general_skills.strength, general_skills.agility, general_skills.magic, general_skills.level, general_skills.exp_points " \
                      "FROM (((players INNER JOIN personal_attributes ON players.user_id=personal_attributes.user_id) " \
                      "INNER JOIN personal_skills ON players.user_id=personal_skills.user_id) " \
                      "INNER JOIN general_skills ON players.user_id=general_skills.user_id) WHERE players.user_id=%s"
                cursor.execute(sql, (user_id))
                result = cursor.fetchone()
                if not result:
                    print(f"User does not exist: {user_id}")
                else:
                    return result
        except Exception as e:
            print(f"Error looking up userid {user_id}\n{e}")

    @commands.command(name="stats",
                      enabled=True,
                      brief="Shows a players' stats",
                      aliases=["profile", "s"],
                      usage=["[Example] `os` -> Shows your stats", "[Example] `os @user` -> Shows another users profile"])
    async def stats(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        user_info = await self.get_user_info(member.id)
        if user_info:
            user_info = list(user_info.values())
            # 0 = player_type, 1 = nebula, 2 = overall_evaluation, 3 = attribute 4 = attribute_rating, 5 = personal_skills,
            # 6 = skill_level, 7 = stamina, 8 = strength, 9 = Agility, 10 = Magic, 11 = level, 12 = exp_points
            attribute = user_info[3].split(", ")
            attribute_rating = user_info[4].split(", ")
            temp = attribute
            attribute = ""
            for i in range(0, len(temp)):
                if i % 2 == 1:
                    attribute += f'{temp[i]} ({attribute_rating[i]}),\n'
                else:
                    attribute += f'{temp[i]} ({attribute_rating[i]}), '
            personal_skills = user_info[5].split(", ")
            skill_level = user_info[6].split(", ")
            temp = personal_skills
            personal_skills = ""
            for i in range(0, len(temp)):
                if i % 2 == 1:
                    personal_skills += f"[{temp[i]} Lv.{skill_level[i]}],\n"
                else:
                    personal_skills += f"[{temp[i]} Lv.{skill_level[i]}], "

            if user_info[2]:
                addition = "**Overall Evaluation:** \n{user_info[2]}\n\n"
            else:
                addition = "**Overall Evaluation** \nThe current comprehensive evaluation is \ncurrently in progress.\n\n"

            block1=f"{addition} **Name:** {member.name}\n**Level:** {user_info[11]}, [{user_info[12]}/2680 EXP]"

            if user_info[0] == "Constellation":
                block1 += f"\n**Constellation Modifier:** *Architect of revelation*"
            elif user_info[0] == "Incarnation":
                block1 += f"\n**Star Backing:** N/A"
            if user_info[1]:
                block1 += f"\n**Nebula Backing:** {user_info[1]}"


            embed = discord.Embed(title=f"**Character Information**", color=discord.Color.from_rgb(130, 234, 255))
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            # embed.set_image(url=self.bot.user.avatar_url)

            embed.timestamp = datetime.now()

            embed.add_field(name="\u200b", value=f"{block1}\n**Coins:** {self.get_coins(ctx.author.id)}", inline=True)

            embed.add_field(name=f"**Personal Attribute(s):** ", value=f"{attribute[:-2]}", inline=False)
            embed.add_field(name=f'**Personal Skill(s):** ', value=f'{personal_skills[:-2]}', inline=False)
            embed.add_field(name=f'**Overall Stats:** ', value=f"[Stamina Lv.{user_info[8]}], [Strength Lv.{user_info[9]}],\n[Agility Lv.{user_info[10]}], [Magic Power Lv.{user_info[11]}]", inline=False)

            await ctx.send(embed=embed)
        else:
            await self.error.not_registered_error(ctx, "stats")





def setup(bot):
    bot.add_cog(Profile(bot))