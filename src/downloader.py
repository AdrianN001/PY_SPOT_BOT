import os

''' Youtube '''
import yt_dlp as youtube_dl

''' Spotify '''
from src.spotify_downloader import SpotifyDownloader

''' Soundcloud '''
from src.soundcloud_downloader import SoundCloudDownloader

class Downloader:

    def __init__(self, url: str, id:str):

        self.url = url 
        self.id  = id      #  Random name of the file


        self.__website = ""

    def __set_website(self) -> None:

        for domain in ["youtube","youtu.be", "spotify","soundcloud"]:
            if domain in self.url:
                self.__website = domain.replace(".","")
                break
    
    def __download_mp3_from_youtube(self) -> None:

        ydl_opts = {
            "outtmpl":f"./temp/{self.id}/%(title)s.%(ext)s",   # save to tmp dir
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
 
    def __download_mp3_from_spotify(self) -> None:
        spotify_client = SpotifyDownloader(self.url, self.id)
        spotify_client.run()

      

    def __download_mp3_from_soundcloud(self) -> None:
        sound_cloud_client = SoundCloudDownloader(self.url, self.id)
        sound_cloud_client.run()

    def run(self) -> None:
        self.__set_website()
        match self.__website:
            case "youtube":
                self.__download_mp3_from_youtube()
            case "spotify":
                self.__download_mp3_from_spotify()
            case "soundcloud":
                self.__download_mp3_from_soundcloud()

    def delete(self) -> None:
        '''Clears the mp3 file from the cache'''

        for file in os.listdir("./temp"):
            if file.startswith(self.id):
                
                os.remove(f"./temp/{self.id}/{os.listdir('./temp/' + self.id)[0]}")
                os.rmdir(f"./temp/{file}")

    @property
    def website(self) -> str:
        return self.__website
    

if __name__ == "__main__":
    client = Downloader("https://soundcloud.com/user-174889742/szivroham")
    client.run()

    print(client.website)