import nextcord
from nextcord.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(kick_members=True)
    @commands.command(aliases=['cl'])
    async def clear(self, ctx, numOfMsgs:int = None):
        if not numOfMsgs: numOfMsgs = 5000
        await ctx.channel.purge(limit=numOfMsgs+1, bulk=True)
    

def setup(bot):
    bot.add_cog(Clear(bot))
