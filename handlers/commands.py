from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from storage import database as db
from engine import phases
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Welcome to *Echoes of Aether: The Silent War*.\n\n"
        "Use /startgame to begin a new game, or /join to join one.",
        parse_mode='Markdown'
    )

def start_game(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if db.is_game_active(chat_id):
        update.message.reply_text("A game is already running!")
        return

    db.start_new_game(chat_id)
    join_btn = [[InlineKeyboardButton("Join Game", callback_data="join")]]
    update.message.reply_text(
        "🌀 *Echoes of Aether Begins!*\nClick below to join the match.",
        reply_markup=InlineKeyboardMarkup(join_btn),
        parse_mode='Markdown'
    )

def join_game(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = update.effective_user

    if not db.is_game_active(chat_id):
        update.message.reply_text("No game has been started yet.")
        return

    success = db.add_player(chat_id, user.id, user.full_name)
    if success:
        update.message.reply_text(f"{user.full_name} has joined the game.")
    else:
        update.message.reply_text("You’re already in the game.")

def vote(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not db.is_game_active(chat_id):
        update.message.reply_text("No game in progress.")
        return

    players = db.get_player_list(chat_id)
    if not players:
        update.message.reply_text("No players found.")
        return

    buttons = [
        [InlineKeyboardButton(name, callback_data=f"vote_{pid}")]
        for pid, name in players.items()
    ]
    update.message.reply_text("🔍 *Vote for a suspect:*", reply_markup=InlineKeyboardMarkup(buttons), parse_mode='Markdown')
