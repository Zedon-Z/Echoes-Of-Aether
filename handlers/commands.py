from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from storage import database as db
from engine import phases
import time 

# Track join message ID to update later
join_message_tracker = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Welcome to *Echoes of Aether: The Silent War*.\n\n"
        "Use /startgame to begin a new game, or /join to join one.",
        parse_mode='Markdown'
    )
join_message_tracker = {}

# ----- START GAME -----
def start_game(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if db.is_game_active(chat_id):
        update.message.reply_text("⚠️ A game is already running!")
        return

    db.start_new_game(chat_id)
    countdown = 60
    db.set_timer(chat_id, countdown)
    context.job_queue.run_once(phases.begin_game, countdown, context=chat_id)
    db.set_game_start_time(chat_id, int(time.time()) + countdown)

    # Static join message (does not change)
    join_btn = [[InlineKeyboardButton("🔹 Join Game", callback_data="join")]]
    context.bot.send_message(
        chat_id=chat_id,
        text="🌀 *Echoes of Aether Begins!*\nClick below to join the match!",
        reply_markup=InlineKeyboardMarkup(join_btn),
        parse_mode='Markdown'
    )

    # Player list message (will be updated)
    player_msg = context.bot.send_message(
        chat_id=chat_id,
        text="📜 *Players Joined:*\n_(Waiting...)_",
        parse_mode='Markdown'
    )
    join_message_tracker[chat_id] = player_msg.message_id


# ----- JOIN GAME -----
def join_game(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = update.effective_user

    if not db.is_game_active(chat_id):
        update.message.reply_text("No game has been started yet.")
        return

    success = db.add_player(chat_id, user.id, user.full_name)
    if not success:
        update.message.reply_text("ℹ️ You're already in the game.")
        return

    # Update the main player list
    players = db.get_player_list(chat_id)
    player_text = "\n".join(f"• {name}" for name in players.values()) or "_Waiting..._"

    try:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=join_message_tracker.get(chat_id),
            text=f"📜 *Players Joined:*\n{player_text}",
            parse_mode='Markdown'
        )
    except:
        pass

    # Send fresh join button for others (without player list)
    end_time = db.get_game_start_time(chat_id)
    seconds_left = max(0, end_time - int(time.time()))
    time_text = f"⏳ Game starts in *{seconds_left} seconds!*"

    join_btn = [[InlineKeyboardButton("🔹 Join Game", callback_data="join")]]
    context.bot.send_message(
        chat_id=chat_id,
        text=f"{user.full_name} joined!\n\n{time_text}",
        reply_markup=InlineKeyboardMarkup(join_btn),
        parse_mode='Markdown'
    )

def extend_time(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if not db.is_game_active(chat_id):
        update.message.reply_text("❌ No active game to extend time for.")
        return

    db.extend_timer(chat_id, 30)  # Extend by 30 seconds (or customize)
    update.message.reply_text("⏳ Extra time added! Waiting for more players...")

def flee(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = update.effective_user

    if not db.is_game_active(chat_id):
        update.message.reply_text("❌ There's no game to flee from.")
        return

    if db.remove_player(chat_id, user.id):
        update.message.reply_text(f"{user.full_name} has left the game.")
    else:
        update.message.reply_text("You’re not part of the game.")

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

def force_start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not db.is_game_active(chat_id):
        update.message.reply_text("❌ No game to start.")
        return

    players = db.get_player_list(chat_id)
    if len(players) < 6:
        update.message.reply_text("⚠️ At least 6 players are needed to start the game.")
        return

    update.message.reply_text("🚀 Game is starting...")
    phases.start_day_phase(chat_id, context)
def get_chat_id(update: Update, context: CallbackContext):
    update.message.reply_text(f"Chat ID: `{update.effective_chat.id}`", parse_mode='Markdown')
    
from config import BOT_OWNER_ID
from storage import authorized

def authorize(update: Update, context: CallbackContext):
    if update.effective_user.id != BOT_OWNER_ID:
        update.message.reply_text("🚫 You are not authorized to do this.")
        return

    chat_id = update.effective_chat.id
    if authorized.add_group(chat_id):
        update.message.reply_text(f"✅ This group ({chat_id}) is now authorized.")
    else:
        update.message.reply_text("ℹ️ This group is already authorized.")

def deauthorize(update: Update, context: CallbackContext):
    if update.effective_user.id != BOT_OWNER_ID:
        update.message.reply_text("🚫 You are not authorized to do this.")
        return

    chat_id = update.effective_chat.id
    if authorized.remove_group(chat_id):
        update.message.reply_text(f"❌ This group ({chat_id}) has been removed from authorized list.")
    else:
        update.message.reply_text("ℹ️ This group wasn't authorized.")
def cancel_game(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if not db.is_game_active(chat_id):
        update.message.reply_text("❌ There’s no active game to cancel.")
        return

    db.cancel_game(chat_id)
    update.message.reply_text("🚫 The game has been *cancelled*. You can /startgame again if you wish.", parse_mode='Markdown')
