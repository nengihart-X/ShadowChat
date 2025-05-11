"""
Utility functions for ShadowChat
"""

import time
import random
import datetime
from typing import List, Dict, Tuple, Optional


def simulate_typing(message_length: int) -> None:
    """
    Simulate realistic typing time based on message length
    """
    # Average typing speed: ~40-60 WPM = ~200-300 CPM
    chars_per_minute = random.randint(200, 300)
    seconds_per_char = 60 / chars_per_minute
    
    # Calculate typing time with some randomness
    base_time = message_length * seconds_per_char
    variance = base_time * 0.3  # 30% variance
    typing_time = base_time + random.uniform(-variance, variance)
    
    # Add a minimum delay and cap maximum delay
    typing_time = max(1.5, min(typing_time, 15))
    
    time.sleep(typing_time)


def should_be_active(activity_patterns: Dict) -> bool:
    """
    Determine if the bot should be active based on configured activity patterns
    """
    now = datetime.datetime.now()
    day_type = "weekend" if now.weekday() >= 5 else "weekday"
    current_hour = now.hour
    
    # Check if current hour falls within any active periods
    for start_hour, end_hour in activity_patterns.get(day_type, {}).get("active_hours", []):
        if start_hour <= current_hour < end_hour:
            return True
    
    return False


def get_response_delay(activity_patterns: Dict) -> float:
    """
    Calculate response delay based on configured activity patterns
    """
    now = datetime.datetime.now()
    day_type = "weekend" if now.weekday() >= 5 else "weekday"
    
    min_delay, max_delay = activity_patterns.get(day_type, {}).get("response_delay", (5, 20))
    return random.uniform(min_delay, max_delay)


def filter_sensitive_content(text: str, sensitive_words: List[str]) -> str:
    """
    Filter out sensitive content from the text
    """
    lower_text = text.lower()
    for word in sensitive_words:
        if word.lower() in lower_text:
            # Replace the word with asterisks of the same length
            text = text.replace(word, '*' * len(word))
    
    return text


def create_message_id_cache(capacity: int = 100) -> List:
    """
    Create a cache to store processed message IDs to avoid duplicate responses
    """
    return []


def update_message_cache(cache: List, message_id: str, capacity: int = 100) -> List:
    """
    Update the message ID cache and maintain its size
    """
    if message_id in cache:
        return cache
    
    cache.append(message_id)
    if len(cache) > capacity:
        cache.pop(0)
    
    return cache


def extract_command(content: str, prefix: str = "!") -> Tuple[Optional[str], str]:
    """
    Extract command and arguments from message content
    """
    if not content.startswith(prefix):
        return None, content
    
    parts = content[len(prefix):].split(maxsplit=1)
    command = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    
    return command, args
