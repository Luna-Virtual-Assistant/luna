from abc import ABC, abstractmethod


class AssistantInterface(ABC):
    @abstractmethod
    def today(self):
        pass
    
    @abstractmethod
    def who(self):
        pass
    
    