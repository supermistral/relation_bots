import vk_api, config, threading
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_handler import VKbot

def msg(user_id, Message):
    vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=Message)
    
def process(target):
    try:
        thread = threading.Thread(target=target)
        thread.start()
    except Exception as err:
        print(err)
        print()

vk_sess = vk_api.VkApi(token=config.tokenVk)
vk = vk_sess.get_api()
longpoll = VkLongPoll(vk_sess)

vkbot = VKbot(vk.messages.send)
process(vkbot.process)

for event in longpoll.listen():
    print(event)
    print(1)

    if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me and event.from_user:
        text = event.text
        print(text)
        # ОБРАБОТЧИК 
        message = vkbot.command(event.user_id, event.text)
        print(message)
        '''for j in mess:
            try: 
                msg(event.user_id, j)
            except Exception as err:
                print(err)'''
        try:
            if message:
                msg(event.user_id, message)
        except Exception as err:
            print("ERROR")
            print(err)