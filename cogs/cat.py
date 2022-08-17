import asyncpraw
import nextcord
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
from load_config import openConfig


class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image = False

    config = openConfig()

    def checkIfImage(self, imgurl:str):
        try:
            if not "https://i.redd.it" in imgurl:
                self.image = False
                return
            elif "https://i.redd.it" in imgurl:
                self.image = True
                return
        except Exception as e:
            print(e)

    @nextcord.slash_command(guild_ids=[config['guildID']], description="Gives you a random picture of a cat")
    async def cat(
        self,
        interaction: nextcord.Interaction
        ):
        reddit = asyncpraw.Reddit(
            client_id="",
            client_secret="",
            password="",
            user_agent="",
            username=""
        )
        try:
            subreddit = await reddit.subreddit("Kitten")
            async for submission in subreddit.random_rising():
                self.checkIfImage(submission.url)
                if self.image == True:
                    embed = nextcord.Embed(title="Cat", description=f"Post by u/{submission.author}", color=0x83f88d)
                    embed.set_image(url=submission.url)
                    await interaction.response.send_message(embed=embed)
                    return
                else:
                    continue
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(Cat(bot))
