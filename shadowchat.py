#!/usr/bin/env python3

import time
import requests
import os
import json
from dotenv import load_dotenv
from config import (
    AI_PERSONALITY,
    MESSAGE_COOLDOWN,
    MAX_MESSAGES,
    RETRY_BACKOFF
)

# Load environment variables
load_dotenv()

# Constants
DISCORD_API_BASE_URL = "https://discord.com/api/v9"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Environment Variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
BOT_USER_ID = os.getenv("BOT_USER_ID")  # Your user account ID
IGNORE_USER_IDS = os.getenv("IGNORE_USER_IDS", "").split(",")  # List of user IDs to ignore

if not DISCORD_TOKEN or not GROQ_API_KEY or not CHANNEL_ID:
    raise ValueError("Missing required environment variables. Ensure DISCORD_TOKEN, GROQ_API_KEY, and CHANNEL_ID are set.")

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

DISCORD_HEADERS = {
    "Authorization": DISCORD_TOKEN,
    "Content-Type": "application/json"
}


def get_latest_messages(limit=MAX_MESSAGES):
    """Fetch recent messages from the Discord channel."""
    url = f"{DISCORD_API_BASE_URL}/channels/{CHANNEL_ID}/messages?limit={limit}"
    try:
        response = requests.get(url, headers=DISCORD_HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        handle_http_error(e, response)
    return []


def handle_http_error(error, response):
    """Handle HTTP errors gracefully."""
    if response.status_code == 401:
        print("⚠️ ERROR: Unauthorized (401) - Check your Discord token.")
    elif response.status_code == 429:
        retry_after = response.json().get("retry_after", RETRY_BACKOFF)
        print(f"Rate limited! Waiting {retry_after} seconds...")
        time.sleep(retry_after)
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")


def generate_response(messages):
    """Generate a response based on the last messages."""
    # Format messages to include context but mask usernames
    chat_history = []
    for msg in messages[::-1]:
        content = msg['content']
        # Don't include usernames in the context, just the messages
        chat_history.append(f"Message: {content}")
    
    context = "\n".join(chat_history)
    
    # Add instruction to never mention usernames
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": AI_PERSONALITY + "\nIMPORTANT: Never mention or repeat usernames in your responses. Respond as if in a natural conversation without referring to specific usernames."},
            {"role": "user", "content": f"Recent message: {messages[0]['content']}\n\nRespond naturally without mentioning any usernames."}
        ],
        "temperature": 0.9,
        "max_tokens": 150
    }

    try:
        response = requests.post(GROQ_API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        response_json = response.json()
        # Add a filter to catch any accidental username mentions
        response_text = response_json.get("choices", [{}])[0].get("message", {}).get("content", "I don't know.")
        return filter_usernames(response_text, messages)
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error generating response: {e}")
    return "Error generating response."


def filter_usernames(response, messages):
    """Filter out any accidental username mentions from the response."""
    # Get list of usernames to filter
    usernames = set(msg['author']['username'].lower() for msg in messages)
    
    # Check if response contains any usernames and remove them
    filtered_response = response
    for username in usernames:
        if username.lower() in filtered_response.lower():
            filtered_response = filtered_response.replace(username, "")
            filtered_response = filtered_response.replace(username.lower(), "")
            filtered_response = filtered_response.replace(username.upper(), "")
    
    # Clean up any double spaces created by filtering
    filtered_response = " ".join(filtered_response.split())
    return filtered_response


def send_message(content, reply_to=None):
    """Send a message to the Discord channel."""
    url = f"{DISCORD_API_BASE_URL}/channels/{CHANNEL_ID}/messages"
    data = {"content": content}
    if reply_to:
        data["message_reference"] = {"message_id": reply_to}

    try:
        response = requests.post(url, headers=DISCORD_HEADERS, json=data)
        response.raise_for_status()
        print("✅ Message sent successfully.")
        time.sleep(MESSAGE_COOLDOWN)
        return True
    except requests.exceptions.HTTPError as e:
        handle_http_error(e, response)
    return False


def should_respond(author_id):
    """Determine if we should respond to this message."""
    # Don't respond to our own messages or ignored users
    if author_id == BOT_USER_ID or author_id in IGNORE_USER_IDS:
        return False
    return True


def main():
    """Main loop for fetching messages and responding in Discord."""
    print("🔮 ShadowChat is now listening...")
    last_message_id = None
    
    while True:
        try:
            messages = get_latest_messages()
            
            if messages and (not last_message_id or messages[0]["id"] != last_message_id):
                latest_message = messages[0]
                last_message_id = latest_message["id"]
                author_id = latest_message["author"]["id"]
                
                if should_respond(author_id):
                    print(f"💬 New message: {latest_message['content'][:50]}...")
                    response = generate_response(messages)
                    
                    if response and response != "Error generating response.":
                        print(f"🤖 Responding with: {response[:50]}...")
                        send_message(response, reply_to=latest_message["id"])
            
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
