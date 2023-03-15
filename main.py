import discord
from discord.ext import commands
from discord.ext.commands import Bot,has_permissions
import os
from src.spoti import get_playlist
from src.dropdown import *
from src.downloader import Downloader


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
async def analize(ctx, *, user_name):
    if not user_name: 
        ctx.reply("Felhasználása: \n analize {felhasználónév}")

    playlist = get_playlist(user_name)
     
    view = Spotify_DropdownView( user_name, playlist ,"Chose a playlist pls")

    await ctx.send("Válaszd ki a playlistet", view=view)

@client.command()
async def hello(ctx):
    await ctx.reply("Hi")

    
client.run(os.environ["DISCORD_BOT_TOKEN"])