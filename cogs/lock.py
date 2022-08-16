import nextcord
from nextcord.ext import commands


class Lock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.has_permissions(kick_members=True)
    @commands.command(aliases=['l'])
    async def lock(self, ctx, roleName: str = None):
        if roleName:
            role = nextcord.utils.get(ctx.guild.roles, name=roleName)
            await ctx.channel.set_permissions(role, send_messages=False)
        else:
            for i in ctx.guild.roles:
                await ctx.channel.set_permissions(i, send_messages=False)
        await ctx.message.delete()
        embed = nextcord.Embed(title="Lock", description="This channel has been locked.", color=0xe7b30a)
        await ctx.send(embed=embed)
    
    
    @commands.has_permissions(kick_members=True)
    @commands.command(aliases=['ul'])
    async def unlock(self, ctx, roleName: str = None):
        if roleName:
            role = nextcord.utils.get(ctx.guild.roles, name=roleName)
            await ctx.channel.set_permissions(role, send_messages=True)
        else:
            for i in ctx.guild.roles:
                await ctx.channel.set_permissions(i, send_messages=True)
        await ctx.message.delete()
        embed = nextcord.Embed(title="Unlock", description="This channel has been unlocked.", color=0xe7b30a)
        msg = await ctx.send(embed=embed)
        await msg.delete(delay=5)
        
            
        
        

    

def setup(bot):
    bot.add_cog(Lock(bot))
