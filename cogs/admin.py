from discord.ext import commands
import discord
    

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # function to disable any Cog.
    @commands.command(
        brief='Unload any Cog.'
    )
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send("Could not unload the Cog.")
            return
        await ctx.send("Cog unloaded successfuly.")

    
    # function to load any Cog.
    @commands.command(
        brief='Load any Cog.'
    )
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not load the Cog.")
            return
        await ctx.send("Cog loaded successfuly.")

    
    @commands.command(
        brief='Reload any Cog.'
    )
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not reload the Cog.")
            return
        await ctx.send("Cog reloaded successfuly")



    @commands.command(
        brief='General Information about the Server.'
    )
    @commands.is_owner()
    async def status(self, ctx):
        guild = ctx.guild

        no_voice_channels = len(guild.voice_channels)
        no_text_channels = len(guild.text_channels)

        embed = discord.Embed(
            description='Server Status',
            colour=discord.Colour.dark_purple()
        )
        embed.add_field(name='Server Name', value=guild.name, inline=False)
        embed.add_field(name='# Voice Channels', value=no_voice_channels)
        embed.add_field(name='# Text Channels', value=no_text_channels)

        embed.set_author(name=self.bot.user.name)
        embed.set_thumbnail(url='https://www.root-solutions.co.uk/wp-content/uploads/Technical-Support-Icon.jpg')

        await ctx.send(embed=embed)


    @commands.command(
        brief='Clears previous 5 messages.'
    )
    @commands.is_owner()
    async def clear(self, ctx, amount=6):
        await ctx.channel.purge(limit=amount)


def setup(bot):
    bot.add_cog(Admin(bot))