from __future__ import print_function
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import discord

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                               client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                                               redirect_uri="http://localhost:8080",
                                               scope="playlist-modify-private playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"))
sp.trace = False




class Spotify_Dropdown(discord.ui.Select):
    def __init__(self, options: list[list[str]], placeholder):

        # Set the options that will be presented inside the dropdown

        options = [discord.SelectOption(label = x[0], description=x[1], emoji=[2]) for x in options]
        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder, min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's 
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')


class Spotify_DropdownView(discord.ui.View):
    def __init__(self, *args):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(args))


def get_playlist(user_name):
    choices = []

    playlist = sp.user_playlists(username)
    for playlist in playlist["items"]:
        name = playlist["name"]
        id = playlist["id"]
        img = playlist["images"][0]["url"]
        tracks = playlist["tracks"]["href"]

        choices.append( ( name, id, "🎶") )

    return choices

def analyze_playlist(track): 
    Ellipsis




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