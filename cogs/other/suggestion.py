import nextcord
from nextcord.ext import commands
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
from load_config import openConfig


class suggestion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config = openConfig()
    roles = config['modRoles']

    @nextcord.slash_command(guild_ids=[config['guildID']],description="Give a suggestions about the game or the server")
    async def suggestion(
        self,
        interaction: nextcord.Interaction,
        suggestion: str = SlashOption(description="What do you want to suggest?", required=True),
        ):
        config = openConfig()
        id = config['other']['suggestChannel']
        channel = interaction.guild.get_channel(id)
        
        embed = nextcord.Embed(title="Suggestion", description=suggestion, color=0xa5f4ee)
        embed.set_author(name=interaction.user.name, url="", icon_url=interaction.user.avatar.url)
        
        msg = await channel.send(embed=embed)
        await msg.add_reaction("⬆️")
        await msg.add_reaction("⬇️")
        
        embed = nextcord.Embed(title=f"Your suggestion has been submitted", description="", color=0xea4b4b)
        embed.add_field(name="View your suggestion: ", value=f"[Your suggestion]({msg.jump_url})", inline=True)
        embed.set_author(name=interaction.user.name, url="", icon_url=interaction.user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(suggestion(bot))
