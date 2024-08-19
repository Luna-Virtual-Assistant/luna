        
from services.youtube.interface import VideoPlayerInterface
import pywhatkit


class YoutubeVideoPlayerAdapter(VideoPlayerInterface):
    
        def play_video(self, video_title: str) -> None:
            pywhatkit.playonyt(video_title)
            

            
        
            
