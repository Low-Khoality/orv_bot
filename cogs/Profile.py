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
    async def balance(self, ctx, member=None):
        member = ctx.author if not member else await self.get.get_member(ctx, member)
        if member is None:
            return await self.error.get_error(ctx, f"user {member} not found", "coins")

        coins = self.get.get_coins(member.id)
        if coins is not None:
            embed = discord.Embed(description=f"**Coins possessed:** {format(coins, ',d')}", color=discord.Color.from_rgb(130, 234, 255))
            embed.set_author(name=member.name, icon_url=member.avatar_url)
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
    async def stats(self, ctx, member=None):
        member = ctx.author if not member else await self.get.get_member(ctx, member)
        if member is None:
            return await self.error.get_error(ctx, f"user {member} not found", "stats")
        if self.get.get_user(member.id):
            evaluation = self.get.get_evaluation(member.id)
            if evaluation:
                addition = f"**Overall Evaluation:** \n{evaluation}\n\n"
            else:
                addition = "**Overall Evaluation** \nThe current comprehensive evaluation is \ncurrently in progress.\n\n"
            level = self.get.get_level(member.id)
            block1=f"{addition} **Name:** {member.name}\n**Level:** {level}"

            user_type = self.get.get_user_type(member.id)
            if user_type == "Constellation":
                # TODO add constellation modifiers to database
                block1 += f"\n**Constellation Modifier:** *Architect of revelation*"  # placeholder value
            elif user_type == "Incarnation":
                # TODO code here
                block1 += f"\n**Constellation sponsor:** N/A"  # placeholder value
            nebula = self.get.get_nebula(member.id)
            if nebula:
                block1 += f"\n**Nebula Backing:** {nebula}"


            embed = discord.Embed(title=f"**Character Information**", color=discord.Color.from_rgb(130, 234, 255))
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            # embed.set_image(url=self.bot.user.avatar_url)

            embed.timestamp = datetime.now()

            embed.add_field(name="\u200b", value=f"{block1}\n**Coins:** {self.get.get_coins(member.id)}", inline=True)

            attribute = self.get.get_attributes(member.id)
            personal_skills = self.get.get_skills(member.id)
            embed.add_field(name=f"**Personal Attribute(s):** ", value=f"{attribute[:-2]}", inline=False)
            embed.add_field(name=f'**Personal Skill(s):** ', value=f'{personal_skills[:-2]}', inline=False)

            general_skills = self.get.get_general_skills(member.id)
            embed.add_field(name=f'**Overall Stats:** ', value=f"[Stamina Lv.{general_skills[0]}], [Strength Lv.{general_skills[1]}],\n[Agility Lv.{general_skills[2]}], [Magic Power Lv.{general_skills[3]}]", inline=False)

            await ctx.send(embed=embed)
        else:
            await self.error.not_registered_error(ctx, "stats")

    @commands.command(enabled=True,
                      brief="transfer coins to another incarnation or constellation",
                      usage=["[Example] `ogive Uriel#9158 7942` -> gives 7942 to user \"Uriel\""])
    async def give(self, ctx,  *args):
        giver = ctx.author
        member = await self.get.get_member(ctx, args[0])
        amount = int(args[1])

        if member is None:
            return await self.error.get_error(ctx, f"user {args[0]} not found", "give")

        if amount < 1:
            return await self.error.get_error(ctx, f"you cannot transfer less than 1 coin to someone!", "give")

        if amount > self.get.get_coins(giver.id):
            return await self.error.get_error(ctx, f"you cannot transfer more coins than you own!", "give")

        try:
            with db.cursor() as cursor:
                sql = f"UPDATE players SET coins=%s WHERE user_id=%s"
                cursor.execute(sql, (self.get.get_coins(member.id) + amount, member.id))

                sql = f"UPDATE players SET coins=%s WHERE user_id=%s"
                cursor.execute(sql, (self.get.get_coins(giver.id)-amount, giver.id))

                db.commit()
        except Exception as e:
            print(f"Error transferring {amount} coins to {member.name} [{member.id}] from {giver.name} [{giver.id}])\n{e}")
            return await self.error.get_error(ctx, f"{member.name} is not registered!", "addcoins")






def setup(bot):
    bot.add_cog(Profile(bot))