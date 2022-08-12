import nextcord
from nextcord.ext import commands


class HelpCom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def help(self, ctx):
        embed = nextcord.Embed(title="Help", description="", color=0xbf00ff)
        await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(HelpCom(bot))
