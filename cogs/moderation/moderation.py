import asyncio
import json
from xml.sax.handler import EntityResolver
import nextcord
from nextcord.ext import commands
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
from load_config import openConfig
from cogs.moderation.modlog import modlog as ml


class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(r'cogs\\moderation\\moderation.json',"r") as i:
            data = json.load(i)
            self.db = data

    config = openConfig()
    roles = config['modRoles']


#ENTRY CREATION


    def create_entry(self, id:str):
        self.db[id] = {
            "warns": 0,
            "mutes": 0,
            "kicks": 0,
            "is_banned": False
        }
        with open(r'cogs\\moderation\\moderation.json', "w") as f:
            json.dump(self.db, f, indent=4)
                
    def check_account(self, id):
        if str(id) in self.db: return True
        elif str(id) not in self.db:
            self.create_entry(id=str(id))
            return True
        else:
            print("Unknown Error! | moderation.py")
            return False
        
    def save_account(self):
        with open(r'cogs\\moderation\\moderation.json', "w") as f:
            json.dump(self.db, f, indent=4)
            
            
    def add_to_entry(self, id, entry):
        id = str(id)
        
        
        if not self.check_account(id=id):
            self.create_entry(id)
        
        
        
        if 'w' in entry:
            entry = "warns"
            
        elif 'm' in entry:
            entry = "mutes"
            
        elif 'b' in entry:
            entry = "is_banned"
            self.db[id][entry] = True
            self.save_account()
            return
        
        elif 'k' in entry:
            entry = "kicks"
           
        else:
            print("Entry invalid")
        
        
            
        try:
            self.db[id][entry] += 1
            self.save_account()
            return True
        
        except Exception as e:
            print(f"Error: can't add to entry\nTraceback: {e}")
            return False
        
    def subtract_from_entry(self, id, entry):
        
        id = str(id)
        
        
        if not self.check_account(id=id):
            self.create_entry(id)
        
        
        
        if 'w' in entry:
            entry = "warns"
            
        elif 'm' in entry:
            entry = "mutes"
            
        elif 'b' in entry:
            entry = "is_banned"
            self.db[id][entry] = False
            self.save_account()
            return
        
        elif 'k' in entry:
            entry = "kicks"
           
        else:
            print("Entry invalid")
        
        
            
        try:
            self.db[id][entry] -= 1
            self.save_account()
            return True
        
        except Exception as e:
            print(f"Error: can't subtract from entry\nTraceback: {e}")
            return False
            
            
            
