from abc import ABC, abstractmethod

class VideoPlayerInterface(ABC):
    
    @abstractmethod
    def play_video(self, video_title: str) -> None:
        pass


