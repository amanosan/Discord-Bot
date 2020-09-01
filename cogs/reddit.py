import praw
from discord.ext import commands
import discord
import random
import dotenv
import os 

dotenv.load_dotenv()
REDDIT_ID = os.getenv('REDDIT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id=REDDIT_ID, client_secret=REDDIT_SECRET,
        user_agent="Discord:luna.bot:1.0.2 (by /u/amanosan)")

    @commands.command(
        brief='Gives a Random Post from a Subreddit.',
        description='Does not work for NSFW Subreddits.'
    )
    async def randomReddit(self, ctx, subreddit: str=""):
        async with ctx.channel.typing():
            if self.reddit:
                chosen_subreddit = 'funny'
                if subreddit:
                    chosen_subreddit = subreddit

                submissions = self.reddit.subreddit(chosen_subreddit).hot()
                post_to_pick = random.randint(1,100)
    
                for i in range(0, post_to_pick):
                    selected_post = next(x for x in submissions if not x.stickied)

                embed = discord.Embed(
                    title=f'Random {chosen_subreddit} Post.',
                    description=f'{selected_post.url}',
                    colour=discord.Colour.orange()
                )
                if not selected_post.is_self:
                    embed.set_image(url=selected_post.url)
                else:
                    embed.set_footer(text=selected_post.selftext)
            
                await ctx.send(embed=embed)

            else:
                await ctx.send("This is currently not working. Please contact the Admin.")


def setup(bot):
    bot.add_cog(Reddit(bot))
