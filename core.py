import keyword
from services.keyboard.factory import KeyboardFactory
from services.youtube.factory import VideoPlayerFactory

class Core:
    def __init__(self):
        self._name = "Core"
        self._video_player = VideoPlayerFactory.get_video_player("youtube")
        self._keyboard_controller = KeyboardFactory.get_keyboard("default")
        self._actions = {
            'play': self.play_video,
            'pause': self.pause_video,
            'continue': self.continue_video,
            'next': self.next_video,
            'previous': self.previous_video,
            'volume_up': self.volume_up,
            'volume_down': self.volume_down,
            'mute': self.mute,
        }
        
    def run(self, action: str, *args) -> None:
        if action in self._actions:
            self._actions[action](*args)
        else:
            raise ValueError(f"Action {action} is not supported.")
        
    def play_video(self, video_title: str) -> None:
        self._video_player.play_video(video_title)
        
    def pause_video(self) -> None:
        self._keyboard_controller.pause_video()
    
    def continue_video(self) -> None:
        self._keyboard_controller.continue_video()
        
    def next_video(self) -> None:
        self._keyboard_controller.next_video()
        
    def previous_video(self) -> None:
        self._keyboard_controller.previous_video()
        
    def volume_up(self) -> None:
        self._keyboard_controller.volume_up()
        
    def volume_down(self) -> None:
        self._keyboard_controller.volume_down()
        
    def mute(self) -> None:
        self._keyboard_controller.mute()
        
