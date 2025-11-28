import os
import random
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from datetime import time
import pytz

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN")

WISHES = [
    "Пусть утро принесёт тебе только радость!",
    "Желаю лёгкого и успешного дня!",
    "Пусть сегодня все двери будут открыты!",
    "Удача уже идёт к тебе навстречу!",
    "Пусть этот день будет лучше, чем вчера!",
    "Желаю энергии и вдохновения!",
    "Пусть сегодня случится что-то приятное!",
    "Хорошего настроения на весь день!",
    "Пусть всё получится!",
    "Солнечного настроения тебе!",
] * 10  # 100 пожеланий

subscribers = set()

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    subscribers.add(chat_id)
    keyboard = [[InlineKeyboardButton("🌟 ПОЖЕЛАТЬ", callback_data="wish")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Привет! Я твой утренний бот 😊\n\n"
        "Каждое утро в 08:00 я буду присылать новое пожелание.\n"
        "Хочешь прямо сейчас? Жми кнопку!",
        reply_markup=reply_markup
    )

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "wish":
        wish = random.choice(WISHES)
        query.edit_message_text(f"✨ {wish}")

def morning_wish(context: CallbackContext):
    for chat_id in subscribers:
        wish = random.choice(WISHES)
        try:
            context.bot.send_message(chat_id=chat_id, text=f"☀️ Доброе утро!\n\n{wish}")
        except Exception as e:
            logging.error(f"Ошибка отправки пожелания: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    tz = pytz.timezone("Europe/Kiev")
    updater.job_queue.run_daily(morning_wish, time=time(hour=8, minute=0, tzinfo=tz))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
