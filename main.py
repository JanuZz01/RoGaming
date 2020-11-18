import discord
from discord.ext import commands
from secrets import *
import os

client = commands.Bot(command_prefix=PREFIX)

commands = discord

for file in os.listdir("./Commands"):
    if file.endswith(".py"):
        print(f"Loaded : {file[:-3]}")
        client.load_extension(f"Commands.{file[:-3]}")

client.load_extension("Events")

client.run(TOKEN)