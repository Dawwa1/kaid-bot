import nextcord
from nextcord.ext import commands
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
from load_config import openConfig
from cogs.moderation.modlog import modlog as ml


class Lock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
        
    config = openConfig()
    roles = config['modRoles']
       
    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config['guildID']],description="Lock a channel")
    async def lock(
        self,
        interaction: nextcord.Interaction,
        rolename: str = SlashOption(description="The role you want to lock the channel for. If None, locks for everyone", required=False)
        ):
        if rolename:
            role = nextcord.utils.get(interaction.guild.roles, name=rolename)
            await interaction.channel.set_permissions(role, send_messages=False)
        else:
            for i in interaction.guild.roles:
                await interaction.channel.set_permissions(i, send_messages=False)
        embed = nextcord.Embed(title="Lock", description="This channel has been locked.", color=0xe7b30a)
        msg = await interaction.send(embed=embed)
        await msg.delete(delay=5)
        
        await ml(message=msg, command="Lock")
        
        
        
    @application_checks.has_any_role(roles)
    @nextcord.slash_command(guild_ids=[config['guildID']],description="Unlock a channel")
    async def unlock(
        self,
        interaction: nextcord.Interaction,
        rolename: str = SlashOption(description="The role you want to unlock the channel for. If None, locks for everyone", required=False)
        ):
        if rolename:
            role = nextcord.utils.get(interaction.guild.roles, name=rolename)
            await interaction.channel.set_permissions(role, send_messages=True)
        else:
            for i in interaction.guild.roles:
                await interaction.channel.set_permissions(i, send_messages=True)
        embed = nextcord.Embed(title="Unlock", description="This channel has been unlocked.", color=0xe7b30a)
        msg = await interaction.send(embed=embed)
        await msg.delete(delay=5)
        await ml(message=msg, command="Unlock")
        
        
            
        
        

    

def setup(bot):
    bot.add_cog(Lock(bot))
