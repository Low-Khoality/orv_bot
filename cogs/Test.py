import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(hidden=True,
                 aliases=["embedt"])
    async def testembed(self, ctx):
        embed = discord.Embed(title="Title", description="Description", color=discord.Color.red())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_image(url="https://s3.amazonaws.com/images.seroundtable.com/google-css-images-1515761601.jpg")
        embed.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/p01ezbiuDHgRFQ-htBCd7QxaYxo=/0x105:2012x1237/1600x900/cdn.vox-cdn.com/uploads/chorus_image/image/47070706/google2.0.0.jpg")
        embed.add_field(name="Field 1", value="value 1 \u200b", inline=True)
        embed.add_field(name="Field 2", value="value 2", inline=True)

        embed.add_field(name="Field 3", value="value 3", inline=False)
        embed.add_field(name="Field 4", value="value 4", inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Test(bot))