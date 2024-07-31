from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv
import asyncio
import config


# Replace these with your own values
api_id = config.api_id
api_hash = config.api_hash
phone_number = config.phone_number

async def main():
    client = TelegramClient('session', api_id, api_hash)
    await client.start(phone=phone_number)

    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    # result = await client(GetDialogsRequest(
    #     offset_date=last_date,
    #     offset_id=0,
    #     offset_peer=InputPeerEmpty(),
    #     limit=chunk_size,
    #     hash=0
    # ))
    # chats.extend(result.chats)

    # for chat in chats:
    #     try:
    #         if chat.megagroup == True:
    #             groups.append(chat)
    #     except:
    #         continue

    async for dialog in client.iter_dialogs():
        if dialog.is_user:
            chats.append(dialog)
        
    for chat in chats:
        groups.append(chat)
    

    print('Choose a group to scrape messages from:')
    for i, g in enumerate(groups):
        print(f'{i}. {g.title}')

    g_index = input("Enter a number: ")
    target_group = groups[int(g_index)]

    print('Fetching Messages...')
    all_messages = []
    user_dict = {}

    async for message in client.iter_messages(target_group, limit=None):
        if message.sender_id:
            if message.sender_id not in user_dict:
                sender = await client.get_entity(message.sender_id)
                if hasattr(sender, 'first_name'):
                    user_dict[message.sender_id] = f"{sender.first_name} {sender.last_name if sender.last_name else ''}"
                else:
                    user_dict[message.sender_id] = f"User {message.sender_id}"
            
            sender_name = user_dict[message.sender_id]
            all_messages.append([sender_name, message.text, str(message.date)])

    print('Saving in CSV...')
    with open("telegram_messages.csv", "w", encoding='UTF-8', newline='') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['sender_name', 'message', 'date'])
        writer.writerows(all_messages)

    print('Messages saved to telegram_messages.csv')

    await client.disconnect()

asyncio.run(main())
