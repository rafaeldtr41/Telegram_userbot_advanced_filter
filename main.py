from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
from Input_Configuration.orders import Interpreter, List_Recipent, List_Chat_Syncro, List_Chat
from asgiref.sync import sync_to_async
from Input_Configuration.filter import Filter
import asyncio



#To catch error messages
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
#Load .env
load_dotenv()
#Basic Login
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
user_id = os.getenv('USER_ARROBA')
client = TelegramClient(user_id, api_id, api_hash)


REGEXES = {
    "order": r'^order *',
    
    }


@client.on(events.NewMessage(chats="me"))
async def get_order(event):

    message = await Interpreter(event.raw_text)
    await event.reply(message)

@client.on(events.NewMessage(chats=List_Chat_Syncro()))
async def apply_filter(event):

    chats = await List_Chat()
    if len(chats) != 0:

        state = await Filter(event.raw_text)
        if state:

            recipents = await List_Recipent()
            if len(recipents) == 0 :

                await client.forward_messages('me', event.message)
            else:
                
                for i in recipents:

                    try:
                        await client.forward_messages(i.chat_name, event.message)
                    except ValueError:
                        await client.send_message("me", "Error, entidad " + i.chat_name + " desconocida")

client.start()
client.run_until_disconnected()
