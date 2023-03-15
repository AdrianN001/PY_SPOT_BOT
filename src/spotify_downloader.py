
from youtubesearchpython import VideosSearch
import yt_dlp as youtube_dl

import requests
import bs4

class SpotifyDownloader:

    def __init__( self, url: str, id: str ):

        self.url = url
        print(self.url)
        self.id = id
    
    def __set_title_and_artists( self ) -> None:
        
        res = requests.get(self.url)

        soup = bs4.BeautifulSoup(res.text, features="lxml")

        html_title = soup.find_all("title")[0]

        html_title = str(html_title).removeprefix("<title>")

        html_title = html_title.split(" |")[0]

        html_title = html_title.replace("- song and lyrics","").replace("song","")

        print(html_title.split("by"))

        self.title, self.artist = html_title.split("by")

    
   

    def __fetch_youtube_results( self ) -> str:

        self.__set_title_and_artists()

        videosSearch = VideosSearch(f'{self.artist} - {self.title}', limit = 1)

        link = videosSearch.result()['result'][0]['link']
        return link

    def run(self) -> None:
        song_url = self.__fetch_youtube_results()
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
            ydl.download([song_url])
        
    
if __name__ == "__main__":
    SpotifyDownloader(r"https://open.spotify.com/track/2ynCjjrmED5CfiVn2ZLkUk","asd213").run()
    #SoundCloudDownloader("https://soundcloud.com/horipeti15/majka-curtis-blr-belehalok").fetch_youtube_results()