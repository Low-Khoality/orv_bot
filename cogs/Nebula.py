import asyncio

import discord
from discord.ext import commands
from orv_bot._orv_bot import db, add_user_to_db


class Nebulas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error = self.bot.get_cog("Error")
        self.get = self.bot.get_cog("Get")

    def get_nebula(self, nebula):
        try:
            with db.cursor() as cursor:
                sql = "SELECT `nebula` FROM `nebulas` WHERE `nebula`=%s"
                cursor.execute(sql, (nebula,))
                result = cursor.fetchone()
                if not result:
                    print(f"Nebula does not exist: {nebula}")
                else:
                    return result
        except Exception as e:
            print(f"Error looking up nebula {nebula}\n{e}")

    def new_nebula(self, nebula):
        if self.get_nebula(nebula):
            return False
        else:
            return True

    def get_message(self, nebula):
        try:
            with db.cursor() as cursor:
                sql = "SELECT message FROM `nebulas` WHERE `nebula`=%s"
                cursor.execute(sql, (nebula,))
                result = cursor.fetchone()
                message = result["message"]
                return message
        except Exception as e:
            print(f"Error looking up message of: {nebula}\n{e}")

    @commands.group(name="nebula",
                    aliases=["neb"],
                    enabled=True,
                    brief="Views the info of your nebula",
                    usage=["[Example] onebula -> Shows you the basic info of your nebula."])
    async def nebula(self, ctx):
        if self.get.get_user(ctx.author.id):
            if ctx.invoked_subcommand is None:

                nebula = self.get.get_nebula(ctx.author.id)
                if nebula is None:
                    await self.error.get_error(ctx,
                                               f"{self.get.get_user_type(ctx.author.id)} **{ctx.author.name}**, You are not in a nebula",
                                               "nebula")

                else:
                    embed = discord.Embed(title=f"**{nebula} 🌌**", color=discord.Color.from_rgb(130, 234, 255))
                    # embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    # embed.add_field(name=f'Nebula Message', value=". . .")
                    # embed.add_field(name="\u200b", value=f"**Nebula Founder:** \n**Nebula Co-Founder:** \n**Nebula Supervisor:** \n**Nebula Members:**", inline=False)
                    # embed.add_field(name=f'Nebula Blessings <:Up_Arrow:792403744134004736>', value="\u200b")

                    await ctx.send(embed=embed)
        else:
            await self.error.not_registered_error(ctx, "nebula")

    @nebula.command(brief="Create your own nebula")
    async def create(self, ctx, *, nebula: str = None):
        if self.get.get_user(ctx.author.id) is None:
            return

        in_nebula = self.get.get_nebula(ctx.author.id)
        if in_nebula is not None:
            return await self.error.get_error(ctx, f"{self.get.get_user_type(ctx.author.id)} **{ctx.author.name}**, You are already in a nebula!", "nebula create")

        if nebula is None:
            return await self.error.get_error(ctx, "You must enter a name for your nebula", "nebula create")

        ' '.join(nebula.split())
        new_nebula = self.new_nebula(nebula)
        try:
            with db.cursor() as cursor:
                sql = "SELECT `guild_id` FROM `nebulas` WHERE `guild_id`=%s"
                cursor.execute(sql, (ctx.guild.id,))
                result = cursor.fetchone()
                if not result:
                    guild_has_nebula = False
                else:
                    guild_has_nebula = True
        except Exception as e:
            print(f"Error looking up nebula's in guild {ctx.guild.name}\n{e}")

        if guild_has_nebula:
            return await self.error.get_error(ctx, "This guild already has a nebula", "nebula create")

        if new_nebula is False:
            return await self.error.get_error(ctx,f"the nebula \"{nebula}\" is already taken", "nebula create")

        embed = discord.Embed(title="Confirmation",
                              description=f"{self.get.get_user_type(ctx.author.id)}, are you sure you want to create the **{nebula}** nebula for __250,000__ coins?",
                              color=discord.Color.from_rgb(130, 234, 255))
        msg = await ctx.send(embed=embed)

        await msg.add_reaction("✅")

        await asyncio.sleep(.35)

        await msg.add_reaction("❌")

        def check(reaction, user):
            return ctx.author == user and str(reaction.emoji) in ["✅", "❌"]

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=5.0, check=check)
        except asyncio.TimeoutError:
            await msg.delete(delay=0)
            msg = await ctx.send(f"{ctx.author.mention}, you waited too long")
            await msg.delete(delay=3)
        else:
            if str(reaction.emoji)== "✅":

                coin = self.get.get_coins(ctx.author.id)
                if coin < 250000:
                    await msg.delete(delay=0)
                    return await self.error.get_error(ctx,
                                                      f"{self.get.get_user_type(ctx.author.id)}, you do not have enough coins to fund a nebula! You currently have __{format(coin, ',d')}__ coins. Nebulas require __250,000__ coins to fund",
                                                      "nebula create")

                try:
                    with db.cursor() as cursor:
                        sql = "INSERT INTO `nebulas` (nebula, guild_id, message, leader, vice_leader) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(sql, (nebula, ctx.guild.id, None, ctx.author.id, None,))

                        sql = "INSERT INTO `nebula_members` (nebula, member_ids, nebula_rank, total_members) VALUES (%s, %s, %s, %s)"
                        cursor.execute(sql, (nebula, ctx.author.id, "leader", 1))

                        sql = f"UPDATE players SET nebula=%s, coins=%s WHERE user_id=%s"
                        cursor.execute(sql, (nebula, self.get.get_coins(ctx.author.id)-250000, ctx.author.id))

                        db.commit()

                        embed = discord.Embed(title="Congratulations 🎉",
                                              description=f"{self.get.get_user_type(ctx.author.id)} {ctx.author.mention}, you are responsible for the birth of a nebula. You may now challenge the scenarios with other incarnations and constellations as a nebula.",
                                              color=discord.Color.from_rgb(130, 234, 255))
                        embed.add_field(name="\u200b",
                                        value=f"*do `{self.get.get_prefix(ctx)}help nebula` for information on commands regarding nebulas*",
                                        inline=False)
                        await ctx.send(embed=embed)
                except Exception as e:
                    print(f"Error adding Nebula: {e}")
            elif str(reaction.emoji)=="❌":
                await msg.delete(delay=0)

    @nebula.command()
    async def view(self, ctx):
        if self.get.get_user(ctx.author.id) is None:
            return
        await ctx.send("second command layer")
        pass


def setup(bot):
    bot.add_cog(Nebulas(bot))
