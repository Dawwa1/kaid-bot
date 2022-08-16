import math
import os
import time
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
from dotenv import load_dotenv
from load_config import openConfig

config = openConfig()
guildID = config['guildID']
prefix = config['prefix']

intents = nextcord.Intents.all()

bot = commands.Bot(command_prefix=prefix,help_command=None, intents=intents)
 
economyStatus = config['economy']['enabled']
welcomeStatus = config['on_join']['enabled']

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded {filename[:-3]}")
    else:
        pass

load_dotenv()

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
async def on_command_error(ctx:commands.Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        ping = await ctx.send(ctx.author.mention)
        embed = nextcord.Embed(title="Cooldown!", description=f"Command on cooldown. Try again in {math.trunc((error.retry_after / 60) + 1)} minutes" , color=0xff0000)
        em = await ctx.send(embed=embed)
        await em.delete(delay=10)
        await ping.delete(delay=10)
    if isinstance(error, commands.MissingPermissions):
        ping = await ctx.send(ctx.author.mention)
        embed = nextcord.Embed(title="Permission Error", description=f"You do not have the required permissions to execute this command!" , color=0xff0000)
        em = await ctx.send(embed=embed)
        await ctx.message.delete()
        await em.delete(delay=10)
        await ping.delete(delay=10)

#@bot.event
#async def on_application_command_error(error, interaction:nextcord.Interaction):
#    if isinstance(error, application_checks.ApplicationMissingPermissions):
#        await interaction.send("test")

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
        eco.createAccount(member=member)
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
        
        
        
from cogs.economy import Economy

token = config['token']
bot.run(token)