from discord.ext import commands
import discord
from utils import mods_or_owner, notify_user


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        brief='Kick members.'
    )
    @mods_or_owner()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)  # checking for correct permission.
    async def kick(self, ctx, member: discord.Member=None,
    reason: str='You have been kicked because of unappropriate behaviour'):
        if member is not None:
            await ctx.guild.kick(member, reason=reason)
            await notify_user(member, reason)
        else:
            await ctx.send("Please specify user to kick via mention.")

    @commands.command(
        brief='Ban members.'
    )
    @mods_or_owner()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None,
    reason: str='You have been banned for unappropriate behaviour.'):
        if member is not None:
            await ctx.guild.ban(member, reason=reason)
            await notify_user(member, reason)
        else:
            await ctx.send("Please specify user to ban via mention.")


    @commands.command(
        brief='Unban members.'
    )
    @mods_or_owner()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: str='', reason: str='You have been unbanned.'):
        if member == "":
            await ctx.send("PLease specify the username as text to unban.")
            return

        bans = await ctx.guild.bans()  # getting all banned usernames
        for b in bans:
            if b.user.name == member:
                await ctx.guild.unban(b.user, reason=reason)
                await notify_user(b.user, reason)
                await ctx.send("User was unbanned.")
                return
            
        await ctx.send('User not found in banned list, please check again.')


def setup(bot):
    bot.add_cog(Moderator(bot))