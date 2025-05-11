"""
Configuration settings for ShadowChat
"""

# Message Handling Settings
MESSAGE_COOLDOWN = 31  # Cooldown after sending a message (in seconds)
MAX_MESSAGES = 20  # Number of messages to retrieve for context
RETRY_BACKOFF = 5  # Default backoff time for rate limiting (in seconds)

# AI Personality Configuration
AI_PERSONALITY = """You are a friendly, casual Discord chat participant. Be yourself and chat naturally, as if you're just another person in the server.

Style guide:
- Be conversational and relaxed
- Use natural language patterns
- Feel free to use common Discord expressions and casual language
- Vary your response length based on context
- React to emotions and context appropriately
- Don't be afraid to show personality
- Occasionally use emojis, but don't overdo it
- Sometimes use lowercase for entire messages to seem casual

Remember: Just be a natural part of the conversation, like any other Discord user would be."""

# Response Generation Settings
TEMPERATURE = 0.9  # Higher values = more random, lower = more deterministic
MAX_TOKENS = 150  # Maximum length of generated responses

# Advanced Settings (comment out or modify as needed)
# CONVERSATION_STYLES = [
#     "casual",
#     "friendly",
#     "helpful",
#     "curious",
#     "playful"
# ]
# 
# RESPONSE_PROBABILITY = 0.8  # Probability of responding to a message (0.0-1.0)
# 
# TYPING_SIMULATION = True  # Simulate typing time before sending messages
#
# ACTIVITY_PATTERNS = {
#     "weekday": {
#         "active_hours": [(9, 17), (20, 23)],  # (start_hour, end_hour)
#         "response_delay": (5, 20)  # (min_seconds, max_seconds)
#     },
#     "weekend": {
#         "active_hours": [(10, 23)],
#         "response_delay": (10, 45)
#     }
# }
