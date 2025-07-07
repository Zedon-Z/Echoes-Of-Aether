from storage import database as db

# Simulated power logic (extend with real effects as needed)
def use_power(user_id, target_username):
    user_role = db.get_user_role(user_id)
    target_id = db.get_user_id_by_name(target_username.replace("@", ""))

    if not target_id:
        return "Target not found."

    # Example: Assassin (Veilborn)
    if user_role == "Shadeblade":
        if db.is_player_protected(target_id):
            return "⚠️ Target was protected!"
        db.mark_player_for_death(target_id)
        return f"🗡 You marked @{target_username} for death tonight."

    # Oracle (Luminae)
    if user_role == "Oracle":
        faction = db.get_player_faction(target_id)
        return f"🔮 Oracle's Vision: @{target_username} is part of *{faction}*."

    # Succubus (Veilborn)
    if user_role == "Succubus":
        db.disable_player_next_vote(target_id)
        return f"💋 @{target_username} is seduced and can’t vote tomorrow."

    # Tinkerer (Nexus)
    if user_role == "Tinkerer":
        inv = db.get_inventory(target_id)
        return f"🧪 @{target_username}'s inventory: {', '.join(inv)}"

    return "❌ Your role has no defined power yet."
