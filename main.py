import fnmatch
import math
import os
import time
import nextcord
from nextcord.ext import commands, application_checks
from load_config import openConfig
from cooldowns import CallableOnCooldown

config = openConfig()
guildID = config['guildID']
prefix = config['prefix']

intents = nextcord.Intents.all()

bot = commands.Bot(command_prefix=prefix,help_command=None, intents=intents)
 
economyStatus = config['economy']['enabled']
welcomeStatus = config['on_join']['enabled']

root = './cogs'
pattern = "*.py"

for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch.fnmatch(name, pattern):
            paths = os.path.join(path, name)[2:][:-3]
            pathsFormatted = paths.replace("\\", ".")
            try:
                bot.load_extension(pathsFormatted)
                print(f"Loaded {pathsFormatted}")
            except Exception as e:
                print(e)

@bot.event
async def on_ready():
    print(f"\n{bot.user} has connected to Discord!")
    print(f"Bot is in {len(bot.guilds)} servers")
    if not economyStatus:
        print("\nEconomy functions disabled!")
        bot.unload_extension('cogs.economy')
    if not welcomeStatus:
        print("\nWelcome functions disabled!")

@bot.event
async def on_application_command_error(interaction:nextcord.Interaction, error):
    if isinstance(error, nextcord.ApplicationInvokeError):
        error = error.original
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        embed = nextcord.Embed(title="Permission Error", description=f"You do not have the required permissions to execute this command!" , color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
    if isinstance(error, application_checks.ApplicationMissingAnyRole):
        embed = nextcord.Embed(title="Permission Error", description=f"You do not have the required permissions to execute this command!" , color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
    if isinstance(error, CallableOnCooldown):
        ping = interaction.user.mention
        embed = nextcord.Embed(title="Cooldown!", description=f"{ping} Command on cooldown. Try again in {math.trunc((error.retry_after / 60) + 1)} minutes" , color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
    else:
        raise error

@bot.event
async def on_member_join(member:nextcord.Member):
    if welcomeStatus:
        channel = bot.get_channel(config['on_join']['welcomeChannel'])
        welcomeMessage = config['on_join']['welcomeMessage'].replace("{member}", "{guild}", str(member), str(member.guild))
        role = await getRole(id=int(config['on_join']['roleOnJoin']))
        if not role:
            return
        embed = nextcord.Embed(title=welcomeMessage, description="", color=0x0bda0a)
        msg = await channel.send(embed=embed)
        await msg.add_reaction("🥳")
    if economyStatus:
        eco = Economy(bot=bot)
        eco.createAccount(member=str(member.id))
    else:
        return

    
    
    
def countdown(t):
    while t:
        mins, secs = divmod(t,60)
        timer = '{:02d}:{:02d}'.format(mins,secs)
        print(timer,end='\r')
        time.sleep(1)
        t-=1
    print("Exiting...")
    
    
    
async def getRole(id:int):
    guild = bot.get_guild(guildID)
    role = guild.get_role(id)
    if role: return role
    else: return False
        
        
        
from cogs.economy.economy import Economy

token = config['token']
bot.run(token)
