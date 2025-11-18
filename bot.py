import os
from dotenv import load_dotenv
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")


# Channels to monitor (public channels you do NOT own)
CHANNELS = [
    "ahujobs",
    "sabi_jobs",
    "geez_jobs_ethiopia"
]

# Keywords (optional)
KEYWORDS = ["job", "hiring", "vacancy", "apply", "position"]

client = TelegramClient("job_scraper_session", API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNELS))
async def forwarder(event):
    text = event.raw_text.lower()

    if any(k in text for k in KEYWORDS):
        me = await client.get_me()

        # Forward message to your Saved Messages
        await client.forward_messages(me.id, event.message)

async def main():
    print("Starting user-client job scraper...")
    await client.start()   # LOGIN AS USER WITH PHONE NUMBER (ONLY FIRST TIME LOCALLY)
    await client.run_until_disconnected()

client.loop.run_until_complete(main())


