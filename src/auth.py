from src.config import settings
from src.logger import logger
from db import authenticate_user as db_authenticate_user, create_user as db_create_user


class AuthError(ValueError):
    pass


def login_user(username: str, password: str):
    if not username or not password:
        logger.warning("Login attempt with empty username or password")
        return None

    user_info = db_authenticate_user(username, password)
    if not user_info:
        logger.warning("Failed login attempt for user '%s'", username)
        return None

    if isinstance(user_info, dict) and "id" in user_info:
        logger.info("User '%s' authenticated successfully", username)
        return user_info

    if isinstance(user_info, (list, tuple)) and len(user_info) >= 2:
        try:
            normalized = {"id": user_info[0], "role": user_info[1]}
            logger.warning("Normalized non-dict auth response for user '%s'", username)
            return normalized
        except Exception as exc:
            logger.error("Unable to normalize auth response: %s", exc, exc_info=True)
            return None

    logger.error("Unexpected auth payload for user '%s': %r", username, user_info)
    return None


def register_user(username: str, password: str, app_secret: str):
    if app_secret != settings.app_secret:
        raise AuthError("Invalid App Access Key. You cannot create an account.")

    if not username or not password:
        raise AuthError("Username and password are required.")

    if len(password) < 6:
        raise AuthError("Password must be at least 6 characters long.")

    created = db_create_user(username, password)
    if not created:
        raise AuthError("Username already exists or registration failed.")

    logger.info("New user account created: '%s'", username)
    return True
