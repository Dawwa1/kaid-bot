import json
import random
import nextcord
from nextcord.ext import commands, application_checks, tasks
from nextcord import SlashOption
from load_config import openConfig
import cooldowns

class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.member = None

    @nextcord.ui.button(label="Claim", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        if self.value:
            member = interaction.user
            self.member = member
        else:
            interaction.response.send_message("Cancelled..", ephemeral=True)
        self.stop()

class Economy(commands.Cog, nextcord.ui.Select):
    
    config = openConfig()
    roles = config['modRoles']
    
    def __init__(self, bot):
        #self.drop.start()
        self.bot = bot
        self.guildid = self.config['guildID']
        with open(r'cogs\\economy\\bank.json',"r") as i:
            data = json.load(i)
            self.bank = data
        
    def createAccount(self, member:str):
        
        self.bank[member] = {
            "bank": 0,
            "cash": 0,
            "xp": 0,
        }
        
        with open(r'cogs\\economy\\bank.json', "w") as f:
            json.dump(self.bank, f, indent=4)
            print(f"Account created")
            
    def getAccount(self, member:str):
        if str(member) in self.bank: return True
        elif str(member) not in self.bank:
            self.createAccount(member=member)
            return True
        else:
            print("Unknown Error!")
            return False
        
    def saveAccount(self):
        data=self.bank
        with open(r'cogs\\economy\\bank.json', "w") as f:
            json.dump(data, f, indent=4)
        
    @nextcord.slash_command(guild_ids=[config['guildID']])
    async def balance(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(description="The person whos balance you want to check", required=False)
        ):
        if not member: 
            userid = str(interaction.user.id)
            member = interaction.user
        else: userid = member.id
        userid = str(userid)
        if self.getAccount(member=userid):
            embed = nextcord.Embed(title="Another Bank", description=f"{member}", color=0x00ffff)
            embed.add_field(name="Bank", value=f"{self.bank[userid]['bank']}$", inline=True)
            embed.add_field(name="Cash", value=f"{self.bank[userid]['cash']}$", inline=True)
            embed.add_field(name="Net worth", value=f"{self.bank[userid]['cash'] + self.bank[userid]['bank']}$", inline=True)
            await interaction.send(embed=embed)
           
    @nextcord.slash_command(guild_ids=[config['guildID']])
    @cooldowns.cooldown(1, config["economy"]['cooldown']['workCooldown']*60, bucket=cooldowns.SlashBucket.author)
    async def work(
        self,
        interaction: nextcord.Interaction
        ):
        userid = str(interaction.user.id)
        if random.randint(0, 100) <= 5:
            pay = random.randrange(685, 950)
            self.bank[userid]['cash'] += pay
            self.saveAccount()
            embed = nextcord.Embed(title="Work Bonus", description=f"You did such an amazing job that you got a bonus of {pay}$!", color=0x8a43ed)
            await interaction.send(embed=embed)
            
        else:    
            pay = random.randrange(95, 365)
            self.bank[userid]['cash'] += pay
            self.saveAccount()
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
            pay = random.randrange(150, 1050)
            self.bank[userid]['cash'] -= pay
            self.saveAccount()
            embed = nextcord.Embed(title="Beg", description=f"Oh no! You got robbed and lost {pay}$ :(", color=0x8a43ed)
            await interaction.send(embed=embed)
        else:
            pay = random.randrange(25, 575)
            self.bank[userid]['cash'] += pay
            self.saveAccount()
            embed = nextcord.Embed(title="Beg", description=f"You earned {pay}$ from begging on the streets.", color=0x8a43ed)
            await interaction.send(embed=embed)
               
    @nextcord.slash_command(guild_ids=[config['guildID']])
    @cooldowns.cooldown(1, config["economy"]['cooldown']['showoffCooldown']*60, bucket=cooldowns.SlashBucket.author)
    async def showoff(
        self,
        interaction: nextcord.Interaction
        ):
        userid = str(interaction.user.id)
        if random.randint(0, 100) <= 30:
            pay = random.randrange(600, 1050)
            self.bank[userid]['cash'] -= pay
            self.saveAccount()
            embed = nextcord.Embed(title="Show off", description=f"You got arrested for soliciting! You had to pay a {pay}$ fine :(", color=0x8a43ed)
            await interaction.send(embed=embed)
        else:
            pay = random.randrange(550, 750)
            self.bank[userid]['cash'] += pay
            self.saveAccount()
            embed = nextcord.Embed(title="Show off", description=f"You earned {pay}$ from showing off on the streets!", color=0x8a43ed)
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
            self.saveAccount()
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
            self.saveAccount()
            embed = nextcord.Embed(title="Withdraw", description=f"You withdrew {int(amt)}$ from your bank.", color=0x8a43ed)
            await interaction.send(embed=embed)
            
    @nextcord.slash_command(guild_ids=[config['guildID']])
    async def pay(
        self,
        interaction: nextcord.Interaction,
        amt: str = SlashOption(description="Amount of money you want to pay", required=True),
        member: nextcord.Member = SlashOption(description="Person that you want to pay", required=True)
        ):
        userid = str(interaction.user.id)
        otheruserid = str(member.id)
        if self.getAccount(otheruserid) and self.getAccount(userid):
            try:
                if int(amt) > self.bank[userid]['bank']:
                    await interaction.response.send_message("bro u aint got that money kekw")
                    return
                else:
                    self.bank[userid]['bank'] -= int(amt)
                    self.bank[otheruserid]['bank'] += int(amt)
                    self.saveAccount()
                    embed = nextcord.Embed(title="Pay", description=f"You paid {str(member)} {amt}$!", color=0x8a43ed)
                    await interaction.send(embed=embed)
            except Exception as e:
                await interaction.response.send_message("oops poopsy, error occured! please contact an admin :D", delete_after=5)
                print(e)
        else:
            await interaction.response.send_message("Error! | Either you entered the wrong member, or the member doesn't have an account!", ephemeral=True)
            return
     
    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config["guildID"]])
    async def drop(
        self,
        interaction: nextcord.Interaction,
        amt: int = SlashOption(description="Amount of money you want to drop", required=True)
    ):
        view = Confirm()
        embed = nextcord.Embed(title="Money Drop", description=f"{interaction.user} has dropped {amt}$", color=0x648ff6)
        msg = await interaction.send(embed=embed, view=view)
        await view.wait()
        if view.value:
            member = view.member
            self.bank[str(member.id)]['bank'] += amt
            self.saveAccount()
            await interaction.send(f"**{member.mention} has claimed the money.**")
            await msg.delete()

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
            txt = f"```You won a prize of {prize}$!```"
            self.bank[userid]['cash'] += prize
        else:
            name = "Lose"
            prize = int(amt)*2
            txt = f"```You lost {prize}$ :(```"
            self.bank[userid]['cash'] -= prize
        self.saveAccount()
        embed = nextcord.Embed(title="Guessing Game", description="", color=0x0aec84)
        embed.add_field(name="AI Choice", value=f"`{aichoice}`", inline=False)
        embed.add_field(name="Your Choice", value=f"`{choice}`", inline=True)
        embed.add_field(name=name, value=txt, inline=False)
        await interaction.send(embed=embed)  
            
    #Admin commands below
            
    @application_checks.has_any_role(*roles)
    @nextcord.slash_command(guild_ids=[config["guildID"]])
    async def eco(
        self,
        interaction:nextcord.Interaction,
        op: str = SlashOption(description="am, rm, ax, rx (add money, remove money, add xp, remove xp)", required=True),
        member: nextcord.Member = SlashOption(description="ID of the person whos account you want to change", required=True),
        amt: int = SlashOption(description="Amount of currency you want to give them", required=True)
        ):
        id = str(member.id)
        amt = int(amt)
        if self.getAccount(member=id):
            opstr = ""
            # add money
            # remove money
            # add experience
            # remove experience
            if 'am' in op:
                opstr = "Add money"
                self.bank[id]['bank'] += amt
                self.saveAccount()
            if 'rm' in op:
                opstr = "Remove money"
                self.bank[id]['bank'] -= amt
                self.saveAccount()
            if 'ax' in op:
                opstr = "Add xp"
                self.bank[id]['xp'] += amt
                self.saveAccount()
            if 'rx' in op:
                opstr = "Remove xp"
                self.bank[id]['xp'] -= amt
                self.saveAccount()
            embed = nextcord.Embed(title="Eco Admin", description=f"{interaction.user} | {opstr} {amt}$ on {interaction.guild.get_member(int(id))}", color=0x9264f6)
            await interaction.send(embed=embed)
            
        else:
            return print("Account invalid")
        
    #Create an account for every member in server
    @application_checks.has_permissions(administrator=True)
    @nextcord.slash_command(guild_ids=[config["guildID"]])
    async def createaccountformembers(self, interaction:nextcord.Interaction):
        guild = interaction.guild
        c = 0
        try:
            async for i in guild.fetch_members():
                if not i.bot:
                    if not self.getAccount(member=i.id):
                        self.createAccount(member=i)
                        c+=1
                else:
                    continue
        except Exception as e:
            print(e)
            
        await interaction.response.send_message(f"Created an account for {c} users")
    

def setup(bot):
    bot.add_cog(Economy(bot))
