from discord.ext import commands
import discord
from utils import *


class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, ex):
    #     print(ex)
    #     await ctx.send("Please check with !help the usage of this command, or contact the Administrator")


    @commands.command(
        brief=("Random Yo Mamma! jokes.")
    )
    async def insult(self, ctx, member: discord.Member = None):
        insult = await get_momma_joke()
        if member is not None:
            await ctx.send(f"{member.name} eat this : {insult}")
        else:
            await ctx.send(insult)



def setup(bot):
    bot.add_cog(NSFW(bot))
