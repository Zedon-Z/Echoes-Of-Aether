from telegram import Update
from telegram.ext import CallbackContext
from storage import database as db
from engine import roles, tasks, inventory

def handle_dm(update: Update, context: CallbackContext):
    ...
