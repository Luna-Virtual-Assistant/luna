from abc import ABC, abstractmethod


class KeyboardControllerInterface(ABC):
        
    @abstractmethod
    def pause_video(self) -> None:
        pass
    
    @abstractmethod
    def continue_video(self) -> None:
        pass
    
    @abstractmethod
    def next_video(self) -> None:
        pass
    
    @abstractmethod
    def previous_video(self) -> None:
        pass
    
    @abstractmethod
    def volume_up(self) -> None:
        pass
    
    @abstractmethod
    def volume_down(self) -> None:
        pass
    
    @abstractmethod
    def mute(self) -> None:
        pass
    