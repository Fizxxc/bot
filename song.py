import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Logger untuk debugging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Dictionary untuk menyimpan pengguna dalam antrean dan pasangan
waiting_users = []
active_chats = {}

# Fungsi untuk memulai bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Selamat datang di Anonymous Chat!\n\n"
        "Gunakan /search untuk mencari pasangan chat.\n"
        "Gunakan /stop untuk keluar dari obrolan."
    )

# Fungsi untuk mencari pasangan chat
async def search(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id

    if user_id in active_chats:
        await update.message.reply_text("Kamu sudah dalam obrolan! Gunakan /stop untuk keluar.")
        return

    if waiting_users and waiting_users[0] != user_id:
        partner_id = waiting_users.pop(0)
        active_chats[user_id] = partner_id
        active_chats[partner_id] = user_id

        await context.bot.send_message(partner_id, "🎉 Pasangan ditemukan! Kamu sekarang bisa mengobrol.")
        await update.message.reply_text("🎉 Pasangan ditemukan! Kamu sekarang bisa mengobrol.")
    else:
        waiting_users.append(user_id)
        await update.message.reply_text("⏳ Menunggu pasangan...")

# Fungsi untuk mengakhiri obrolan
async def stop(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id

    if user_id in active_chats:
        partner_id = active_chats.pop(user_id)
        active_chats.pop(partner_id, None)

        await context.bot.send_message(partner_id, "🚫 Pasanganmu telah keluar dari obrolan.")
        await update.message.reply_text("🚫 Kamu telah keluar dari obrolan.")
    elif user_id in waiting_users:
        waiting_users.remove(user_id)
        await update.message.reply_text("🚫 Kamu telah keluar dari antrean pencarian.")
    else:
        await update.message.reply_text("❌ Kamu tidak sedang dalam obrolan.")

# Fungsi untuk menangani pesan dan meneruskannya ke pasangan chat
async def message_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id

    if user_id in active_chats:
        partner_id = active_chats[user_id]
        await context.bot.send_message(partner_id, update.message.text)
    else:
        await update.message.reply_text("❌ Kamu tidak sedang dalam obrolan. Gunakan /search untuk mencari pasangan.")

# Fungsi utama untuk menjalankan bot
def main():
    TOKEN = "7604337358:AAFitWVGj2UA3jCJ38ymVDwE12IS9IX3CIo"

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
