from telegram import Update
from telegram.ext import CallbackContext
from engine import phases
from storage import database as db

def phase(update: Update, context: CallbackContext):
    ...
