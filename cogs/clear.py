import nextcord
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
from load_config import openConfig

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    config = openConfig()

    @application_checks.has_permissions(kick_members=True)
    @nextcord.slash_command(guild_ids=[config['guildID']])
    async def clear(
        self,
        interaction: nextcord.Interaction,
        number: int = SlashOption(description="Number of messages that you want to delete", required=False)
        ):
        if not number: number = 1000
        msgs = await interaction.channel.purge(limit=number, bulk=True)
        await interaction.response.send_message(f"Deleted {len(msgs)} messages", ephemeral=True)
    

def setup(bot):
    bot.add_cog(Clear(bot))
