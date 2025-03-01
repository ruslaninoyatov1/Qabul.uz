from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
from django.contrib.auth import get_user_model
import asyncio

User = get_user_model()
TOKEN = "7408258357:AAF-NDdLcL8g6mhAuc9cU7zHoXOvcV49jAA"


async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = update.effective_user.username

    if not chat_id or not user:
        await update.message.reply_text("Xatolik yuz berdi! Iltimos, qayta urinib ko‘ring.")
        return

    chat_id = str(chat_id)  # Chat ID
    telegram_name = user if user else f"tg_user_{user.id}"

    user_obj, created = await asyncio.to_thread(
        lambda: User.objects.get_or_create(username=user, defaults={"chat_id": chat_id})
    )

    if not created:
        user_obj.chat_id = chat_id
        user_obj.save()

    print(f"User {telegram_name} started the bot. Chat ID: {chat_id}")

    await update.message.reply_text(f"Salom {telegram_name}, sizning chat ID: {chat_id}")


async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

    print("Bot ishga tushdi...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
