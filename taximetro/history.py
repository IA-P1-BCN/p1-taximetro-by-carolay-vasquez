import json
import logging
import os
 
logger = logging.getLogger(__name__)
 
HISTORY_FILE = "history.json"
 
 
def load() -> list:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        logger.error("Could not read history file: %s", exc)
        return []


def save(ride_record: dict):
    history = load()
    history.append(ride_record)
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except OSError as exc:
        logger.error("Could not write history file: %s", exc)
    else:
        logger.info("Ride saved to history: %s", ride_record)
