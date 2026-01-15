import os
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===== ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SHORTNER_LINK = os.getenv("SHORTNER_LINK")

# ===== SETTINGS =====
VERIFY_TIME = 86400   # 24 hour
DELETE_TIME = 300     # 5 minute

verified_users = {}   # simple memory (Mongo later add kar sakte ho)

app = Client(
    "desi_plus_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

def is_verified(user_id):
    if user_id not in verified_users:
        return False
    return time.time() - verified_users[user_id] < VERIFY_TIME

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    if not is_verified(message.from_user.id):
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Verify Now", url=SHORTNER_LINK)],
            [InlineKeyboardButton("✅ I Have Verified", callback_data="verified")]
        ])
        await message.reply_text(
            "🔐 Verification Required\n\n"
            "Aapko 24 hour me sirf 1 baar verify karna hoga.",
            reply_markup=buttons
        )
    else:
        await message.reply_text("✅ Aap verified ho. File ka naam bhejo.")

@app.on_callback_query(filters.regex("verified"))
async def verified(client, query):
    verified_users[query.from_user.id] = time.time()
    await query.message.edit_text(
        "✅ Verification Successful\n"
        "24 ghante ke liye access unlock ho gaya 🎉"
    )

@app.on_message(filters.private & filters.text)
async def send_file(client, message):
    if not is_verified(message.from_user.id):
        await message.reply_text("❌ Pehle verify karo /start se")
        return

    warn = await message.reply_text(
        "⚠️ Important Notice\n\n"
        "Ye file sirf 5 minute ke liye available hai.\n"
        "5 minute baad auto delete ho jayegi.\n\n"
        "📥 Jaldi download karo"
    )

    file_msg = await client.send_message(
        message.chat.id,
        "📂 (Yahan file send logic add hoga)"
    )

    await asyncio.sleep(DELETE_TIME)

    try:
        await warn.delete()
        await file_msg.delete()
    except:
        pass

app.run()
