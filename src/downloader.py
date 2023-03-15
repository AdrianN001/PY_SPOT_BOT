import os

''' Youtube '''
import yt_dlp as youtube_dl


''' Spotify '''
from savify import Savify
from savify.types import  Format, Quality
from savify.logger import Logger
from savify.utils import PathHolder


''' Soundcloud '''
from soundcloud_downloader import SoundCloudDownloader

class Downloader:

    def __init__(self, url: str):

        self.url = url 

        self.__website = ""

    def __set_website(self) -> None:

        for domain in ["youtube","youtu.be", "spotify","soundcloud"]:
            if domain in self.url:
                self.__website = domain.replace(".","")
                break
    
    def __download_mp3_from_youtube(self) -> None:

        ydl_opts = {
            "outtmpl":f"./temp/YT-%(title)s.%(ext)s",   # save to tmp dir
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


        logger = Logger(log_location='path/for/logs', log_level=None) # Silent output
        spotify_client = Savify(    api_credentials=( os.environ.get("SPOTIPY_CLIENT_ID"), os.environ.get("SPOTIPY_CLIENT_SECRET") ),
                                    quality=Quality.BEST,
                                    download_format=Format.MP3, 
                                    path_holder=PathHolder(downloads_path='./temp'),
                                    logger=logger
                                     )
        
        spotify_client.download(self.url)

    def __download_mp3_from_soundcloud(self) -> None:
        sound_cloud_client = SoundCloudDownloader(self.url)
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


    @property
    def website(self) -> str:
        return self.__website
    

if __name__ == "__main__":
    client = Downloader("https://soundcloud.com/user-174889742/szivroham")
    client.run()

    print(client.website)