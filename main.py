import discord
from discord.ext import commands
from discord.ext.commands import Bot,has_permissions
import os
from src.spoti import get_playlist
from src.dropdown import *


intents = discord.Intents.default().all()
intents.members = True

description = "ASDSD"

client = Bot(command_prefix='$',description=description, intents=intents, case_insensitivity=True)

@client.event
async def on_ready():
    user = await client.fetch_user("510515915125948426")
    if user:
        await user.send("```Waltuh Started```")
    print("Discord bot started")

@client.command()
async def view(ctx, *, user_name):

    playlist = get_playlist(user_name)
     
    view = Spotify_DropdownView( playlist ,"Chose a playlist pls")

    await ctx.send("Valami", view=view)

@client.command()
async def hello(ctx):
    await ctx.reply("Hi")

    
client.run(os.environ["DISCORD_BOT_TOKEN"])