        


import datetime
from services.assistant.interface import AssistantInterface


class AssistantAdapter(AssistantInterface):
    def today():
        return f"Agora são {datetime.datetime.now().strftime('%d de %B de %Y, %I:%M %p')}"
        
    def who():
        return f"Fui criada por um grupo de desenvolvedores do IFRN. Eles se chamam: Lucas, Renan e Vitor."
            

            
        
            
