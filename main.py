import discord
from discord.ext import commands
from discord.ext.commands import Bot,has_permissions
import os
from src.spoti import Spotify_DropdownView 


intents = discord.Intents.default().all()
intents.members = True

description = "ASDSD"

client = Bot(command_prefix='$',description=description, intents=intents, case_insensitivity=True)

@client.event
async def on_ready():
    print("Discord bot started")

@client.command()
async def hello(ctx):
    await ctx.reply("Hi")

    
client.run(os.environ["DISCORD_BOT_TOKEN"])
