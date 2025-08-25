import json
import os

def save_cache(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_cache(filename, default):
    if not os.path.exists(filename):
        return default
    if os.path.getsize(filename) == 0:
        return default
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
