import json
import os
import random
from discord.ext import commands
from utils import *
import discord


async def notify_user(member, message):
    if member is not None:
        channel = member.dm_channel
        if channel is None:
            channel = await member.create_dm()
        await channel.send(message)


# Creating our own coroutine to check for owner and different roles:
def mods_or_owner():
    def predicate(ctx):
        return commands.check_any(
        commands.is_owner(),
        commands.has_role('moderator')
        )
    return commands.check(predicate)

async def get_momma_joke():
    path = r'C:\Users\AMAN OSSAN\Documents\Python\Projects\Discord Bot\data\jokes.json'
    with open(path, encoding='utf-8') as file:
        jokes = json.load(file)

    random_category = random.choice(list(jokes.keys()))
    insult = random.choice(list(jokes[random_category]))

    return insult
