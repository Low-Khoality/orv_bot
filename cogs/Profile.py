import discord
from discord.ext import commands
from orv_bot._orv_bot import db, add_user_to_db
from datetime import datetime

class Profile(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.error = self.bot.get_cog("Error")
        self.get = self.bot.get_cog("Get")

    @commands.command(name="coins",
                      aliases=["balance", "c", "bal"],
                      enabled=True,
                      brief="Shows how many coins you currently have",
                      usage=["[Example] oc"])
    async def balance(self, ctx):
        coins = self.get.get_coins(ctx.author.id)
        if coins is not None:
            embed = discord.Embed(description=f"**Coins possessed:** {format(coins, ',d')}", color=discord.Color.from_rgb(130, 234, 255))
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            # embed = discord.Embed(title=f"[{get_user_type(ctx.author.id)} **{ctx.author.name}** you have obtained __{coins}__ coins!]", color=discord.Color.from_rgb(130, 234, 255))
            await ctx.send(embed=embed)
        else:
            await self.error.not_registered_error(ctx, "coins")

    @commands.command(name="start",
                 enabled=True,
                 brief="Enter the scenarios")
    async def start_playing(self, ctx):
        new_player = add_user_to_db(ctx.author)

        if new_player is False:
            await self.error.get_error(ctx, f"{self.get.get_user_type(ctx.author.id)} **{ctx.author.name}**, you are already registered with this bot!", "start")
        else:
            embed = discord.Embed(title="#BI-7623 Channel is now open",
                                  description=f"Incarnation {ctx.author.mention}, the free service of planetary system 8612 has been terminated. The main scenario starts now.",
                                  color=discord.Color.from_rgb(130, 234, 255))
            embed.add_field(name="\u200b", value="*Note: alting, macroing, exploting bugs, and cross-trading are **bannable** offenses.* \n*If you need an explanation on any of those terms, please join the support server*", inline=False)
            embed.set_footer(text=f"Use <{self.get.get_prefix(ctx)}basics> and <{self.get.get_prefix(ctx)}help> for information on how to begin and the list of commands")
            await ctx.send(embed=embed)

    @commands.command(name="stats",
                      enabled=True,
                      brief="Shows a players' stats",
                      aliases=["profile", "s"],
                      usage=["[Example] `os` -> Shows your stats", "[Example] `os @user` -> Shows another users profile"])
    async def stats(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        if self.get.get_user(ctx.author.id):
            evaluation = self.get.get_evaluation(ctx.author.id)
            if evaluation:
                addition = f"**Overall Evaluation:** \n{evaluation}\n\n"
            else:
                addition = "**Overall Evaluation** \nThe current comprehensive evaluation is \ncurrently in progress.\n\n"
            level = self.get.get_level(ctx.author.id)
            block1=f"{addition} **Name:** {member.name}\n**Level:** {level}"

            user_type = self.get.get_user_type(ctx.author.id)
            if user_type == "Constellation":
                block1 += f"\n**Constellation Modifier:** *Architect of revelation*"  # placeholder value
            elif user_type == "Incarnation":
                block1 += f"\n**Constellation sponsor:** N/A"  # placeholder value
            nebula = self.get.get_nebula(ctx.author.id)
            if nebula:
                block1 += f"\n**Nebula Backing:** {nebula}"


            embed = discord.Embed(title=f"**Character Information**", color=discord.Color.from_rgb(130, 234, 255))
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            # embed.set_image(url=self.bot.user.avatar_url)

            embed.timestamp = datetime.now()

            embed.add_field(name="\u200b", value=f"{block1}\n**Coins:** {self.get.get_coins(ctx.author.id)}", inline=True)

            attribute = self.get.get_attributes(ctx.author.id)
            personal_skills = self.get.get_skills(ctx.author.id)
            embed.add_field(name=f"**Personal Attribute(s):** ", value=f"{attribute[:-2]}", inline=False)
            embed.add_field(name=f'**Personal Skill(s):** ', value=f'{personal_skills[:-2]}', inline=False)

            general_skills = self.get.get_general_skills(ctx.author.id)
            embed.add_field(name=f'**Overall Stats:** ', value=f"[Stamina Lv.{general_skills[0]}], [Strength Lv.{general_skills[1]}],\n[Agility Lv.{general_skills[2]}], [Magic Power Lv.{general_skills[3]}]", inline=False)

            await ctx.send(embed=embed)
        else:
            await self.error.not_registered_error(ctx, "stats")





def setup(bot):
    bot.add_cog(Profile(bot))