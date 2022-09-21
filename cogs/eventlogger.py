from email import message
import nextcord
from nextcord.ext import commands
from load_config import openConfig


class Eventlogger(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.config = openConfig()
        self.enabled = self.config['logging']['enabled']
        self.logchannel = self.config['logging']['logging_channel']
        gid = self.config['guildID']
        if not self.enabled:
            return

    @commands.Cog.listener(name='on_message_delete')
    async def on_message_delete(self, message:nextcord.Message):
        
        if not message.embeds:
            a = message.content
            pass
        else:
            for embed in message.embeds:
                a = embed.title
        
        channel = await self.bot.fetch_channel(self.logchannel)
        embed = nextcord.Embed(title="Message Deleted", description="", color=0x646ef6)
        embed.add_field(name=str(message.author), value=f"Message: ```{a}```", inline=True)
        await channel.send(embed=embed)

    @commands.Cog.listener(name='on_message_edit')
    async def on_message_edit(self, before, after):
        if len(before.embeds) > 0:
            return
        else:
            channel = await self.bot.fetch_channel(self.logchannel)
            embed = nextcord.Embed(title="Message Edited", description="", color=0x646ef6)
            embed.add_field(name=str(before.author), value=f"**Before:** ```{before.content}``` **After:** ```{after.content}```", inline=False)
            await channel.send(embed=embed)
        
    @commands.Cog.listener(name='on_reaction_add')
    async def on_reaction_add(self, reaction: nextcord.Reaction, user:nextcord.User):
        if user.bot:
            return
        channel = await self.bot.fetch_channel(self.logchannel)
        embed = nextcord.Embed(title="Reaction Added", description="", color=0x646ef6)
        embed.add_field(name=str(user), value=f"[Reaction:]({reaction.message.jump_url}) ```{reaction.emoji}```", inline=True)
        await channel.send(embed=embed)
        
    @commands.Cog.listener(name='on_guild_scheduled_event_create')
    async def on_guild_scheduled_event_create(self, event:nextcord.ScheduledEvent):
        channel = await self.bot.fetch_channel(self.logchannel)
        embed = nextcord.Embed(title="Event Created", description="", color=0x646ef6)
        embed.add_field(name="Event Name", value=f"```{event.name}```", inline=False)
        await channel.send(embed=embed)
        
    @commands.Cog.listener(name='on_reaction_remove')
    async def on_reaction_remove(self, reaction: nextcord.Reaction, user: nextcord.User):
        channel = await self.bot.fetch_channel(self.logchannel)
        embed = nextcord.Embed(title="Reaction Removed", description="", color=0x646ef6)
        embed.add_field(name=str(user), value=f"[Reaction:]({reaction.message.jump_url}) ```{reaction.emoji}```", inline=True)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Eventlogger(bot))
