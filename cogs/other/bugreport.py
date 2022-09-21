from socket import inet_aton
import nextcord
from nextcord.ext import commands
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
from load_config import openConfig


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config = openConfig()
    roles = config['modRoles']

    @nextcord.slash_command(guild_ids=[config['guildID']],description="Report a bug")
    async def bugreport(
        self,
        interaction: nextcord.Interaction,
        report: str = SlashOption(description="The topic of the report", required=True),
        proof: nextcord.Attachment = SlashOption(description="An image or video of the report, if applicable", required=False),
        ):
        config = openConfig()
        id = config['other']['reportChannel']
        channel = interaction.guild.get_channel(id)
        if proof:
            file = await proof.to_file()
            
            embed = nextcord.Embed(title="Report", description=report, color=0xea4b4b)
            embed.set_author(name=interaction.user.name, url="", icon_url=interaction.user.avatar.url)
            await channel.send(embed=embed)
            msg = await channel.send(file=file)
            
            embed = nextcord.Embed(title=f"Your report has been submitted", description="", color=0xea4b4b)
            embed.add_field(name="View your report: ", value=f"[Your report]({msg.jump_url})", inline=True)
            embed.set_author(name=interaction.user.name, url="", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            return
        else:
            embed = nextcord.Embed(title="Report", description=report, color=0xea4b4b)
            embed.set_author(name=interaction.user.name, url="", icon_url=interaction.user.display_avatar.url)
            msg = await channel.send(embed=embed)
            
            embed = nextcord.Embed(title=f"Your report has been submitted", description="", color=0xea4b4b)
            embed.add_field(name="View your report: ", value=f"[Your report]({msg.jump_url})", inline=True)
            embed.set_author(name=interaction.user.name, url="", icon_url=interaction.user.display_avatar.url)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            return

def setup(bot):
    bot.add_cog(Report(bot))
