from utils import SQL
import config, time
from vk_api.utils import get_random_id


class InteractionSQL():
    """
    Взаимодействие с БД для ботов
    """
    def __init__(self):
        self.sql = SQL(config.database, config.tableName)
        self.sql.create_connection()
        self.sql.create_table()


    def start_message(self, userId):
        self.sql.create_user(userId)
        return Message_From_SQL.message("start")


    def update_user(self, userId, text, network):
        self.sql.update_user_relations(userId, text, network)
        return Message_From_SQL.message("update")


    def get_text_message(self, userId, text):
        self.sql.add_message(userId, text)


    def process(self, sendMessage, cond=False, **kwargs):
        # kwargs["bot"]
        while True:
            userMessages = self.sql.get_message(kwargs["network"])
            print(userMessages)

            for message in userMessages:
                print("Юзер", message[1], "отправил сообщение", message[0])

                if cond:
                    sendMessage(user_id=message[0], message=message[2], random_id=get_random_id())
                else:
                    sendMessage(message[0], message[2])

            time.sleep(3)


class Message_From_SQL():
    """
    Отправка сообщений исходя из запрашиваемой функции для ботов
    """
    @staticmethod
    def message(text):
        if text == "start":
            return "Вы зарегистрированы у бота!"
        elif text == "update":
            return "Вы начали диалог с этим пользователем"