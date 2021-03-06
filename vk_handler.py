from interaction_sql import InteractionSQL
from vk_api.utils import get_random_id

class VKbot(InteractionSQL):
    """
    Обработчик сообщений для ВК
    
    Использует класс взаимодействия с SQL - накладывается поверх него с целью определения методов под ВК
    """
    def __init__(self, target):
        super().__init__()
        self.target = target


    def command(self, userId, message):
        if message.lower() == "/start":
            return self.start_message(userId)
        elif message[:6].lower() == "/user ":
            print("12345")
            return self.update_user(userId, message[6:], "Telegram")    # ИНИЦИАЛИЗАТОР СЕТИ АДРЕСАТА
        else:
            self.get_text_message(userId, message)
            return ""

    
    def process(self):
        super().process(self.target, True, network="VK")    # ИНИЦИАЛИЗАТОР СЕТИ