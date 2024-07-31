from telethon import TelegramClient, events
import asyncio

# Replace these with your own values
api_id = '29276106'
api_hash = 'a90d5723270e13dfe3dd2550cd7b380c'
phone_number = '+79259616710'

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.reply('Hello! This is an automated response.')

@client.on(events.NewMessage)
async def echo_all(event):
    await event.reply(event.text)

async def main():
    await client.start(phone=phone_number)
    print("Client Created")
    await client.run_until_disconnected()

asyncio.run(main())

