import discord
from discord.ext import commands 
import aiohttp


class Pokedex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        brief='Brief Information of the Pokemon.'
    )
    async def pokeInfo(self, ctx, name: str):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://some-random-api.ml/pokedex?pokemon={name.lower()}") as r:
                    if r.status == 200:
                        data = await r.json(content_type=None)

                        if data is None:
                            await ctx.send(f"No information available for {name}, try again.")
                            return
                            
                        poke_name = data['name'].upper()
                        poke_type = data['type'][0]
                        poke_species = data['species'][0]
                        poke_description = data['description']
                        poke_url = data['sprites']['animated']

                        embed = discord.Embed(
                            title=poke_name,
                            colour=discord.Colour.dark_red()
                        )
                        embed.set_thumbnail(url=poke_url)
                        embed.add_field(name='Type', value=poke_type, inline=False)
                        embed.add_field(name='Species', value=poke_species, inline=False)
                        embed.add_field(name='Description', value=poke_description, inline=False)

                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"There is some problem, please try after some time.")

    
    @commands.command(
        brief='Displays the Stats of Pokemon.'
    )
    async def pokeStats(self, ctx, name: str=""):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://some-random-api.ml/pokedex?pokemon={name.lower()}") as r:
                    if r.status == 200:
                        data = await r.json(content_type=None)

                        if data is None:
                            await ctx.send(f"No information available for {name}, try again.")
                            return

                        poke_name = data['name'].upper()
                        poke_hp = data['stats']['hp']
                        poke_attack = data['stats']['attack']
                        poke_defense = data['stats']['defense']
                        poke_spatk = data['stats']['sp_atk']
                        poke_spdef = data['stats']['sp_def']
                        poke_speed = data['stats']['speed']
                        poke_total = data['stats']['total']

                        embed = discord.Embed(
                            title=poke_name.upper(),
                            colour=discord.Colour.dark_red()
                        )
                        embed.set_thumbnail(url=data['sprites']['animated'])
                        embed.set_footer(text=(
                                f"HP: {poke_hp}\n"
                                f"Defense: {poke_defense}\n"
                                f"Sp. Attack: {poke_spatk}\n"
                                f"Sp. Defense: {poke_spdef}\n"
                                f"Speed: {poke_speed}\n"
                                f"Total: {poke_total}\n"
                        ))

                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"There is some problem, please try after some time.")


def setup(bot):
    bot.add_cog(Pokedex(bot))