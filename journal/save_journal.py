import json
from datetime import datetime

def save_query(query, response):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "response": response
    }
    with open("journal/journal.json", "a") as f:
        f.write(json.dumps(entry) + "\n")
