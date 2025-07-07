from telegram import Update
from telegram.ext import CallbackContext
from storage import database as db
from engine import roles, tasks, inventory

def handle_dm(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Command to list tasks
    if text == "/mytasks":
        task_list = tasks.get_user_tasks(user_id)
        update.message.reply_text(task_list)

    elif text.startswith("/complete_task"):
        _, code = text.split(maxsplit=1)
        result = tasks.submit_task(user_id, code)
        update.message.reply_text(result)

    elif text == "/abandon_task":
        result = tasks.abandon_task(user_id)
        update.message.reply_text(result)

    # Powers
    elif text.startswith("/usepower"):
        parts = text.split()
        if len(parts) < 2:
            update.message.reply_text("Usage: /usepower @username")
            return
        target_username = parts[1]
        result = roles.use_power(user_id, target_username)
        update.message.reply_text(result)

    # Inventory usage
    elif text.startswith("/useitem"):
        parts = text.split()
        if len(parts) < 2:
            update.message.reply_text("Usage: /useitem item_name")
            return
        item = parts[1]
        result = inventory.use_item(user_id, item)
        update.message.reply_text(result)

    else:
        update.message.reply_text("Unknown command. Try /mytasks or /usepower.")
