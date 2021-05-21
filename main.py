from discord.ext import commands
import os
import dotenv
import os

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix='!')

# Adding all the Cog Files
for filename in os.listdir('./cogs'):
    if filename.endswith(".py") and filename != '__init__.py':
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(BOT_TOKEN)
