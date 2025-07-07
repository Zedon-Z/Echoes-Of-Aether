from storage import database as db

def get_user_tasks(user_id):
    tasks = db.get_tasks(user_id)
    if not tasks:
        return "📭 You have no active tasks."
    return "🧾 Your Tasks:\n" + "\n".join(f"• {t['description']}" for t in tasks)

def submit_task(user_id, code):
    tasks = db.get_tasks(user_id)
    for task in tasks:
        if task['code'] == code:
            db.complete_task(user_id, task)
            return "✅ Task completed!"
    return "❌ Invalid or expired task code."

def abandon_task(user_id):
    success = db.abandon_current_task(user_id)
    return "⚠️ Task abandoned." if success else "You have no task to abandon."
