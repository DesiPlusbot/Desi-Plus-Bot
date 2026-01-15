from pyrogram import Client, filters
from pymongo import MongoClient

# ===== CREDENTIALS =====
BOT_TOKEN = "7837426350:AAGhNIlKZ4f7Q2_qtEHtyEm6W9hclFaF5G4"
API_ID = 27641128
API_HASH = "6770e69b357624d73e8ce64de1cdadd8"

MONGO_URL = "mongodb+srv://DesiPlusBot:<db_password>@cluster0.ufj5mpz.mongodb.net/?appName=Cluster0"

# ===== DATABASE =====
mongo = MongoClient(MONGO_URL)
db = mongo["telegram_bot"]
users = db["users"]

# ===== BOT =====
app = Client(
    "DesiPlusBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    uid = message.from_user.id
    if not users.find_one({"_id": uid}):
        users.insert_one({
            "_id": uid,
            "name": message.from_user.first_name
        })

    await message.reply_text(
        "✅ Bot successfully start ho gaya!\n💾 MongoDB connected"
    )

print("🤖 Bot Running...")
app.run()
