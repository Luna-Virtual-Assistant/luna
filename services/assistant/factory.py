from services.assistant.adapter import AssistantAdapter
from services.assistant.interface import AssistantInterface

class AssistantFactory:
    
    @staticmethod
    def get_assistant(assistant_type: str) -> AssistantInterface:
        if assistant_type == "luna":
            return AssistantAdapter