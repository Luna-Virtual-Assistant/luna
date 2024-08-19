from mqtt_publisher.publisher import publish
from services.assistant.factory import AssistantFactory
from services.keyboard.factory import KeyboardFactory
from services.youtube.factory import VideoPlayerFactory


class Core():
    _is_selecting_contact = False
    _contacts = []
    _message_to_send = ""
    
    def __init__(self):
        self._name = "Core"
        self._assistant = AssistantFactory.get_assistant("luna")
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
            'who': self.who,
            'today': self.today,
            'help': self.ai_response,
            'duplicated_contacts': self.duplicated_contacts
        }
        
    def run(self, action: str, *args) -> None:
        if action in self._actions:
            self._actions[action](*args)
        else:
            raise ValueError(f"Action {action} is not supported.")
        
    def duplicated_contacts(self, data: dict) -> None:
        print(data)
        contacts = data.get('contacts')
        speak_text = [f"{index + 1} {contact['chat_name']}," for index, contact in enumerate(contacts)]
        self._is_selecting_contact = True
        self._contacts = contacts
        self._message_to_send = data.get('message')
        return publish(f"Para qual contato deseja enviar? {speak_text}", '/tts')
      
    def ai_response(self, prompt: str):
        return publish(prompt, '/ai')
        
    def today(self) -> None:
        print(self._assistant.today())
        
    def who(self) -> None:
        print(self._assistant.who())
        
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
        
