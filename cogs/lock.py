import nextcord
from nextcord.ext import commands


class Lock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.has_permissions(kick_members=True)
    @commands.command(aliases=['l'])
    async def lock(self, ctx, roleName: str = None):
        if roleName:
            role = nextcord.utils.get(ctx.guild.roles, name=roleName.lower())
            msg = await ctx.channel.set_permissions(role, send_messages=False)
            await msg.delete(delay=5)
        else:
            for i in ctx.guild.roles:
                msg = await ctx.channel.set_permissions(i, send_messages=False)
                await msg.delete(delay=5)
    
    
    @commands.has_permissions(kick_members=True)
    @commands.command(aliases=['ul'])
    async def unlock(self, ctx, roleName: str = None):
        if roleName:
            role = nextcord.utils.get(ctx.guild.roles, name=roleName.lower())
            msg = await ctx.channel.set_permissions(role, send_messages=True)
            await msg.delete(delay=5)
        else:
            for i in ctx.guild.roles:
                msg = await ctx.channel.set_permissions(i, send_messages=True)
                await msg.delete(delay=5)
            
        
        

    

def setup(bot):
    bot.add_cog(Lock(bot))
