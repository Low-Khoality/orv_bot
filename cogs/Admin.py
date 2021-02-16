import discord
from discord.ext import commands
from orv_bot._orv_bot import db
from pprint import pprint

def is_khoa(ctx):
    return ctx.author.id == 122837007834677251

def is_admin(ctx):
    return ctx.author.id in [423674541886406656, 122837007834677251, 526152115140427782]

class Admin (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error = self.bot.get_cog("Error")
        self.get = self.bot.get_cog("Get")

    @commands.command(name="remneb",
                      brief="remove a nebula from the database [ADMIN]",
                      aliases=["remn"],
                      usage=["[Example] `oremn \"Milky Wars\"` -> removes [Milky Wars]"],
                      hidden=True)
    @commands.check(is_admin)
    async def remove_nebula_from_db(self, ctx, nebula):
        try:
            with db.cursor() as cursor:
                sql = f"DELETE nebulas, nebula_members FROM (nebulas INNER JOIN nebula_members ON nebulas.nebula = nebula_members.nebula) WHERE nebulas.nebula = %s"
                cursor.execute(sql, (nebula))

                sql = f"UPDATE players SET nebula=Null WHERE user_id=%s"
                cursor.execute(sql, (ctx.author.id))

                db.commit()
                embed = discord.Embed(title=f"[Successfully removed nebula [{nebula}] from the database",
                                      color=discord.Color.from_rgb(130, 234, 255))
                await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error removing nebula [{nebula}] from the database\n{e}")
            return await self.error.get_error(ctx, f"nebula [{nebula}] does not exist!", "remneb")

    @commands.command(name="remu",
                      brief="remove a user from the database [ADMIN]",
                      hidden=True)
    @commands.check(is_admin)
    async def remove_user_from_db(self, ctx, member):
        member = await self.get.get_member(ctx, member)
        if member is None:
            return await self.error.get_error(ctx, f"user {member} not found")
        if member.id == 122837007834677251:
            return await ctx.send("no.")
        try:
            with db.cursor() as cursor:
                sql = f"DELETE players, general_skills, personal_skills, personal_attributes FROM (((players INNER JOIN general_skills ON players.user_id = general_skills.user_id) INNER JOIN personal_attributes ON players.user_id=personal_attributes.user_id) INNER JOIN personal_skills ON players.user_id=personal_skills.user_id) WHERE players.user_id = %s"
                cursor.execute(sql, (member.id))

                db.commit()
                embed = discord.Embed(title=f"[Successfully removed {member.name} [{member.id}] from the database", color=discord.Color.from_rgb(130, 234, 255))
                await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error removing {member.name} [{member.id}] from the database\n{e}")
            return await self.error.get_error(ctx, f"{member.name} is not registered!", "remu")


    @commands.command(name="addcoins",
                      brief="adds coins to a user [ADMIN]",
                      aliases=["ac"],
                      hidden=True)
    @commands.check(is_admin)
    async def give_gold(self, ctx, *args):
        if (len(args)) >= 2:
            member = await self.get.get_member(ctx, args[0])
            amount = int(args[1])
            if member is None:
                return await self.error.get_error(ctx, f"user {args[0]} not found", "addcoins")
        else:
            member = ctx.author
            amount = int(args[0])
        try:
            with db.cursor() as cursor:
                sql = f"UPDATE players SET coins=%s WHERE user_id=%s"
                cursor.execute(sql, (self.get.get_coins(member.id) + amount, member.id))

                db.commit()
                embed = discord.Embed(title=f"[{self.get.get_user_type(member.id)} **{member.name}** you have obtained __{amount}__ coins!]", color=discord.Color.from_rgb(130, 234, 255))
                await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error updating coins ({amount} to {member.id} from {ctx.author.name} [{ctx.author.id}])\n{e}")
            return await self.error.get_error(ctx, f"{member.name} is not registered!", "addcoins")


def setup(bot):
    bot.add_cog(Admin(bot))