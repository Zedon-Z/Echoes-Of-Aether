from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import os
from threading import Thread
from handlers import commands, callbacks, game, dm
from config import TOKEN

def run_bot():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", commands.start))
    dp.add_handler(CommandHandler("startgame", commands.start_game))
    dp.add_handler(CommandHandler("join", commands.join_game))
    dp.add_handler(CommandHandler("vote", commands.vote))
    dp.add_handler(CommandHandler("phase", game.phase))
    dp.add_handler(CallbackQueryHandler(callbacks.handle_callback))
    dp.add_handler(MessageHandler(Filters.private & Filters.text, dm.handle_dm))

    PORT = int(os.environ.get("PORT", 8443))
    APP_URL = os.environ.get("APP_URL")

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{APP_URL}/{TOKEN}"
    )

    updater.idle()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    import server  # Runs the Flask app to expose port
