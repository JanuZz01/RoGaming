import discord
from discord.ext import commands
from secrets import *

client = commands.Bot(command_prefix=PREFIX)

@client.event
async def on_ready():
    print(f"Bot is running as {client.user}")

client.run(TOKEN)