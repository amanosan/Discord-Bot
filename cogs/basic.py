from discord.ext import commands 
import discord
from utils import notify_user

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # this function is an error listener, it will handle all the errors.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        print(ex)
        await ctx.send("Please check with !help the usage of this command, or contact the Administrator")


    @commands.command(
        brief = 'Latency.'
    )
    async def ping(self, ctx):
        await ctx.send(f'Pong {round(self.bot.latency * 1000)}ms')


    @commands.command(
        brief='Greets you back.'
    )
    async def hello(self, ctx):
        await ctx.send(f"Hey there, {ctx.author}")


    @commands.command(
        brief='Create an invite link (valid for 1 Day).'
    )
    @commands.guild_only()  # this function will only work in text channels (not in direct messages)
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_uses=1, unique=True)
        await ctx.send(link)

    
    @commands.command(
        brief='Send a poke to dm.'
    )
    async def poke(self, ctx, member: discord.Member=None):
        if member is not None:
            message = f"{ctx.author.name} poked you!!"
            await notify_user(member, message)
        else:
            await ctx.send("PLease use @mention to poke someone.")


# Setting up the Cog to the Bot.
def setup(bot):
    bot.add_cog(Basic(bot))