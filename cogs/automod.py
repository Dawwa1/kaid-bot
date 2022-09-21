import nextcord
from nextcord.ext import commands
from load_config import openConfig
from cogs.moderation.modlog import modlog as ml


class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled = self.config['automod']['enabled']
        self.logchannel = self.config['logging']['logging_channel']

    @commands.Cog.listener(name='on_message')
    async def on_message(self, message:nextcord.Message):
        
        config = openConfig()
        roles = config['modRoles']
        
        for i in roles:
            role = message.guild.get_role(i)
            if role in message.author.roles:
                return
            else:
                continue
            
        badwords = self.config['automod']['filter']['blacklisted_words']
        mentions = self.config['automod']['filter']['allowableMentions']
        if message.author.bot:
            return
        else:
            for i in badwords:
                if i in message.content:
                    await message.delete()
            if len(message.mentions) > mentions:
                await message.delete()
        await ml(message=message, command="Automod")
            

def setup(bot):
    bot.add_cog(Automod(bot))
