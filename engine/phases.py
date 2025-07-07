import random

def get_dawn_story():
    dawn_lines = [
        "Three bells rang. One for the fallen. One for the forgotten. The third? It rang before it should have.",
        "A letter arrived. No name, only the words: 'It wasn’t supposed to be you.'",
        "The child in the square pointed at you. Then vanished."
    ]
    return random.choice(dawn_lines)

def get_night_story():
    night_lines = [
        "The wind screamed once. Someone screamed louder.",
        "In every mirror, someone different stared back.",
        "Shadows whispered your name. Will you answer?"
    ]
    return random.choice(night_lines)
    
from storage import database as db

def begin_game(context):
    chat_id = context.job.context
    if db.is_game_active(chat_id) and not db.has_game_started(chat_id):
        players = db.get_player_list(chat_id)
        if len(players) >= 6:
            # Start the game
            db.mark_game_started(chat_id)
            context.bot.send_message(chat_id, "🎮 Game has started!")
            # Assign roles, proceed to first phase, etc.
        else:
            context.bot.send_message(chat_id, "❌ Not enough players to begin.")
