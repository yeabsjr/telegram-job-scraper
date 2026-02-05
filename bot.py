import os
import asyncio
import datetime
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# ===================== TELEGRAM CONFIG =====================
API_ID = int(os.getenv("API_ID")) 
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "job_scraper_session"

CHANNELS = [
    "freelance_ethio",
    "geezjobs_ethiopia",
    "sabijobs"
]

# ===================== KEYWORDS ============================
KEYWORDS = [
    "marketing", "digital marketing", "social media",
    "social media manager", "content creator",
    "content writer", "graphic design",
    "video editor", "branding", "seo",
    "facebook ads", "tiktok", "host"
]

# ===================== CLIENT ==============================
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ===================== HELPERS =============================
def contains_keyword(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in KEYWORDS)


def format_message(msg):
    post_date = msg.date.strftime("%Y-%m-%d")
    source = f"@{msg.chat.username}" if msg.chat and msg.chat.username else "Unknown"

    return (
        f"📅 Posted on: {post_date}\n"
        f"📢 Source: {source}\n\n"
        f"{msg.text}"
    )


async def safe_send(text):
    try:
        await client.send_message("me", text)
        await asyncio.sleep(3)  # rate limit

    except FloodWaitError as e:
        wait_time = e.seconds + 5
        print(f"⏳ FloodWait hit. Sleeping for {wait_time} seconds...")
        await asyncio.sleep(wait_time)
        await client.send_message("me", text)
        await asyncio.sleep(3)

# ===================== LIVE HANDLER ========================
@client.on(events.NewMessage(chats=CHANNELS))
async def live_handler(event):
    if not event.raw_text:
        return

    if not contains_keyword(event.raw_text):
        return

    formatted = format_message(event.message)
    await safe_send(formatted)
    print("✔ Live post forwarded")

# ===================== HISTORY (LAST 5 DAYS) ===============
async def scrape_last_7_days():
    print("🔍 Scraping last 7 days...")
    since = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)

    for channel in CHANNELS:
        print(f"📂 Channel: {channel}")

        async for msg in client.iter_messages(channel, offset_date=since):
            if not msg.text:
                continue

            if not contains_keyword(msg.text):
                continue

            formatted = format_message(msg)
            await safe_send(formatted)
            print("✔ Old post forwarded safely")

# ===================== MAIN ================================
async def main():
    await client.start()
    print("🤖 Bot is running...")

    # One-time history scrape
    await scrape_last_7_days()

    print("📡 Listening for live posts...")
    await client.run_until_disconnected()

# ===================== ENTRY POINT =========================
while True:
    try:
        asyncio.run(main())
    except Exception as e:
        print("Crash:", e)
        time.sleep(10)

