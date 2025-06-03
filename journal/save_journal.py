import json
from datetime import datetime

def save_query(query, response, emotion="😊"):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "response": response,
        "emotion": emotion
    }
    with open("journal/journal.json", "a") as f:
        f.write(json.dumps(entry) + "\n")
