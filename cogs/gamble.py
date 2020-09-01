from discord.ext import commands
import random
import discord

class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # this function is an error listener, it will handle all the errors.
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, ex):
    #     print(ex)
    #     await ctx.send("Please check with !help the usage of this command, or contact the Administrator")


    @commands.command(
        brief='Gives a random number between 1 and 100.'
    )
    async def randomn(self, ctx):
        n = random.randint(1, 100)
        await ctx.send(n)


    @commands.command(
        brief='Rolls a Dice.'
    )
    async def dice(self, ctx):
        n = random.randint(1, 6)
        await ctx.send(n)
    
    
    @commands.command(
        brief='Tosses a Coin.'
    )
    async def toss(self, ctx):
        n = random.choice(['Heads', 'Tails'])
        await ctx.send(f"It's a {n}")


    @commands.command(
        brief='Ask any question.',
        aliases=['8ball']
    )
    async def _8ball(self, ctx, *, question):
        results = [
        'It is certain.',
        'It is decidedly so.',
        'Without a doubt.',
        'Yes - definitely.',
        'You may rely on it.',
        'As I see it, yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',
        'Reply hazy, try again.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate ans ask again.',
        'Dont count on it.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.'
        ]
        embed = discord.Embed(
            title='Magical 8 Ball',
            description=f'Question: {question}\nAnswer: {random.choice(results)}',
            colour=ctx.author.colour
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Gamble(bot))
