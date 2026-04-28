import json, os

LB_FILE = "leaderboard.json"
ST_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": [50, 100, 220],
    "difficulty": "normal"
}

def load_leaderboard():
    if not os.path.exists(LB_FILE):
        return []
    with open(LB_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_leaderboard(lb):
    lb = sorted(lb, key=lambda x: x["score"], reverse=True)[:10]
    with open(LB_FILE, "w", encoding="utf-8") as f:
        json.dump(lb, f, ensure_ascii=False, indent=2)

def add_score(name, score, distance, coins):
    lb = load_leaderboard()
    lb.append({"name": name, "score": score,
                "distance": distance, "coins": coins})
    save_leaderboard(lb)

def load_settings():
    if not os.path.exists(ST_FILE):
        return DEFAULT_SETTINGS.copy()
    with open(ST_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_settings(s):
    with open(ST_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=2)