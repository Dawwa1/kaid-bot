import datetime
import nextcord
from nextcord.ext import commands
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
from load_config import openConfig


class Serverevents(commands.Cog):
    def __init__(self, bot: nextcord.Client):
        self.bot = bot


    config = openConfig()
    roles = config['modRoles']

    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config['guildID']],description="Create a server event!")
    async def createevent(
        self,
        interaction: nextcord.Interaction,
        stage_channel: nextcord.StageChannel = SlashOption(description="The stage channel where you want to create an event", required=True),
        event_name : str = SlashOption(description="The name of the event", required=True),
        event_description : str = SlashOption(description="Describe your event!", required=True),
        event_start_time_month: int = SlashOption(description="The month you want to start your event (ex, 12 = December)", required=True),
        event_start_time_day : int = SlashOption(description="The day you want to start the event", required=True),
        sign_up_channel : nextcord.TextChannel = SlashOption(description="The channel where people will sign up for the event", required=True)
        ):
        config = openConfig()
        
        guild = self.bot.get_guild(config['guildID'])
        
        year = datetime.datetime.now().year
        s = f"{year}{event_start_time_month}{event_start_time_day}"
        e = f"{year}{event_start_time_month}{event_start_time_day+1}"
        start_time = datetime.datetime.strptime(s, '%Y%m%d')
        end_time = datetime.datetime.strptime(e, '%Y%m%d')
        
        event = await guild.create_scheduled_event(name=event_name, description=event_description, channel=stage_channel ,entity_type=nextcord.ScheduledEventEntityType.stage_instance, start_time=start_time, end_time=end_time)
        await interaction.response.send_message(f"{event_name} has been successfully created!", ephemeral=True)
        
        embed = nextcord.Embed(title=f"{event}", description="", color=0xdb87f1)
        embed.add_field(name=f"Description", value=event.description, inline=False)
        embed.add_field(name=f"Location", value=f"{event.channel}", inline=False)
        embed.add_field(name=f"Time", value=f"{event.start_time}", inline=False)
        
        await sign_up_channel.send(embed=embed)
        
    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config['guildID']],description="Check event attendee's")
    async def checkevent(
        self,
        interaction: nextcord.Interaction,
        event_id: str = SlashOption(description="The id of the event that you want to check", required=True)
    ):
        event = self.bot.get_scheduled_event(int(event_id))
        if not event:
            await interaction.response.send_message("You have entered the wrong event ID.", ephemeral=True)
        else:
            embed = nextcord.Embed(title=f"{event} stats", description="", color=0xdb87f1)
            embed.add_field(name=f"Description", value=event.description, inline=False)
            embed.add_field(name=f"Creator", value=event.creator, inline=False)
            embed.add_field(name=f"Location", value=f"{event.channel}", inline=False)
            embed.add_field(name=f"Interested", value=event.user_count, inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        

def setup(bot):
    bot.add_cog(Serverevents(bot))
