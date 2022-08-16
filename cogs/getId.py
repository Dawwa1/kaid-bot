import nextcord
from nextcord.ext import commands

class getid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Get ID Command Self Explanatory
    @commands.command(pass_context = True)
    async def getid(self, ctx , member : nextcord.Member):
        IdEmbed = nextcord.Embed(
        title=f"{member._user}'s Id",
        color=0x2852fa, 
        description=f"The Id Of {member._user} is {member.id}")
        IdEmbed.set_thumbnail(member.avatar.url)
        await ctx.send(embed=IdEmbed)

    @getid.error
    async def getid_error(self, ctx, error):
        if isinstance(error , commands.MissingRequiredArgument):
            await ctx.send(f"<@{ctx.author.id}> \nThis Command Usage Is ` -GetId [Member] `")

#Setup 
def setup(bot):
    client.add_cog(getid(bot))
