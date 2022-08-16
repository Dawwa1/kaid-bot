import nextcord
from nextcord.ext import commands
from cogs.load_config import openConfig


class HelpCom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = openConfig()


    @commands.command()
    async def help(self, ctx:commands.Context):
        try:
            embed = nextcord.Embed(title="Help", description="", color=0xbf00ff)
            embed.add_field(name="Economy", value="All economy commands", inline=False)
            embed.add_field(name="work", value=f"Earn money through legally working. {self.config['economy']['cooldown']['workCooldown']}m cooldown", inline=True)
            embed.add_field(name="beg", value=f"Beg on the streets for money. {self.config['economy']['cooldown']['begCooldown']}m cooldown", inline=True)
            embed.add_field(name="slut", value=f"Solicit on the streets. More money, higher risk! {self.config['economy']['cooldown']['slutCooldown']}m cooldown", inline=True)
            embed.add_field(name="guess {choice} {amt}", value="if you choose the same number as the bot, you earn money!", inline=True)
            embed.add_field(name="Economy Admin", value="All economy admin commands", inline=False)
            embed.add_field(name="eco {action} {account number} {amount}", value="Remove or add money and remove or add xp", inline=True)
            embed.add_field(name="createAccountForMembers", value="Creates an account for every member in the server", inline=True)
            embed.add_field(name="General Admin", value="General admin commands", inline=False)
            embed.add_field(name="lock {role name = OPTIONAL}", value="Lock a channel for everyone, or a specific role", inline=True)
            embed.add_field(name="clear {# of messages = OPTIONAL}", value="Deletes the specifed # of messages. If not specifed, deletes all", inline=True)
            embed.add_field(name="GetId {member}", value="Gets the id of the specified member", inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
    

def setup(bot):
    bot.add_cog(HelpCom(bot))
