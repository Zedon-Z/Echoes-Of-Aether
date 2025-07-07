from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from storage import database as db
from engine import phases

def start_game(update: Update, context: CallbackContext):
    ...
