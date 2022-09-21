import nextcord
from nextcord import PartialInteractionMessage
from load_config import openConfig

async def modlog(message: nextcord.Message, command: str):
    
    message = await PartialInteractionMessage.fetch(message)
    
    config = openConfig()
    
    guild = message.guild
    
    channel = guild.get_channel(config['moderation']['modLogsChannel'])
    
    if not message.embeds:
        a = message.content
        pass
    else:
        for embed in message.embeds:
            a = embed.title
    
    embed = nextcord.Embed(title=f"{command} command by {message.author}", description="", color=0x87f18f)
    embed.add_field(name=f"Channel: {message.channel}", value=f"Message: ```{a}```", inline=True)
    await channel.send(embed=embed)