import nextcord
from nextcord.ext import commands
from load_config import openConfig


class Eventlogger(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.config = openConfig()
        self.enabled = self.config['logging']['enabled']
        self.logchannel = self.config['logging']['logging_channel']


    @commands.Cog.listener(name='on_message_delete')
    async def on_message_delete(self, message:nextcord.Message):
        channel = await self.bot.fetch_channel(self.logchannel)
        embed = nextcord.Embed(title="Message Deleted", description="", color=0x646ef6)
        embed.add_field(name=str(message.author), value=f"Message: ```{message.content}```", inline=True)
        await channel.send(embed=embed)

    @commands.Cog.listener(name='on_message_edit')
    async def on_message_edit(self, before, after):
        channel = await self.bot.fetch_channel(self.logchannel)
        embed = nextcord.Embed(title="Message Edited", description="", color=0x646ef6)
        embed.add_field(name=str(before.author), value=f"**Before:** ```{before.content}``` **After:** ```{after.content}```", inline=False)
        await channel.send(embed=embed)
        
    #@commands.Cog.listener(name='on_guild_channel_create')
    #async def on_guild_channel_create(self, channel:nextcord.TextChannel):
    #    user = None
    #    async for entry in channel.guild.audit_logs(action=nextcord.AuditLogAction.channel_create):
    #        user = entry.user
    #    channel = await self.bot.fetch_channel(self.logchannel)
    #    embed = nextcord.Embed(title="Channel Created", description="", color=0x646ef6)
    #    embed.add_field(name=f"**Channel Name: **```{channel.name}```", value=f"**Created by: **```{user}```", inline=False)
    #    await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Eventlogger(bot))
