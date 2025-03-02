# from telegram import Update
# from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
# from django.contrib.auth import get_user_model
# from asgiref.sync import sync_to_async
# import asyncio
# from .tasks import save_chat_id_task
#
# User = get_user_model()
# TOKEN = "7408258357:AAF-NDdLcL8g6mhAuc9cU7zHoXOvcV49jAA"
#
#
# async def start(update: Update, context: CallbackContext):
#     chat_id = update.effective_chat.id
#     user = update.effective_user.username
#
#     if not chat_id or not user:
#         await update.message.reply_text("Xatolik yuz berdi! Iltimos, qayta urinib ko‘ring.")
#         return
#
#     chat_id = str(chat_id)  # Chat ID
#     telegram_name = user if user else f"tg_user_{chat_id}"
#
#     # Foydalanuvchini username orqali topish yoki yaratish
#     user_obj, created = await sync_to_async(User.objects.get_or_create)(
#         username=user,
#         defaults={"chat_id": chat_id, "telegram_name": telegram_name}
#     )
#
#     if not created:
#         user_obj.chat_id = chat_id
#         user_obj.telegram_name = telegram_name
#         await sync_to_async(user_obj.save)()
#
#     print(f"User {telegram_name} started the bot. Chat ID: {chat_id}")
#
#     await update.message.reply_text(f"Salom {telegram_name}, sizning chat ID: {chat_id}")
#
#
# async def handle_message(update: Update, context: CallbackContext):
#     chat_id = update.effective_chat.id
#     user = update.effective_user.username
#
#     if not chat_id or not user:
#         await update.message.reply_text("Xatolik yuz berdi! Iltimos, qayta urinib ko‘ring.")
#         return
#
#     chat_id = str(chat_id)
#     # telegram_name = user if user else f"tg_user_{chat_id}"
#     user = f"@{user}"
#
#     user_obj = await sync_to_async(User.objects.filter(telegram_name=user).first)()
#     if user_obj:
#         # Celery orqali chat_id ni saqlash
#         save_chat_id_task.delay(user_obj.id, chat_id)
#         await update.message.reply_text(f"Sizning chat ID ({chat_id}) saqlandi.")
#     else:
#         await update.message.reply_text("Siz ro'yxatdan o'tmagansiz!")
#
#
# async def main():
#     app = Application.builder().token(TOKEN).build()
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
#
#     print("Bot ishga tushdi...")
#     await app.run_polling()
#
# if __name__ == "__main__":
#     asyncio.run(main())
#
