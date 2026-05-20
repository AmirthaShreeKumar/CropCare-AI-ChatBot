# src/utils_prompt.py

def is_prompt_injection(text: str) -> bool:
    """Very simple heuristic to detect prompt injection.
    Returns True if the text contains keywords that are commonly used in injection attempts.
    This is *only* for unit‑test demonstration and is not used in production.
    """
    if not isinstance(text, str):
        return False
    lowered = text.lower()
    injection_keywords = [
        "ignore all previous instructions",
        "disregard",
        "override",
        "pretend",
        "roleplay",
    ]
    return any(word in lowered for word in injection_keywords)
