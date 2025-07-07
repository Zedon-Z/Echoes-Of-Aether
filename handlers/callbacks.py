from telegram import Update
from telegram.ext import CallbackContext
from storage import database as db
from engine import tasks, win

def handle_callback(update: Update, context: CallbackContext):
    ...
