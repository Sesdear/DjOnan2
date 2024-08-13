import discord

from discord.ext import commands
import requests

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='shit')
    async def shit(self, ctx, mode: str = None):
        if mode == "yourself":
            print('Try to request')
            response = requests.get("https://evilinsult.com/generate_insult.php",
                                    params={"lang": "ru", "type": "json"})
            insult = response.json()
            print(f'Request done output: {insult['insult']}')
            await ctx.send(insult['insult'])

async def setup(bot):
    await bot.add_cog(Fun(bot))