import os
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")

client = TelegramClient("job_scraper_session", api_id, api_hash)

WATCHED_CHANNELS = [
    "@freelance_ethio",
    "@sabijobs",
    "@hahujobs",
    "@geezjobs_ethiopia"
]

KEYWORDS = [
    "marketing",
    "digital marketing",
    "editing",
    "graphics design",
    "graphic designer",
    "social media",
    "social media manager",
]


@client.on(events.NewMessage(chats=WATCHED_CHANNELS))
async def job_handler(event):
    text = event.raw_text.lower()
    if any(keyword in text for keyword in KEYWORDS):
        await client.send_message("me", f"🔔 NEW JOB POST:\n\n{text}")


async def main():
    await client.start(bot_token=bot_token)
    print("Bot started successfully! Listening for job posts...")
    await client.run_until_disconnected()


asyncio.run(main())