#COMMANDS     
            

    #Warn

    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config['guildID']])
    async def warn(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(description="Who are you warning", required=True),
        reason: str = SlashOption(description="What's the reason for warning them", required=False)
        ):
        
        if not reason:
            reason = "Not following the rules"
        
        id = str(member.id)
        
        self.add_to_entry(id=id, entry="w")
        
        embed = nextcord.Embed(title="Warn", description="", color=0xed6969)
        embed.add_field(name=f"{member} has been warned for: ", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)
        await member.send(f"You have been warned for {reason} by {interaction.user}!")
    
    
    
    #MUTE
    
    
    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config['guildID']])
    async def mute(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(description="Who are you muting", required=True),
        time: str = SlashOption(description="How long do you want to mute them for? (5s = 5 seconds, 6h = 6 hours etc)", required=True),
        reason: str = SlashOption(description="What's the reason for muting them", required=False)
        ):
        config = openConfig()
        role = interaction.guild.get_role(config['moderation']['muteRole'])
        timeConverted = self.convert_time_to_seconds(time=time)
        
        if not reason:
            reason = "Not following the rules"
        if role in member.roles:
            interaction.response.send_message("Member is already muted!")

        
        await member.add_roles(role, reason=reason)
        self.add_to_entry(id=member.id, entry="m")
        
        
        embed = nextcord.Embed(title=f"{interaction.user} muted {member}", description="", color=0xed6969)
        embed.add_field(name="Moderator: ", value=interaction.user, inline=False)
        embed.add_field(name="Reason: ", value=reason, inline=False)
        embed.add_field(name="Duration: ", value=time, inline=False)
        
        message = await interaction.response.send_message(embed=embed)
        
        await ml(message=message, command="Mute")
        
        await asyncio.sleep(int(timeConverted))
        
        await member.remove_roles(role)
        
    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config['guildID']])
    async def unmute(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(description="Who are you unmuting", required=True)
        ):
        config = openConfig()
        
        role = interaction.guild.get_role(config['moderation']['muteRole'])


        if not role in member.roles:
            await interaction.response.send_message("Member is already unmuted!")
            
        
        await member.remove_roles(role)
        
        
        embed = nextcord.Embed(title=f"{interaction.user} unmuted {member}", description="", color=0xed6969)
        embed.add_field(name="Moderator: ", value=interaction.user, inline=False)
        
        message = await interaction.response.send_message(embed=embed)
        
        await ml(message=message, command="Unmute")
        
    
    def convert_time_to_seconds(self, time):
        
        time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        
        try:
            return int(time[:-1]) * time_convert[time[-1]]
        except:
            return time
        
        
        
        
        
    #BAN
        
        
    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config['guildID']],description="Ban a member of the server")
    async def ban(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(description="Person that you want to ban", required=True),
        reason: str = SlashOption(description="What's the reason that you're banning them", required=False)
        ):
        if not reason:
            reason = "Not following the rules"
            
        await interaction.guild.ban(member, reason=reason)
        self.add_to_entry(id=member.id, entry='b')
        
        embed = nextcord.Embed(title=f"{member} has been banned", description="", color=0xed6969)
        embed.add_field(name="Moderator: ", value=interaction.user, inline=False)
        embed.add_field(name="Reason: ", value=reason, inline=False)
        
        msg = await interaction.send(embed=embed)
        await ml(message=msg, command="Ban")
        
        
    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config['guildID']],description="Unban a member of the server")
    async def unban(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(description="Person that you want to unban", required=True),
        reason: str = SlashOption(description="What's the reason that you're unbanning them", required=False)
        ):
        if not reason:
            reason = "They learned their lesson"
            
        await interaction.guild.unban(member, reason=reason)
        self.subtract_from_entry(id=member.id, entry='b')
        
        embed = nextcord.Embed(title=f"{member} has been unbanned", description="", color=0xed6969)
        embed.add_field(name="Moderator: ", value=interaction.user, inline=False)
        embed.add_field(name="Reason: ", value=reason, inline=False)
        msg = await interaction.send(embed=embed)
        
        await ml(message=msg, command="Ban")
        
        
    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config['guildID']],description="Kick a member of the server")
    async def kick(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(description="Person that you want to kick", required=True),
        reason: str = SlashOption(description="What's the reason that you're kicking them", required=False)
        ):
        if not reason:
            reason = "Not following the rules"
            
        await interaction.guild.kick(member, reason=reason)
        await self.add_to_entry(id=member.id, entry="k")
        
        embed = nextcord.Embed(title=f"{member} has been kicked", description="", color=0xed6969)
        embed.add_field(name="Moderator: ", value=interaction.user, inline=False)
        embed.add_field(name="Reason: ", value=reason, inline=False)
        
        msg = await interaction.send(embed=embed)
        await ml(message=msg, command="Kick")
        

    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config['guildID']],description="Check the # of warns a member has")
    async def info(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(description="Person that you want to kick", required=True)
        ):
        try:
            embed = nextcord.Embed(title=f"Info of {member}", description="", color=0xed6969)
            embed.add_field(name="Warns: ", value=self.db[str(member.id)]['warns'], inline=False)
            embed.add_field(name="Mutes: ", value=self.db[str(member.id)]['mutes'], inline=False)
            embed.add_field(name="Kicks: ", value=self.db[str(member.id)]['kicks'], inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
            await interaction.response.send_message("Member doesn't exist in database!", ephemeral=True)
        

    

def setup(bot):
    bot.add_cog(moderation(bot))