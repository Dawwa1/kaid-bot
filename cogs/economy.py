import json
import nextcord
import random
import math
from nextcord.ext import commands
from main import guildID


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = guildID
        with open(r'cogs\\bank.json',"r") as i:
            data = json.load(i)
            self.bank = data
        
    def createAccount(self, member: nextcord.Member):
        if not str(member.id) in self.bank:
            with open(r'cogs\\bank.json',"r") as i:
                data = json.load(i)
                self.bank = data

            data[member.id] = {
                "balance": 0,
                "cash": 0,
                "xp": 0,
            }
            with open(r'cogs\\bank.json', "w") as f:
                json.dump(self.bank, f, indent=4)
                print("Account created")
        else:
            print("Member in bank")
            
    def getAccount(self, member:str):
        if str(member) in self.bank: return True
        else: return False
        
    def saveAccount(self, data):
        with open(r'cogs\\bank.json', "w") as f:
            json.dump(data, f, indent=4)
        
    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        author = ctx.message.author.id
        if self.getAccount(member=author):
            embed = nextcord.Embed(title="Kaid Bank", description="", color=0x00ffff)
            embed.add_field(name="Balance", value=f"{self.bank[str(author)]['balance']}$", inline=True)
            await ctx.send(embed=embed)
        else:
            return ctx.send("You do not have an account! Please rejoin to create one.")
        
    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work(self, ctx):
        pay = random.randrange(50, 200)
        id = str(ctx.message.author.id)
        self.bank[id]['balance'] += pay
        self.saveAccount(data=self.bank)
        embed = nextcord.Embed(title="Work", description=f"You got {pay}$ for your work!", color=0x011adf)
        await ctx.send(embed=embed)
        
    @commands.Cog.listener(name="on_command_error")
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = nextcord.Embed(title="Cooldown!", description=f' Command on cooldown. Try again in {math.trunc((error.retry_after / 60) + 1)} minutes' , color=0xff0000)
            await ctx.send(embed=embed)
            
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def eco(self, ctx, op, id, amt):
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
                self.bank[id]['balance'] += amt
                self.saveAccount(data=self.bank)
            if 'rm' in op:
                opstr = "remove money"
                self.bank[id]['balance'] -= amt
                self.saveAccount(data=self.bank)
            if 'ax' in op:
                opstr = "add xp"
                self.bank[id]['xp'] += amt
                self.saveAccount(data=self.bank)
            if 'rx' in op:
                opstr = "remove xp"
                self.bank[id]['xp'] -= amt
                self.saveAccount(data=self.bank)
            msg = await ctx.send(f"{opstr}: {float(amt):,} on {ctx.guild.get_member(int(id))}")
            await msg.delete(delay=5)
        else:
            return print("Account invalid")
        
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def createAccountForMembers(self, ctx):
        guild = ctx.guild
        print(guild)
        async for i in guild.fetch_members():
            print(i)
            self.createAccount(member=i)
        

def setup(bot):
    bot.add_cog(Economy(bot))
