import tomli
import os
import time
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix='-',help_command=None, intents=intents)
 
with open('config.toml', mode="rb") as fp:
    config = tomli.load(fp)
    
guildID = config['guildID']

load_dotenv()

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    print(f"Bot is in {len(bot.guilds)} servers")
    
@bot.event
async def on_member_join(member):
    eco = Economy(bot=bot)
    channel = bot.get_channel(config['on_join']['welcomeChannel'])
    welcomeMessage = config['on_join']['welcomeMessage'].replace("{member}", str(member))
    role = await getRole(id=int(config['on_join']['roleOnJoin']))
    eco.createAccount(member=member)
    if not role:
        return
    else:
        await member.add_roles(role)
    embed = nextcord.Embed(title=welcomeMessage, description="", color=0x0bda0a)
    msg = await channel.send(embed=embed)
    await msg.add_reaction("🥳")
    
def countdown(t):
    while t:
        mins, secs = divmod(t,60)
        timer = '{:02d}:{:02d}'.format(mins,secs)
        print(timer,end='\r')
        time.sleep(1)
        t-=1
    print("Exiting...")
    
async def getRole(id:int):
    guild = bot.get_guild(980870866638340166)
    role = guild.get_role(id)
    if role: return role
    else: return False

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded {filename[:-3]}")
    else:
        print(f'Unable to load {filename[:-3]}')

from cogs.economy import Economy

token = config['token']
bot.run(os.getenv('TOKEN'))