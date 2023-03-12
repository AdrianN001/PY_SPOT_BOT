import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
import discord

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                               client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                                               redirect_uri="http://localhost:8080",
                                               scope="playlist-modify-private playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"))
sp.trace = False

def analize_tracks(tracks: list[str]) -> list: 
    playlist_features_list = ["danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]

    playlist_features = {}
    for track_id in tracks:
        try:
            audio_features = sp.audio_features(track_id)[0]
        except TypeError:  # Nonetype is not itarable
            continue
        for feature in playlist_features_list:
            if feature in playlist_features:
                playlist_features[feature].append(audio_features[feature])
            else: 
                playlist_features[feature] = [audio_features[feature]]
    
    return playlist_features

def get_playlist(user_name):
    choices = []

    playlist = sp.user_playlists(user_name)
    for playlist in playlist["items"]:
        name = playlist["name"]
        id = playlist["id"]
        

        choices.append( ( name, id, "🎶") )

    return choices

def get_track_of_playlist(user_name: str,playlist_id: str) -> list: 
    return [ track["track"]["id"] for track in sp.user_playlist_tracks(user_name,playlist_id)["items"]]


def format_analized_output(output: dict) -> dict: 
    formated_output = {} 

    for key,value in output.items():

        match key:
            case 'danceability' |  'energy' |  'loudness' |  'speechiness' |  "instrumentalness" | "liveness" | "valence" :
                avg = sum(value)/len(value)
                avg *= 100  # Percentage
                formated_output[key] = round(avg,2)
            case "tempo":
                avg = sum(value)/len(value) 
                formated_output[key] = round(avg,2)
            case 'duration_ms':
                avg_in_seconds = ( sum(value)/len(value) ) / 1000
                formated_output['duration'] = round(avg_in_seconds)
          
    return formated_output

def build_embed( formated_output: dict ) -> discord.Embed:
    embed = discord.Embed(title = "Spotify analyzer", description="bottom text")
    embed.set_thumbnail(url="https://img-cdn.tnwcdn.com/image?fit=1280%2C720&url=https%3A%2F%2Fcdn0.tnwcdn.com%2Fwp-content%2Fblogs.dir%2F1%2Ffiles%2F2021%2F02%2FSpotify-Lossless-lossy.jpg&signature=2c31bda805a4e9c87ab4ed25e4b3f604")
    for key,value in formated_output.items():
        match key: 
            case "valence":
                circles = ['🔴', "🟢","🟡","🔵"]
                ball_value = f"{random.choice(circles) * int(value / 10)}{'⚫'* (10-int(value/10))}"[:10]
                embed.add_field(name=f"HAPPINESS ({value} / 100)", value=ball_value, inline=False)
            case "tempo":
                embed.add_field(name="Hajtás", value=f"{value} bpm", inline=False)
            case "duration":
                embed.add_field(name="Átlag hossz", value=f"{value} másodperc", inline=False)
            case _:
                circles = ['🔴', "🟢","🟡","🔵"]
                ball_value = f"{random.choice(circles) * int(value / 10)}{'⚫'* (10-int(value/10))}"[:10]
                embed.add_field(name=f"{str(key).upper()} ({value} / 100)", value=ball_value, inline=False)
    return embed   


if __name__ == "__main__":
    print(get_playlist("gogosadrian"))


# artist_name = "Azahriah"

# results = sp.search(q=artist_name, limit=50)
# tids = []
# for i, t in enumerate(results['tracks']['items']):
#     print(' ', i, t['name'])
#     tids.append(t['uri'])

# start = time.time()
# features = sp.audio_features(tids)
# delta = time.time() - start
# for feature in features:
#     print(json.dumps(feature, indent=4))
#     print()
   
# print("features retrieved in %.2f seconds" % (delta,))