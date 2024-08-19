from services.keyboard.adapter import KeyboardAdapter
from services.keyboard.interface import KeyboardControllerInterface

class KeyboardFactory:
    
    @staticmethod
    def get_keyboard(keyboard_type: str) -> KeyboardControllerInterface:
        if keyboard_type == "default":
            return KeyboardAdapter()
        else:
            raise ValueError(f"Keyboard type {keyboard_type} is not supported.")