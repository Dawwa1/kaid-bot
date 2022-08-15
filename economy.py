import json
import nextcord
import random
import math
from nextcord.ext import commands
from main import guildID
import main


class Economy(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.guild = guildID
        with open(r'cogs\\bank.json',"r") as i:
            data = json.load(i)
            self.bank = data
        self.config = main.config
        
    def createAccount(self, member: nextcord.Member):
        if not str(member.id) in self.bank:
            with open(r'cogs\\bank.json',"r") as i:
                data = json.load(i)
                self.bank = data

            data[member.id] = {
                "bank": 0,
                "cash": 0,
                "xp": 0,
            }
            with open(r'cogs\\bank.json', "w") as f:
                json.dump(self.bank, f, indent=4)
                print(f"Account created for {member}")
        else:
            print("Member in bank")
            
    def getAccount(self, member:str):
        if str(member) in self.bank: return True
        else: return False
        
    def saveAccount(self, data):
        with open(r'cogs\\bank.json', "w") as f:
            json.dump(data, f, indent=4)
        
    @commands.command(aliases=['bal'])
    async def balance(self, ctx:commands.Context):
        userid = str(ctx.message.author.id)
        if self.getAccount(member=userid):
            embed = nextcord.Embed(title="Kaid Bank", description="", color=0x00ffff)
            embed.add_field(name="Bank", value=f"{self.bank[userid]['bank']}$", inline=True)
            embed.add_field(name="Cash", value=f"{self.bank[userid]['cash']}$", inline=True)
            embed.add_field(name="Net worth", value=f"{self.bank[userid]['cash'] + self.bank[userid]['bank']}$", inline=True)
            await ctx.send(embed=embed)
        else:
            return ctx.send("You do not have an account! Please rejoin to create one.")
        
    @commands.command()
    @commands.cooldown(1, main.config["economy"]['cooldown']['workCooldown']*60, commands.BucketType.user)
    async def work(self, ctx:commands.Context):
        userid = str(ctx.message.author.id)
        if random.randint(0, 100) <= 5:
            pay = random.randrange(300, 500)
            self.bank[userid]['cash'] += pay
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Work Bonus", description=f"You did such an amazing job that you got a bonus of {pay}$!", color=0x8a43ed)
            await ctx.send(embed=embed)
            
        else:    
            pay = random.randrange(50, 200)
            self.bank[userid]['cash'] += pay
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Work", description=f"You got {pay}$ for your work!", color=0x8a43ed)
            await ctx.send(embed=embed)
        
    @commands.command()
    @commands.cooldown(1, main.config['economy']['cooldown']['begCooldown']*60, commands.BucketType.user)
    async def beg(self, ctx:commands.Context):
        userid = str(ctx.message.author.id)
        if random.randint(0, 100) <= 25:
            pay = random.randrange(150, 300)
            self.bank[userid]['cash'] -= pay
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Beg", description=f"Oh no! You got robbed and lost {pay}$ :(", color=0x8a43ed)
            await ctx.send(embed=embed)
        else:
            pay = random.randrange(25, 100)
            self.bank[userid]['cash'] += pay
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Beg", description=f"You earned {pay}$ from begging on the streets.", color=0x8a43ed)
            await ctx.send(embed=embed)
        
    @commands.command()
    @commands.cooldown(1, main.config['economy']['cooldown']['slutCooldown']*60, commands.BucketType.user)
    async def slut(self, ctx:commands.Context):
        userid = str(ctx.message.author.id)
        if random.randint(0, 100) <= 30:
            pay = random.randrange(600, 1050)
            self.bank[userid]['cash'] -= pay
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Slut", description=f"You got arrested for soliciting! You had to pay a {pay}$ fine :(", color=0x8a43ed)
            await ctx.send(embed=embed)
        else:
            pay = random.randrange(400, 550)
            self.bank[userid]['cash'] += pay
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Slut", description=f"You earned {pay}$ from showing off on the streets!", color=0x8a43ed)
            await ctx.send(embed=embed)
    
    @commands.command(aliases=["dep"])
    async def deposit(self, ctx:commands.Context, amt=None):
        userid = str(ctx.message.author.id)
        if 'all' in amt: amt = self.bank[userid]['cash']
        if int(amt) > self.bank[userid]['cash']:
            await ctx.send("too poor to do that kekw")
        else:
            self.bank[userid]['cash'] -= int(amt)
            self.bank[userid]['bank'] += int(amt)
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Deposit", description=f"You depositeed {int(amt)}$ into your bank.", color=0x8a43ed)
            await ctx.send(embed=embed)
    
    @commands.command(aliases=["with"])
    async def withdraw(self, ctx:commands.Context, amt=None):
        userid = str(ctx.message.author.id)
        if 'all' in amt: amt = self.bank[userid]['bank']
        if int(amt) > self.bank[userid]['bank']:
            await ctx.send("too poor to do that kekw")
        else:
            self.bank[userid]['cash'] += int(amt)
            self.bank[userid]['bank'] -= int(amt)
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Withdraw", description=f"You withdrew {int(amt)}$ from your bank.", color=0x8a43ed)
            await ctx.send(embed=embed)
            
    #Admin commands below
            
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def eco(self, ctx:commands.Context, op, id, amt):
        userid = str(ctx.message.author.id)
        id = str(id)
        amt = int(amt)
        if self.getAccount(member=id):
            opstr = ""
            # add money
            # remove money
            # add experience
            # remove experience
            if 'am' in op:
                opstr = "add money"
                self.bank[userid]['bank'] += amt
                self.saveAccount(data=self.bank)
            if 'rm' in op:
                opstr = "remove money"
                self.bank[userid]['bank'] -= amt
                self.saveAccount(data=self.bank)
            if 'ax' in op:
                opstr = "add xp"
                self.bank[userid]['xp'] += amt
                self.saveAccount(data=self.bank)
            if 'rx' in op:
                opstr = "remove xp"
                self.bank[userid]['xp'] -= amt
                self.saveAccount(data=self.bank)
            msg = await ctx.send(f"{opstr}: {float(amt):,} on {ctx.guild.get_member(int(id))}")
            print(msg)
            await msg.delete(delay=5)
        else:
            return print("Account invalid")
        
    #Create an account for every member in server
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def createAccountForMembers(self, ctx:commands.Context):
        guild = ctx.guild
        print(guild)
        async for i in guild.fetch_members():
            if not i.bot:
                if not self.getAccount(member=i.id):
                    self.createAccount(member=i)
                    await ctx.message.delete(delay=0)
            else:
                continue
            
    @commands.Cog.listener(name="on_command_error")
    async def on_command_error(self, ctx:commands.Context, error):
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
    

def setup(bot):
    bot.add_cog(Economy(bot))
