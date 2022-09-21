import os
import random
import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from load_config import openConfig


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config = openConfig()

    @nextcord.slash_command(guild_ids=[config['guildID']], description="Gives you a random number from 1 to the number you set (not above 10k)")
    async def random(
        self,
        interaction: nextcord.Interaction,
        number: int = SlashOption(description="The highest number you want it to generate (can't be above 10k). If unspecified, its 10k", required=False)
        ):
        if not number or number > 10000: number = 10000
        number = random.randrange(1, number)
        embed = nextcord.Embed(title="Random Number Generator", description=f"```Your number is {number}```", color=0xf47b45)
        await interaction.send(embed=embed)
    

def setup(bot):
    bot.add_cog(Fun(bot))
