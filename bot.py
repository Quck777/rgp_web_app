from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = '7630385568:AAFVvV1sFRe9tmMln9eO42cQIcgt77NrPAc'
WEBAPP_URL = 'https://rgp-web-app.onrender.com'  # твой адрес

def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton(text="🎮 Играть в RPG", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Нажми кнопку ниже, чтобы открыть игру:", reply_markup=reply_markup)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()
    print("Бот запущен")
    updater.idle()

if __name__ == '__main__':
    main()
