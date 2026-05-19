# Utility functions for safe json parsing
import json
from src.logger import logger

def safe_json_parse(text):
    try:
        # sometimes the model adds extra text before/after JSON, extract {...}
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end == -1:
            return None
        return json.loads(text[start:end])
    except Exception as e:
        logger.error("JSON parsing failed: %s", e, exc_info=True)
        logger.debug("Raw output: %s", text)
        return None
