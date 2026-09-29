import json
import logging
import os
 
logger = logging.getLogger(__name__)
 
_DEFAULT_RATE_STOPPED = 0.02
_DEFAULT_RATE_MOVING = 0.05
_RATES_FILE = os.path.join(
    os.path.dirname(__file__), "..", "config", "rates.json"
)
 
 
def _load_rates():
    try:
        with open(_RATES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return float(data["stopped"]), float(data["moving"])
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        logger.error(
            "Could not load rates from %s (%s). Falling back to default rates.",
            _RATES_FILE, exc,
        )
        return _DEFAULT_RATE_STOPPED, _DEFAULT_RATE_MOVING
 
 
RATE_STOPPED, RATE_MOVING = _load_rates()

