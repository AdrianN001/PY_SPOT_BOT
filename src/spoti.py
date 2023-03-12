
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
import discord

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                               client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                                               redirect_uri="http://localhost:8080",
                                               scope="playlist-modify-private playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"))
sp.trace = False





def get_playlist(user_name):
    choices = []

    playlist = sp.user_playlists(user_name)
    for playlist in playlist["items"]:
        name = playlist["name"]
        id = playlist["id"]
        img = playlist["images"][0]["url"]
        tracks = playlist["tracks"]["href"]

        choices.append( ( name, id, "🎶") )

    return choices

def get_track_of_playlist(playlist_id: str) -> list:
    offset = 0
    tracks = []

    while True:
        response = sp.playlist_items(playlist_id,
                                    offset=offset,
                                    fields='items.track.id,total',
                                    additional_types=['track'])

        if len(response['items']) == 0:
            break

        offset = offset + len(response['items'])
        tracks.append(response['items'])
    return tracks


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