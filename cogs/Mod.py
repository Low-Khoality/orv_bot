import discord
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(cog="Mod",
                      enabled=False)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.member, *, reason="no reason"):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} was kicked by {ctx.author.mention}. [{reason}]')

    @commands.command(cog="Mod",
                      enabled=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.member, *, reason="no reason"):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} was banned by {ctx.author.mention}. [{reason}]')

    @commands.command(aliases=["purge", "prune"],
                      cog="Mod",
                      enabled=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"{amount} messages got deleted")
        await msg.delete(delay=3)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            msg=await ctx.send("You don't have the permission to do that!")
            await msg.delete(delay=3)

        if isinstance(error, commands.MissingRequiredArgument):
            msg=await ctx.send("You need to specify an amount")

            await msg.delete(delay=3)
        if isinstance(error, commands.BadArgument):
            msg=await ctx.send("Give an integer")
            await msg.delete(delay=3)

        print(error)


def setup(bot):
    bot.add_cog(Mod(bot))