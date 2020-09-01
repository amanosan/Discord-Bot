import aiohttp
import discord
from discord.ext import commands
import random

class Facts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        brief='Random Animal Facts.',
        description='Currently works with: [dog, cat, panda, fox, koala, bird, racoon, kangaroo]'
    )
    async def animalFact(self, ctx, animal: str):
        animal = animal.lower()
        if animal in (['dog', 'cat', 'panda', 'fox', 'koala', 'bird', 'racoon', 'kangaroo']):
            if animal == 'bird':
                fact_url = "https://some-random-api.ml/animal/birb"
            else:
                fact_url = f'https://some-random-api.ml/animal/{animal}'

            async with aiohttp.ClientSession() as cs:
                async with cs.get(fact_url) as r:
                    if r.status == 200:
                        data = await r.json()
                        embed = discord.Embed(
                            title=f'{animal.upper()} FACT',
                            description=data['fact'],
                            colour=ctx.author.colour

                        )
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"API returned {r.status} code.")
        else:
            await ctx.send("No fact availabe for this animal.")


def setup(bot):
    bot.add_cog(Facts(bot))