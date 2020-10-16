import sqlite3

class SQL():
    """
    База данных

    Содержит запросы к бд и логику отправки сообщений
    """
    def __init__(self, dbName, tableName):
        self.dbName = dbName
        self.tableName = tableName

        print("Создан объект SQL")

    def create_connection(self):
        """
        Создание коннекта с бд
        """
        self.conn = sqlite3.connect(self.dbName, check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS %s (user_id TEXT, user_id_to TEXT, message TEXT DEFAULT '', current TEXT DEFAULT '', network TEXT)" %self.tableName)
        self.conn.commit()


    def create_user(self, userId):
        print("Чат начал юзер -", userId)
    #    self.cur.execute("INSERT INTO %s (user_id) VALUES (%s)" %(self.tableName, userId))


    def update_user_relations(self, userId, userIdTo, network):
        """
        Вставка новой строки с юзером и адресатом из написанного им сообщения
        """
        print("Пользователь", userId, "начал диалог с", userIdTo)

        self._update_current(userId)
        if self._check_user_relations(userId, userIdTo):
            self.cur.execute("UPDATE %s SET current = ? WHERE user_id = ? AND user_id_to = ?" %self.tableName, ("1", userId, userIdTo))
        else:
            self.cur.execute("INSERT INTO %s (user_id, user_id_to, current, network) VALUES (?, ?, ?, ?)" %self.tableName, (userId, userIdTo, "1", network))
        self.conn.commit()


    def _check_user_relations(self, userId, userIdTo):
        """
        Проверка наличия уже существующей связи юзера с адресатом
        """
        answer = self.cur.execute("SELECT user_id FROM %s WHERE user_id = ? AND user_id_to = ?" %self.tableName, (userId, userIdTo)).fetchone()
        print(answer)
        if answer:
            return True
        return False


    def _update_message(self, userId, message):     # UserId - массив с userid
        """
        Обновление ячейки сообщения юзера
        """
        arguments = ",".join(["?"] * len(userId))
        # print(userId, arguments)
        self.cur.execute("UPDATE %s SET message = ? WHERE user_id IN (%s) AND current = ?" %(self.tableName, arguments), (message, *userId, "1"))
        self.conn.commit()


    def _select_message(self, userId):
        """
        Получение ячейки сообщения, которое отправлено и еще не было удалено
        """
        return self.cur.execute("SELECT message FROM %s WHERE user_id = ? AND current = ?" %self.tableName, (userId, "1")).fetchone()


    def add_message(self, userId, message):
        """
        Приплюсовывание нового сообщения к ячейке, дабы за время обновления запроса не потерять предыдущее
        """
        print("Получено сообщение:", message, "от:", userId)

        messageOld = self._select_message(userId)
        print(messageOld)

        if messageOld:
            if messageOld[0]:
                messageOld = (messageOld[0] + "\n\n", )
            self._update_message([userId], messageOld[0] + message)
    

    def get_message(self, network):
        """
        Получение сообщений запросом из строки, где юзер является адресатом

        Затем обнуление этой ячейки
        """
        values = self._select_message_from_user_id_to(network)
        # print(values)
        answer = list(filter(self._check_current, values))
        self._update_message([arr[1] for arr in answer], '')
        return answer


    def _select_message_from_user_id_to(self, network):
        """
        Выборка id адресата, id юзера и сообщения от всех активных пользователей
        """
        return self.cur.execute("SELECT user_id_to, user_id, message FROM %s WHERE message != ? AND current = ? AND network = ?" %self.tableName, ("", "1", network)).fetchall()


    def _check_current(self, value):
        """
        Проверка на актуальность чата
        """
        # print(value)
        answer = self.cur.execute("SELECT user_id FROM %s WHERE user_id = ? AND user_id_to = ? AND current = ?" %self.tableName, (value[0], value[1], "1")).fetchone()
        # print(answer)
        if answer:
            return True
        return False


    def select_user_id_to(self, userId):
        """
        Выборка id текущего адресата, установленного юзером
        """
        answer = self.cur.execute("SELECT user_id_to FROM %s WHERE user_id = ? AND current = ?" %self.tableName, (userId, "1")).fetchone()[0]
        return answer


    def _update_current(self, userId):
        """
        Сброс всех полей адресатов юзера для установки нового
        """
        self.cur.execute("UPDATE %s SET current = ? WHERE user_id = ?" %self.tableName, ("", userId))
        self.conn.commit()


    def close_connection(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()