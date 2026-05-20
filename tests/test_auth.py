# tests/test_auth.py
"""Tests for authentication utilities"""
import pytest
from src import auth

def test_login_user_empty_credentials():
    # Should return None when username or password is empty
    assert auth.login_user("", "password") is None
    assert auth.login_user("user", "") is None

def test_register_user_invalid_secret(monkeypatch):
    # Simulate wrong app secret to raise AuthError
    from src import config
    monkeypatch.setattr(config.settings, "app_secret", "correct_secret")
    with pytest.raises(auth.AuthError):
        auth.register_user("newuser", "pwd", app_secret="wrong")
