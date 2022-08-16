import json
import random
import nextcord
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
from load_config import openConfig
from cooldowns import SlashBucket
import cooldowns


class Economy(commands.Cog):
    
    config = openConfig()
    
    def __init__(self, bot):
        self.bot = bot
        self.guild = self.config['guildID']
        with open(r'cogs\\bank.json',"r") as i:
            data = json.load(i)
            self.bank = data
        
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
        
    @nextcord.slash_command(guild_ids=[config['guildID']])
    async def balance(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(description="The person whos balance you want to check", required=False)
        ):
        if not member: userid = str(interaction.user.id)
        else: userid = member.id
        userid = str(userid)
        if self.getAccount(member=userid):
            embed = nextcord.Embed(title="Kaid Bank", description=f"{member}", color=0x00ffff)
            embed.add_field(name="Bank", value=f"{self.bank[userid]['bank']}$", inline=True)
            embed.add_field(name="Cash", value=f"{self.bank[userid]['cash']}$", inline=True)
            embed.add_field(name="Net worth", value=f"{self.bank[userid]['cash'] + self.bank[userid]['bank']}$", inline=True)
            await interaction.send(embed=embed)
        else:
            return interaction.send("You do not have an account! Please rejoin to create one.")
           
    @nextcord.slash_command(guild_ids=[config['guildID']])
    @cooldowns.cooldown(1, config["economy"]['cooldown']['workCooldown']*60, bucket=cooldowns.SlashBucket.author)
    async def work(
        self,
        interaction: nextcord.Interaction
        ):
        userid = str(interaction.user.id)
        if random.randint(0, 100) <= 5:
            pay = random.randrange(300, 500)
            self.bank[userid]['cash'] += pay
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Work Bonus", description=f"You did such an amazing job that you got a bonus of {pay}$!", color=0x8a43ed)
            await interaction.send(embed=embed)
            
        else:    
            pay = random.randrange(95, 200)
            self.bank[userid]['cash'] += pay
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Work", description=f"You got {pay}$ for your work!", color=0x8a43ed)
            await interaction.send(embed=embed) 
            
    @nextcord.slash_command(guild_ids=[config['guildID']])
    @cooldowns.cooldown(1, config["economy"]['cooldown']['begCooldown']*60, bucket=cooldowns.SlashBucket.author)
    async def beg(
        self,
        interaction: nextcord.Interaction
        ):
        userid = str(interaction.user.id)
        if random.randint(0, 100) <= 25:
            pay = random.randrange(150, 300)
            self.bank[userid]['cash'] -= pay
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Beg", description=f"Oh no! You got robbed and lost {pay}$ :(", color=0x8a43ed)
            await interaction.send(embed=embed)
        else:
            pay = random.randrange(25, 100)
            self.bank[userid]['cash'] += pay
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Beg", description=f"You earned {pay}$ from begging on the streets.", color=0x8a43ed)
            await interaction.send(embed=embed)
               
    @nextcord.slash_command(guild_ids=[config['guildID']])
    @cooldowns.cooldown(1, config["economy"]['cooldown']['slutCooldown']*60, bucket=cooldowns.SlashBucket.author)
    async def slut(
        self,
        interaction: nextcord.Interaction
        ):
        userid = str(interaction.user.id)
        if random.randint(0, 100) <= 30:
            pay = random.randrange(600, 1050)
            self.bank[userid]['cash'] -= pay
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Slut", description=f"You got arrested for soliciting! You had to pay a {pay}$ fine :(", color=0x8a43ed)
            await interaction.send(embed=embed)
        else:
            pay = random.randrange(400, 550)
            self.bank[userid]['cash'] += pay
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Slut", description=f"You earned {pay}$ from showing off on the streets!", color=0x8a43ed)
            await interaction.send(embed=embed)
            
    @nextcord.slash_command(guild_ids=[config['guildID']])
    async def deposit(
        self,
        interaction: nextcord.Interaction,
        amt: str = SlashOption(description="Amount you want to deposit, or deposit all", required=True)
        ):
        userid = str(interaction.user.id)
        if 'all' in amt: amt = self.bank[userid]['cash']
        if int(amt) > self.bank[userid]['cash']:
            await interaction.send("too poor to do that kekw")
        else:
            self.bank[userid]['cash'] -= int(amt)
            self.bank[userid]['bank'] += int(amt)
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Deposit", description=f"You deposited {int(amt)}$ into your bank.", color=0x8a43ed)
            await interaction.send(embed=embed)
    
    @nextcord.slash_command(guild_ids=[config['guildID']])
    async def withdraw(
        self,
        interaction: nextcord.Interaction,
        amt: str = SlashOption(description="Amount of money you want to withdraw", required=True)
        ):
        userid = str(interaction.user.id)
        if 'all' in amt: amt = self.bank[userid]['bank']
        if int(amt) > self.bank[userid]['bank']:
            await interaction.send("too poor to do that kekw")
        else:
            self.bank[userid]['cash'] += int(amt)
            self.bank[userid]['bank'] -= int(amt)
            self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Withdraw", description=f"You withdrew {int(amt)}$ from your bank.", color=0x8a43ed)
            await interaction.send(embed=embed)

    @nextcord.slash_command(guild_ids=[config['guildID']])
    async def guess(
        self,
        interaction: nextcord.Interaction,
        choice: str = SlashOption(description="The number that you choose", required=True),
        amt = SlashOption(description="Amount of money that your betting", required=True)
        ):
        userid = str(interaction.user.id)
        if int(amt) > self.bank[userid]['cash']:
            await interaction.send("haha to broke for dat kekw")
            return
        else: pass
        
        txt = ""
        choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        aichoice = random.choice(choices) 
        if aichoice == choice:
            name = "Win"
            prize = int(amt)*int(choice)
            txt = f"```You won a prize of {prize}!```"
            self.bank[userid]['cash'] += prize
        else:
            name = "Lose"
            prize = int(amt)*2
            txt = f"```You lost {prize}$ :(```"
            self.bank[userid]['cash'] -= prize
        self.saveAccount(data=self.bank)
        embed = nextcord.Embed(title="Guessing Game", description="", color=0x0aec84)
        embed.add_field(name="AI Choice", value=f"`{aichoice}`", inline=False)
        embed.add_field(name="Your Choice", value=f"`{choice}`", inline=True)
        embed.add_field(name=name, value=txt, inline=False)
        await interaction.send(embed=embed)
        
            
    #Admin commands below
            
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def eco(self, ctx:commands.Context, op, id, amt):
        userid = str(ctx.author.id)
        id = str(id)
        amt = int(amt)
        if self.getAccount(member=id):
            opstr = ""
            # add money
            # remove money
            # add experience
            # remove experience
            if 'am' in op:
                opstr = "Add money"
                self.bank[userid]['bank'] += amt
                self.saveAccount(data=self.bank)
            if 'rm' in op:
                opstr = "Remove money"
                self.bank[userid]['bank'] -= amt
                self.saveAccount(data=self.bank)
            if 'ax' in op:
                opstr = "Add xp"
                self.bank[userid]['xp'] += amt
                self.saveAccount(data=self.bank)
            if 'rx' in op:
                opstr = "Remove xp"
                self.bank[userid]['xp'] -= amt
                self.saveAccount(data=self.bank)
            embed = nextcord.Embed(title="Economy Admin", description="", color=0xf19707)
            embed.add_field(name=opstr, value=f"{float(amt):,}$ on {ctx.guild.get_member(int(id))}", inline=True)
            msg = await ctx.send(embed=embed)
            await msg.delete(delay=10)
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
    

def setup(bot):
    bot.add_cog(Economy(bot))
