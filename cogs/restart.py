from imp import reload
from operator import mod
import os
import nextcord
from load_config import openConfig
from nextcord.ext import commands
import asyncio


class Reload(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def reload(self, ctx:commands.Context, module):
        try:
            if 'all' in module:
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        self.bot.reload_extension(f'cogs.{filename[:-3]}')
                        print(f"Reloaded {filename[:-3]}")
            else:
                self.bot.reload_extension(f"cogs.{module}")
                embed = nextcord.Embed(title="Reload", description=f"Reloaded {module} successfully!", color=0xec0a96)
                await ctx.send(embed=embed)
        except Exception as e:
            print(f"Reloading extension failed! | Error : `{e}`")
            pass

def setup(bot):
    bot.add_cog(Reload(bot))
