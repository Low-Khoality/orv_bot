import discord
from discord.ext import commands
from orv_bot._orv_bot import db, add_user_to_db


class Nebulas (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error = self.bot.get_cog("Error")
        self.get = self.bot.get_cog("Get")

    def get_message(self, nebula):
        try:
            with db.cursor() as cursor:
                sql = "SELECT overall_evaluation FROM `nebula` WHERE `nebula`=%s"
                cursor.execute(sql, (nebula,))
                result = cursor.fetchone()
                evaluation = result["overall_evaluation"]
                return evaluation
        except Exception as e:
            print(f"Error looking up message of: {nebula}\n{e}")


    @commands.group(name="nebula",
                    aliases=["neb"],
                    enabled=False,
                    brief="Views the info of your nebula",
                    usage=["[Example] onebula -> Shows you the basic info of your nebula."])
    async def nebula(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title=f"**{self.get.get_nebula(ctx.author.id)} 🌌**", color=discord.Color.from_rgb(130, 234, 255))
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name=f'Nebula Message', value=". . .")
            embed.add_field(name="\u200b", value=f"**Nebula Founder:** \n**Nebula Co-Founder:** \n**Nebula Supervisor:** \n**Nebula Members:**", inline=False)
            embed.add_field(name=f'Nebula Blessings <:Up_Arrow:792403744134004736>', value="\u200b")


            await ctx.send(embed=embed)

    @nebula.command()
    async def view(self, ctx):
        await ctx.send("second command layer")
        pass


def setup(bot):
    bot.add_cog(Nebulas(bot))