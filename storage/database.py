# NOTE: For production, replace this with persistent DB

games = {}

def is_game_active(chat_id):
    return chat_id in games

def start_new_game(chat_id):
    games[chat_id] = {
        "phase": "day",
        "players": {},
        "votes": {},
        "deaths": [],
    }

def set_phase(chat_id, phase):
    games[chat_id]["phase"] = phase

def get_phase(chat_id):
    return games[chat_id].get("phase", "day")

def add_player(chat_id, user_id, username):
    if user_id in games[chat_id]["players"]:
        return False
    games[chat_id]["players"][user_id] = {
        "name": username,
        "alive": True,
        "faction": None,
        "role": None,
        "inventory": [],
        "tasks": [],
    }
    return True

def get_player_list(chat_id):
    return {
        uid: data["name"]
        for uid, data in games[chat_id]["players"].items()
        if data["alive"]
    }

def cast_vote(chat_id, voter_id, target_id):
    games[chat_id]["votes"][voter_id] = target_id

def get_user_role(user_id):
    for game in games.values():
        if user_id in game["players"]:
            return game["players"][user_id].get("role")
    return None

def get_player_faction(user_id):
    for game in games.values():
        if user_id in game["players"]:
            return game["players"][user_id].get("faction")
    return "Unknown"

def get_user_id_by_name(name):
    for game in games.values():
        for uid, data in game["players"].items():
            if data["name"] == name.replace("@", ""):
                return uid
    return None

def disable_player_next_vote(user_id):
    for game in games.values():
        if user_id in game["players"]:
            game["players"][user_id]["vote_disabled"] = True

def mark_player_for_death(user_id):
    for game in games.values():
        game["deaths"].append(user_id)

def is_player_protected(user_id):
    # Stub: you could expand this with protection logic
    return False

def get_inventory(user_id):
    for game in games.values():
        if user_id in game["players"]:
            return game["players"][user_id]["inventory"]
    return []

def remove_item(user_id, item):
    inv = get_inventory(user_id)
    if item in inv:
        inv.remove(item)

def grant_immunity(user_id):
    for game in games.values():
        if user_id in game["players"]:
            game["players"][user_id]["immune"] = True

def get_tasks(user_id):
    for game in games.values():
        if user_id in game["players"]:
            return game["players"][user_id]["tasks"]
    return []

def complete_task(user_id, task):
    for game in games.values():
        if user_id in game["players"]:
            game["players"][user_id]["tasks"].remove(task)
            game["players"][user_id]["inventory"].append("relic")  # Example reward

def abandon_current_task(user_id):
    for game in games.values():
        if user_id in game["players"] and game["players"][user_id]["tasks"]:
            game["players"][user_id]["tasks"].clear()
            return True
    return False

def reveal_all_roles():
    reveal = []
    for game in games.values():
        for uid, data in game["players"].items():
            reveal.append(f"@{data['name']}: {data['role']}")
    return reveal

def get_alive_players(chat_id):
    return [
        uid for uid, data in games[chat_id]["players"].items()
        if data["alive"]
    ]

def get_username(user_id):
    for game in games.values():
        if user_id in game["players"]:
            return game["players"][user_id]["name"]
    return "Unknown"

def get_relic_count(user_id):
    inv = get_inventory(user_id)
    return inv.count("relic")

def used_thread(user_id):
    # Stub: implement tracking thread usage
    return False

def check_nexus_control(user_id):
    # Stub: check if Nexus has met win requirements
    return True

def set_nexus_winner(user_id):
    # Stub: could broadcast win or end game
    pass

def trigger_goat_prophecy():
    # Stub for future expansion
    pass

def set_game_start_time(chat_id, timestamp):
    game_start_times[chat_id] = timestamp

def get_game_start_time(chat_id):
    return game_start_times.get(chat_id, int(time.time()))
    

def set_timer(chat_id, seconds):
    timers[chat_id] = seconds

def extend_timer(chat_id, seconds):
    if chat_id in timers:
        timers[chat_id] += seconds

def get_timer(chat_id):
    return timers.get(chat_id, 0)
    
def cancel_game(chat_id):
    games.pop(chat_id, None)
    player_data.pop(chat_id, None)
    game_start_times.pop(chat_id, None)

# Inside storage/database.py
 # Your in-memory storage

def remove_player(chat_id, user_id):
    if chat_id in game_sessions and user_id in game_sessions[chat_id]["players"]:
        del game_sessions[chat_id]["players"][user_id]
        return True
    return False
