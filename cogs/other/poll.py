import nextcord
from nextcord.ext import commands
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
from load_config import openConfig


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config = openConfig()
    roles = config['modRoles']
    
    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config['guildID']],description="Inisiate a poll")
    async def poll(
        self,
        interaction: nextcord.Interaction,
        polltopic: str = SlashOption(description="The topic of the poll", required=True)
        ):
        
        embed = nextcord.Embed(title=polltopic, description="", color=0xea4b4b)
        await interaction.send(embed=embed)
        msg = await interaction.original_message()
        await msg.add_reaction("👍")
        await msg.add_reaction("🤷")
        await msg.add_reaction("👎")
        

def setup(bot):
    bot.add_cog(Poll(bot))
