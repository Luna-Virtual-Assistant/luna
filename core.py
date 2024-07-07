from youtube.factory import VideoPlayerFactory


class Core:
    def __init__(self):
        self._name = "Core"
        self._player_type = "youtube"
        self._video_player = VideoPlayerFactory.get_video_player(self._player_type)
        self._actions = {
            "toque": self.play_video
        }
        
    def play_video(self, video_title: str) -> None:
        self._video_player.play_video(video_title)