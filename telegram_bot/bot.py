from telegram.ext import Updater, CommandHandler

TOKEN = "7630385568:AAFVvV1sFRe9tmMln9eO42cQIcgt77NrPAc"

def start(update, context):
    update.message.reply_text("Добро пожаловать в RPG! Перейди по ссылке: http://localhost:8000")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))

updater.start_polling()
updater.idle()
