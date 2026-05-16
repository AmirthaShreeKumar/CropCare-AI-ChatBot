import time
from collections import deque
import streamlit as st
from src.logger import logger

class RateLimiter:
    """
    A simple in-memory rate limiter for Streamlit users.
    Limits the number of requests per user within a time window.
    """
    def __init__(self, requests_limit=10, window_seconds=60):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        
        # Initialize session state for tracking if not present
        if 'request_history' not in st.session_state:
            st.session_state.request_history = deque()

    def is_allowed(self):
        """Check if the current user is allowed to make a request"""
        current_time = time.time()
        
        # Ensure deque exists in session state (in case of page refresh/state loss)
        if 'request_history' not in st.session_state:
            st.session_state.request_history = deque()
            
        history = st.session_state.request_history
        
        # Remove timestamps outside the current window
        while history and history[0] < current_time - self.window_seconds:
            history.popleft()
        
        if len(history) < self.requests_limit:
            history.append(current_time)
            logger.info(f"Rate Limiter: Request allowed. Current count in window: {len(history)}")
            return True, None
        
        # Calculate wait time
        wait_time = int(self.window_seconds - (current_time - history[0]))
        logger.warning(f"Rate Limiter: Request denied. Limit reached ({self.requests_limit}). Wait {wait_time}s.")
        return False, wait_time

# Create a global instance for the app
# Default: 10 requests per 60 seconds per user session
limiter = RateLimiter(requests_limit=10, window_seconds=60)
