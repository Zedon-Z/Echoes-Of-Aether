import sys
print("Python version:", sys.version)
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from handlers import commands, callbacks, game, dm
from config import TOKEN

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("startgame", commands.start_game))
    dp.add_handler(CommandHandler("join", commands.join_game))
    dp.add_handler(CommandHandler("vote", commands.vote))
    dp.add_handler(CommandHandler("phase", game.phase))

    dp.add_handler(CallbackQueryHandler(callbacks.handle_callback))
    dp.add_handler(MessageHandler(Filters.private & Filters.text, dm.handle_dm))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
