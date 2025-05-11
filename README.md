# ShadowChat
A discreet Discord automation system that uses natural language AI to participate in server conversations as a regular user.

## Overview

ShadowChat enables seamless integration of AI conversation capabilities through a standard Discord user account. Using the Groq API with LLaMA 4 Scout model, it generates natural, context-aware responses that blend into regular server conversations.

## Features

- **Natural Interactions**: Responds to conversations in a casual, human-like manner
- **Context Awareness**: Uses recent message history to maintain conversational coherence
- **Privacy-Focused**: Automatically filters out usernames to avoid detection
- **Rate Limiting**: Implements cooldown periods to respect Discord's rate limits
- **Error Handling**: Gracefully handles API errors and rate limits

## Installation

### Prerequisites

- Python 3.8+
- Discord User Token
- Groq API Key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/shadowchat.git
cd shadowchat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your credentials:
```
DISCORD_TOKEN=your_discord_user_token
GROQ_API_KEY=your_groq_api_key
CHANNEL_ID=your_target_channel_id
```

## Usage

Start the bot with:

```bash
python shadowchat.py
```

The system will automatically:
1. Monitor the specified Discord channel
2. Generate responses to new messages
3. Send replies that maintain natural conversation flow

## Configuration

Edit `config.py` to customize:

- Message cooldown period
- Context message limit
- Bot personality and response style
- User IDs to ignore

## ⚠️ Important Disclaimer

**This project is for educational purposes only.**

Using automated user accounts may violate Discord's Terms of Service. Use at your own risk - Discord may suspend accounts that operate automated user accounts.

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
