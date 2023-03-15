import discord
import spotipy
import asyncio
import random


class Spotify_Dropdown(discord.ui.Select):
    def __init__(self, user_name: str, playlists: list[list[str]], placeholder):

        # Set the options that will be presented inside the dropdown
        self.init_options = playlists
        self.user_name = user_name

        emojis = ["🎧","🎶", "🎹", "🔊","🎙️","🎤"]

        options = [discord.SelectOption(label = x[0], description=x[1], emoji=random.choice(emojis)) for x in playlists]
        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        from src.spoti import get_track_of_playlist, analize_tracks, format_analized_output, build_embed
        
        for name, id, emoji in self.init_options:
            if name == self.values[0]:
                self.chosen_id = id 
        
        await interaction.response.send_message(f'Calculating')

        tracks = get_track_of_playlist(self.user_name,self.chosen_id)

        unformated_ouput = analize_tracks(tuple(tracks))  # Cache-ing

        formated_output = format_analized_output(unformated_ouput)

        await interaction.edit_original_response(embed=build_embed(formated_output), content="Done <3")



class Spotify_DropdownView(discord.ui.View):
    def __init__(self, user_name, options, placeholder):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(Spotify_Dropdown(user_name, options, placeholder))
