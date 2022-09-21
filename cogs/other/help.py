import nextcord
from nextcord.ext import commands
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
from load_config import openConfig


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config = openConfig()
    roles = config['modRoles']
    
    @nextcord.slash_command(guild_ids=[config['guildID']],description="See what commands the bot can do!")
    async def help(
        self,
        interaction: nextcord.Interaction,
        ):
        config = openConfig()
        
        me = interaction.guild.get_member(647949070937096192)
        
        
        embed = nextcord.Embed(title="Help Command", description="See all the features that the bot has!", color=0x85cadf)
        embed.add_field(name="/cat", value="Gives you a random picture of a cat from reddit!", inline=True)
        embed.add_field(name="/random", value="Gives you a random number from 1 to a number that you input", inline=True)
        embed.add_field(name="/balance", value="Check how poor (or rich) you are", inline=True)
        embed.add_field(name="/deposit", value="Deposit your cash into your bank account", inline=True)
        embed.add_field(name="/withdraw", value="Withdraw money from your bank to cold hard cash", inline=True)
        embed.add_field(name="/pay", value="Pay someone else money", inline=True)
        embed.add_field(name="/work", value=f"Work a 9-5 and earn a steady income | Cooldown: {config['economy']['cooldown']['workCooldown']} minutes", inline=True)
        embed.add_field(name="/beg", value=f"Beg on the streets for a few cents | Cooldown: {config['economy']['cooldown']['begCooldown']} minutes", inline=True)
        embed.add_field(name="/showoff", value=f"Show off on the streets for some $$$ | Cooldown: {config['economy']['cooldown']['showoffCooldown']} minutes", inline=True)
        embed.add_field(name="/guess", value="If you guess the same number as the bot, you hit the jackbot!", inline=True)
        embed.set_footer(text="Made by Dawwa#0001", icon_url=me.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        

def setup(bot):
    bot.add_cog(Help(bot))