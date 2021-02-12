import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(hidden=False,
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
        embed.set_footer(text="footer")

        await ctx.send(embed=embed)

    @commands.command(hidden=True, Enabled=False)
    async def ctest(self, ctx):

        def check(m):
            boop = m.author.id == 571027211407196161
            guild = m.guild == ctx.guild
            return (boop==True and guild == True)

        msg = await self.bot.wait_for('message', check=check)
        embed = msg.embeds[0]
        while embed.description != "*A wild anime card appears!*":
            msg = await self.bot.wait_for('message', check=check)
            embed = msg.embeds[0]
        junk=embed.footer.text
        junk=junk.split(" ")
        # await ctx.send(embed=embed)
        await ctx.send(junk)
        await ctx.send(junk[2])

def setup(bot):
    bot.add_cog(Test(bot))