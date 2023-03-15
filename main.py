import discord
from discord.ext import commands, tasks 
from discord.ext.commands import Bot,has_permissions
import os
import asyncio
from src.spoti import get_playlist
from src.dropdown import *
from src.downloader import Downloader
from string import ascii_letters

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
async def download(ctx, *, url: str) -> None: 
    id = "".join([random.choice(ascii_letters) for _ in range(20)])
    dl = Downloader(url, id)


    dl.run()
    await ctx.send(f"Elkezdem a letöltést {dl.website}-ról.")


    for file in os.listdir("./temp"):
        if file.startswith(id):
            file_name = f"./temp/{id}/" + os.listdir(f"./temp/{id}/")[0]
            await ctx.send(file=discord.File(file_name))
            break
    await asyncio.sleep(5)
    dl.delete()

@client.command()
async def analize(ctx, *, user_name):
    cache = {} # cache the Dropdown

    if not user_name: 
        return await ctx.reply("Felhasználása: \n analize {felhasználónév}")

    if user_name in cache: 
        user_playlist_view = cache[user_name]
    else:
        playlist = get_playlist(user_name)
        user_playlist_view = Spotify_DropdownView( user_name, playlist ,"Chose a playlist pls")
        cache[user_name] = user_playlist_view
    
    print(cache)
     
    #view = Spotify_DropdownView( user_name, playlist ,"Chose a playlist pls")

    await ctx.send("Válaszd ki a playlistet", view=user_playlist_view)

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