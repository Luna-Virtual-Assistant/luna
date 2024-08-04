from pynput.keyboard import Key, Controller
from services.keyboard.interface import KeyboardControllerInterface

keyboard = Controller()

class KeyboardAdapter(KeyboardControllerInterface):
    def pause_video(self) -> None:
        keyboard.press(Key.media_play_pause)
        keyboard.release(Key.media_play_pause)
        
    def continue_video(self) -> None:
        keyboard.press(Key.media_play_pause)
        keyboard.release(Key.media_play_pause)
        
    def next_video(self) -> None:
        keyboard.press(Key.media_next)
        keyboard.release(Key.media_next)
        
    def previous_video(self) -> None:
        keyboard.press(Key.media_previous)
        keyboard.release(Key.media_previous)
        
    def volume_up(self) -> None:
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        
    def volume_down(self) -> None:
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        
    def mute(self) -> None:
        keyboard.press(Key.media_volume_mute)
        keyboard.release(Key.media_volume_mute)
        