import json
import os

from dotenv import load_dotenv
import requests
from mqtt_publisher.publisher import publish
from services.assistant.factory import AssistantFactory
from services.keyboard.factory import KeyboardFactory
from services.youtube.factory import VideoPlayerFactory


load_dotenv(override=True)

class Core():
    _is_selecting_contact = False
    _contacts = []
    _message_to_send = ""
    _command = ""
    
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
            'duplicated_contacts': self.duplicated_contacts,
            'send': self.send_whatsapp_message
        }
        
    def run(self, action: str, *args) -> None:
        if action in self._actions:
            self._command = ' '.join([action, *args])
            self._actions[action](*args)
        else:
            msg = f"Desculpe, não entendi. Tente alguma dessas ações: 'quem', 'hoje', 'toque', 'pause', 'continue', 'próximo', 'anterior', 'aumentar volume', 'diminuir volume', 'silenciar'"
            self.save_to_history(command="error", response=msg)
            raise ValueError(msg)
        
    def send_whatsapp_message(self, text: str) -> None:
        parts = text.split(" para ")
        if len(parts) == 2:
            message_text = parts[0].replace("envie", "").strip()
            contact_name = parts[1].strip()
            
        data = {
            "chatName": contact_name,
            "sessionName": "default",
            "message": message_text,
            "chatId": None
        }
        
        print(data)
        
        self.send_message_to_contact(data)
            
    def send_message_to_contact(self, data: dict) -> None:
        headers = {'Content-Type': 'application/json'}
        requests.post(f"http://{os.getenv('WHATSAPP_REST_HOST')}/send-message?token={os.getenv('WHATSAPP_REST_SECRET')}", json=data, headers=headers)
        publish("stop", "/tts/stop")
        return;
        
    def duplicated_contacts(self, data: str) -> None:
        data = json.loads(data)
        contacts = data.get('contacts')
        speak_text = "; ".join([f"{index + 1} {contact['chat_name']}" for index, contact in enumerate(contacts)])
        self._is_selecting_contact = True
        self._contacts = contacts
        self._message_to_send = data.get('message')
        self.save_to_history(command=self._command, response=f"Contatos duplicados. Selecione um contato: {speak_text}")
        publish("signal", "/luna/web/duplicated")
        return publish(f"Para qual contato deseja enviar? {speak_text}", '/tts')
      
    def ai_response(self, prompt: str):
        return publish(prompt, '/ai')
    
    def save_to_history(self, command: str, response: str) -> None:
        data = {
            "command": command,
            "response": response
        }
        stringified_response = json.dumps(data)
        publish(text=stringified_response, topic="/history")
        return
        
    def today(self, _=None) -> None:
        response = self._assistant.today()
        self.save_to_history(
            command=self._command, response=response
        )
        publish(text=response, topic="/tts")
        return;
        
    def who(self, _=None) -> None:
        response = self._assistant.who()
        self.save_to_history(command=self._command, response=response)
        publish(text=response, topic="/tts")
        return;
        
    def play_video(self, video_title: str) -> None:
        self._video_player.play_video(video_title)
        return self.save_to_history(command=self._command, response=f"Reproduzindo {video_title}")
        
    def pause_video(self) -> None:
        self._keyboard_controller.pause_video()
        return self.save_to_history(command=self._command, response="Pausando mídia")
    
    def continue_video(self) -> None:
        self._keyboard_controller.continue_video()
        return self.save_to_history(command=self._command, response="Retomando mídia")
        
    def next_video(self) -> None:
        self._keyboard_controller.next_video()
        return self.save_to_history(command=self._command, response="Próximo vídeo")
        
    def previous_video(self) -> None:
        self._keyboard_controller.previous_video()
        return self.save_to_history(command=self._command, response="Vídeo anterior")
        
    def volume_up(self) -> None:
        self._keyboard_controller.volume_up()
        return self.save_to_history(command=self._command, response="Aumentando volume")
        
    def volume_down(self) -> None:
        self._keyboard_controller.volume_down()
        return self.save_to_history(command=self._command, response="Diminuindo volume")
        
    def mute(self) -> None:
        self._keyboard_controller.mute()
        return self.save_to_history(command=self._command, response="Silenciando volume")
        
