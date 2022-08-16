import os
import nextcord
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
from load_config import openConfig


class Reload(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    config = openConfig()

    @application_checks.has_permissions(administrator=True)
    @nextcord.slash_command(guild_ids=[config['guildID']],description="Reload a module")
    async def reload(
        self,
        interaction: nextcord.Interaction,
        module = SlashOption(description="The module that you want to restart", required=True)
        ):
        try:
            if 'all' in module:
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        self.bot.reload_extension(f'cogs.{filename[:-3]}')
                        print(f"Reloaded {filename[:-3]}")
            else:
                self.bot.reload_extension(f"cogs.{module}")
                embed = nextcord.Embed(title="Reload", description=f"Reloaded {module} successfully!", color=0xec0a96)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            print(f"Reloading extension failed! | Error : `{e}`")
            pass

def setup(bot):
    bot.add_cog(Reload(bot))
