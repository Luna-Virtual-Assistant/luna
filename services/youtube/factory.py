from services.youtube.adapter import YoutubeVideoPlayerAdapter
from services.youtube.interface import VideoPlayerInterface


class VideoPlayerFactory:
    
    @staticmethod
    def get_video_player(player_type: str) -> VideoPlayerInterface:
        if player_type == "youtube":
            return YoutubeVideoPlayerAdapter()
        else:
            raise ValueError(f"Player type {player_type} is not supported.")