import discord
from discord.ext import commands, tasks 
from discord.ext.commands import Bot,has_permissions
import os
import asyncio
from src.spoti import get_playlist
from src.dropdown import *


intents = discord.Intents.default().all()
intents.members = True
description = "ASDSD"

client = Bot(command_prefix='$',description=description, intents=intents, case_insensitivity=True)


file = open("asset/lyrics.txt", "r")
global lyrics
lyrics = file.readlines()

global offset
offset = 0


@client.event
async def on_ready():
    user = await client.fetch_user(os.environ["DISCORD_AUTHOR_ID"])
    if user:
        await user.send("```Waltuh Started```")
    lyrics_task.start()
    print("Discord bot started")

@client.command()
async def analize(ctx, *, user_name):
    cache = {} # cache the Dropdown

    if not user_name: 
        return await ctx.reply("Felhasználása: \n analize {felhasználónév}")

    if user_name in cache: 
        user_playlist_view = cache[user_name]
    else:
        playlist = get_playlist(user_name)
        view = Spotify_DropdownView( user_name, playlist ,"Chose a playlist pls")
        cache[user_name] = view
    
    print(cache)
     
    #view = Spotify_DropdownView( user_name, playlist ,"Chose a playlist pls")

    await ctx.send("Válaszd ki a playlistet", view=view)

@client.command()
async def hello(ctx):
    await ctx.reply("Hi")

@tasks.loop()
async def lyrics_task() -> None:
    while True:
        for offset in range(lyrics.__len__()):
            await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name=lyrics[offset]))
            await asyncio.sleep(7)
    


print(os.environ["DISCORD_BOT_TOKEN"])
client.run(os.environ["DISCORD_BOT_TOKEN"])