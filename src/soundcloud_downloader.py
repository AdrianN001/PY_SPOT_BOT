import requests 
import re
from youtubesearchpython import VideosSearch
import yt_dlp as youtube_dl

class SoundCloudDownloader:

    def __init__( self, url: str ):

        self.url = url
    
    def __set_title_and_artists( self ) -> None:
        
        res = requests.get(self.url)

        title_line = ""
        for line in res.content.decode().split("\n"):
            if re.match(r"^<title>.*</title>$", line):
                title_line = line
                break
        
        title_line = title_line.removeprefix("<title>Stream ")
        
        title_line = title_line.split("|")[0]

        self.artist, self.title = reversed(title_line.split(" by "))

    
   

    def __fetch_youtube_results( self ) -> str:

        self.__set_title_and_artists()

        videosSearch = VideosSearch(f'{self.artist} - {self.title}', limit = 1)

        link = videosSearch.result()['result'][0]['link']
        return link

    def run(self) -> None:
        song_url = self.__fetch_youtube_results()
        ydl_opts = {
            "outtmpl":f"./temp/%(title)s.%(ext)s",   # save to tmp dir
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            }
         
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song_url])
    
if __name__ == "__main__":
    SoundCloudDownloader("https://soundcloud.com/user-174889742/szivroham").run()
    #SoundCloudDownloader("https://soundcloud.com/horipeti15/majka-curtis-blr-belehalok").fetch_youtube_results()