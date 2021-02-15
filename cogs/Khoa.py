import discord
from discord.ext import commands
from orv_bot._orv_bot import db
from pprint import pprint


def is_khoa(ctx):
    return ctx.author.id == 122837007834677251

class Khoa (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error = self.bot.get_cog("Error")
        self.get = self.bot.get_cog("Get")

    @commands.command(name="addcoins",
                      brief="adds coins to a user [ADMIN]",
                      aliases=["ac"],
                      hidden=True)
    @commands.check(is_khoa)
    async def give_gold(self, ctx, *args):
        if (len(args)) >= 2:
            member = await commands.MemberConverter().convert(ctx, args[0])
            amount = int(args[1])
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
            return await self.error.get_error(ctx, f"error adding coins to {member.name}", "addcoins")


def setup(bot):
    bot.add_cog(Khoa(bot))