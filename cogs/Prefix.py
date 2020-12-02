import discord
from discord.ext import commands
import json

def is_guild_owner(ctx):
    return ctx.author.id == ctx.guild.owner_id


class Prefix (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, *, pre: str=None):
        with open("prefixes.json", 'r') as f:
            prefixes = json.load(f)
        if pre is None:
            if str(ctx.guild.id) not in prefixes:
                prefix = "o"
            else:
                prefix = prefixes[str(ctx.guild.id)]
            await ctx.channel.send(f"This server's prefix is `{prefix}` type `{prefix}prefix <new prefix here>` if you wish to change it")
        elif is_guild_owner(ctx) and pre:
            prefixes[str(ctx.guild.id)] = pre
            await ctx.send(f"New prefix is {pre}")

            with open("prefixes.json", 'w') as f:
                json.dump(prefixes, f, indent=4)
        elif not is_guild_owner(ctx) and pre:
            msg = await ctx.send("This command is owners only")
            await msg.delete(delay=3)

def setup(bot):
    bot.add_cog(Prefix(bot))