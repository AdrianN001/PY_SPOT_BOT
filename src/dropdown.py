import discord
import spotipy


class Spotify_Dropdown(discord.ui.Select):
    def __init__(self, options: list[list[str]], placeholder):

        # Set the options that will be presented inside the dropdown
        self.init_options = options

        options = [discord.SelectOption(label = x[0], description=x[1], emoji="🎶") for x in options]
        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        from src.spoti import get_track_of_playlist
        print(self.init_options)
        
        for name, id, emoji in self.init_options:
            if name == self.values[0]:
                self.chosen_id = id 
        
        await interaction.response.send_message(f'Your favourite colour is {self.chosen_id}')

        print(get_track_of_playlist(self.chosen_id))



class Spotify_DropdownView(discord.ui.View):
    def __init__(self, options, placeholder):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Spotify_Dropdown(options, placeholder))
