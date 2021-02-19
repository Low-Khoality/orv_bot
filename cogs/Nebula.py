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
                    print(f"Nebula does not exist: {nebula} 1")
                else:
                    return result
        except Exception as e:
            print(f"Error looking up nebula {nebula}\n{e}")

    def sort_members(self, nebula):
        try:
            with db.cursor() as cursor:
                sql = "SELECT member_ids, nebula_rank, contribution, nebula_ranking FROM `nebula_members` WHERE `nebula`=%s"
                cursor.execute(sql, (nebula,))
                data = cursor.fetchone()

                db.commit()
        except Exception as e:
            print(f"Error sorting nebula {nebula}\n{e}")
        data = list(data.values())
        members, ranks, contribution, ranking = data[0].split(", "), data[1].split(", "), data[2].split(", "), data[3].split(", ")
        sorted_members, sorted_contribution, sorted_ranks, sorted_rankings = "", "", "", ""
        for i in range(len(members)):
            idx = i
            for j in range(i + 1, len(members)):
                if int(contribution[idx]) < int(contribution[j]):
                    idx = j
            members[i], members[idx], contribution[i], contribution[idx] = members[idx], members[i], contribution[idx], contribution[i]
            ranks[i], ranks[idx], ranking[i], ranking[idx] = ranks[idx], ranks[i], ranking[idx], ranking[i]

            sorted_members += f"{members[i]}"
            sorted_contribution += f"{contribution[i]}"
            sorted_ranks += f"{ranks[i]}"
            sorted_rankings += f"{i + 1}"

            if i != len(members)-1:
                sorted_members += ", "
                sorted_contribution += ", "
                sorted_ranks += ", "
                sorted_rankings += ", "

        try:
            with db.cursor() as cursor:
                sql = f"UPDATE nebula_members SET member_ids=%s, nebula_rank=%s, nebula_ranking=%s, contribution=%s WHERE nebula=%s"
                cursor.execute(sql, (sorted_members, sorted_ranks, sorted_rankings, sorted_contribution, nebula))

                db.commit()
        except Exception as e:
            print(f"Error sorting nebula members\n{e}")

    def get_members(self, member):
        nebula = self.get.get_nebula(member.id)
        self.sort_members(nebula)
        try:
            with db.cursor() as cursor:
                sql = "SELECT member_ids, nebula_rank, contribution, nebula_ranking FROM `nebula_members` WHERE `nebula`=%s"
                cursor.execute(sql, (nebula,))
                result = cursor.fetchone()
                if not result:
                    print(f"Nebula does not exist: {nebula} 2")
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

    async def get_member_list(self, ctx, member, page):
        data = list(self.get_members(member).values())
        members, ranks, contribution, ranking = data[0].split(", "), data[1].split(", "), data[2].split(", "), data[3].split(", ")
        nebula = self.get.get_nebula(member.id)
        output = f"All of the members of the nebula **{nebula}** are listed below.\n"

        index = (len(members) - (page * 10))
        for i in range((page - 1) * 10, (page * 10) + index if index < 0 else page * 10):
            idx = i
            for j in range(i + 1, len(members)):
                if int(ranks[idx]) < int(ranks[j]):
                    idx = j
                if int(ranks[idx]) == int(ranks[j]):
                    if int(contribution[idx]) < int(contribution[j]):
                        idx = j
            members[i], members[idx], contribution[i], contribution[idx] = members[idx], members[i], contribution[idx], contribution[i]
            ranks[i], ranks[idx], ranking[i], ranking[idx] = ranks[idx], ranks[i], ranking[idx], ranking[i]
            rank = "Founder" if int(ranks[i]) == 3 else "Co-Founder" if int(ranks[i]) == 2 else "Member" if int(ranks[i]) == 1 else ""
            member = await self.get.get_member(ctx, members[i])
            level = self.get.get_level(member.id).split(",")[0]
            output += f"\n**#{ranking[i]}** | {member.mention} | **Nebula Ranking**: {rank} | **Level**: {level}\n**Contribution**: {contribution[i]}"
            if i != len(members):
                output += "\n"

        embed = discord.Embed(title=f"Members of **{nebula} 🌌**", description=output, color=discord.Color.from_rgb(130, 234, 255))
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        return embed

    @commands.group(name="nebula",
                    aliases=["neb"],
                    enabled=True,
                    brief="Views the info of a nebula",
                    usage=["[Example] onebula -> Shows you the basic info of your nebula.", "[Example] onebula @user - > Shows you the basic information of @user's nebula"],
                    invoke_without_command=True)
    async def nebula(self, ctx, inp=None):
        member = ctx.author if not inp else await self.get.get_member(ctx, inp)
        if member is None:
            return await self.error.get_error(ctx, f"User {inp} not found", "nebula members")
        if self.get.get_user(member.id):
                nebula = self.get.get_nebula(member.id)
                if nebula is None:
                    if member == ctx.author:
                        return await self.error.get_error(ctx, f"{self.get.get_user_type(member.id)} **{member.name}**, you are not in a nebula!", "nebula")
                    else:
                        return await self.error.get_error(ctx, f"The {self.get.get_user_type(member.id)} **{member.name}** is not in a nebula!", "nebula")
                else:
                    embed = discord.Embed(title=f"**{nebula} 🌌**", color=discord.Color.from_rgb(130, 234, 255))
                    # embed.set_author(name=member.name, icon_url=member.avatar_url)
                    # embed.add_field(name=f'Nebula Message', value=". . .")
                    # embed.add_field(name="\u200b", value=f"**Nebula Founder:** \n**Nebula Co-Founder:** \n**Nebula Supervisor:** \n**Nebula Members:**", inline=False)
                    # embed.add_field(name=f'Nebula Blessings <:Up_Arrow:792403744134004736>', value="\u200b")

                    await ctx.send(embed=embed)
        else:
            if member is ctx.author:
                await self.error.not_registered_error(ctx, "nebula")
            else:
                await self.error.get_error(ctx, f"The user **{member.name}** is not registered to this bot!", "nebula")

    @nebula.command(brief="Create your own nebula")
    async def create(self, ctx, *, nebula: str = None):
        if self.get.get_user(ctx.author.id) is None:
            return await self.error.not_registered_error(ctx, "nebula")

        in_nebula = self.get.get_nebula(ctx.author.id)
        if in_nebula is not None:
            return await self.error.get_error(ctx, f"{self.get.get_user_type(ctx.author.id)} **{ctx.author.name}**, you are already in a nebula!", "nebula create")

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
            return await self.error.get_error(ctx,f"The nebula \"{nebula}\" is already taken", "nebula create")

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
            if str(reaction.emoji) == "✅":

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

                        sql = "INSERT INTO `nebula_members` (nebula, member_ids, nebula_rank, contribution) VALUES (%s, %s, %s, %s)"
                        cursor.execute(sql, (nebula, ctx.author.id, 3, 0))

                        sql = f"UPDATE players SET nebula=%s, coins=%s WHERE user_id=%s"
                        cursor.execute(sql, (nebula, self.get.get_coins(ctx.author.id)-250000, ctx.author.id))

                        db.commit()

                        embed = discord.Embed(title="Congratulations 🎉",
                                              description=f"{self.get.get_user_type(ctx.author.id)} {ctx.author.mention}, you are responsible for the birth of a nebula. You may now challenge the scenarios with other incarnations and constellations as a nebula.",
                                              color=discord.Color.from_rgb(130, 234, 255))
                        embed.add_field(name="\u200b",
                                        value=f"*do `{self.get.get_prefix(ctx)}help nebula` for information on commands regarding nebulas*",
                                        inline=False)
                        await msg.delete(delay=0)
                        await ctx.send(embed=embed)
                except Exception as e:
                    print(f"Error adding Nebula: {e}")
            elif str(reaction.emoji) == "❌":
                await msg.delete(delay=0)

    @nebula.command()
    async def test(self, ctx):
        members = list(self.get_members(ctx.author).values())
        contribution, ranking = members[2].split(", "), members[3].split(", ")
        await ctx.send(f"{contribution}\n{ranking}")

    @nebula.command(name="members",
                    aliases=["mems", "ranks"],
                    enabled=True,
                    brief="Views the member list of a nebula",
                    usage=["[Example] onebula members-> Shows you the members of your own nebula.", "[Example] onebula members @user -> shows you the members of @user's nebula"],
                    description="[WIP]")
    async def members(self, ctx, inp=None):
        member = ctx.author if not inp else await self.get.get_member(ctx, inp)
        if member is None:
            return await self.error.get_error(ctx, f"User {inp} not found", "nebula members")

        if self.get.get_user(member.id) is None:
            if member is ctx.author:
                return await self.error.not_registered_error(ctx, "nebula members")
            else:
                return await self.error.get_error(ctx, f"The user **{member.name}** is not registered to this bot!", "nebula members")

        page = 1
        embed = await self.get_member_list(ctx, member, page)

        msg = await ctx.send(embed=embed)
        data = list(self.get_members(member).values())
        total_members = len(data[0].split(", "))
        if total_members <= 10:
            return

        await msg.add_reaction("⬅️")
        await asyncio.sleep(.35)
        await msg.add_reaction("➡️")
        await asyncio.sleep(.35)
        await msg.add_reaction("🗑️")
        done = False

        total_pages = total_members//10 if total_members % 10 == 0 else total_members//10+1

        while not done:
            def check(reaction, user):
                return ctx.author == user and str(reaction.emoji) in ["⬅️", "➡️", "🗑️"]

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                done = True
            else:
                if str(reaction.emoji) == "🗑️":
                    return await msg.delete(delay=0)
                if str(reaction.emoji) == "⬅️":
                    if page == 1:
                        page = total_pages
                    else:
                        page -= 1
                if str(reaction.emoji) == "➡️":
                    if page == total_pages:
                        page = 1
                    else:
                        page += 1
            await msg.edit(embed=await self.get_member_list(ctx, member, page))


def setup(bot):
    bot.add_cog(Nebulas(bot))