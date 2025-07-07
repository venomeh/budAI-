# Discord AI Bot

A Discord bot that uses OpenRouter LLM (e.g., DeepSeek) to answer questions in server channels, threads, and direct messages. The bot responds to messages containing `@ai` and provides concise, helpful answers.

---

## Features
- Responds to `@ai ...` in server text channels (creates a thread for each request)
- Responds in threads (maintains context)
- Responds in DMs (if Discord privacy settings allow)
- Uses OpenRouter LLM for AI-powered answers
- Logs activity to `discord.log`

---

## Requirements
- Python 3.8+
- Discord bot account (application) and token
- OpenRouter API key
- The following Python packages:
  - `discord.py`
  - `python-dotenv`
  - `openai`

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd discord-bot
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install discord.py python-dotenv openai
```

### 4. Create a Discord Bot Application
- Go to the [Discord Developer Portal](https://discord.com/developers/applications)
- Click "New Application" and give it a name
- Go to "Bot" > "Add Bot"
- Under "Privileged Gateway Intents", enable **Message Content Intent**
- Copy the **Bot Token** (you'll need it in the next step)

### 5. Get an OpenRouter API Key
- Sign up at [OpenRouter](https://openrouter.ai/)
- Get your API key from your OpenRouter dashboard

### 6. Create a `.env` File
Create a file named `.env` in the project root with the following content:
```
DISCORD_TOKEN=your_discord_bot_token_here
OPEN_ROUTER=your_openrouter_api_key_here
```

### 7. Run the Bot
```bash
python bot.py
```

---

## Inviting the Bot to Your Server
1. Go to the [OAuth2 URL Generator](https://discord.com/developers/applications)
2. Select your application > OAuth2 > URL Generator
3. Select `bot` scope and permissions (at minimum: Send Messages, Read Message History, Create Public Threads)
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

**Example Invite URL:**
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=274877990912
```

---

## Usage
- In any server channel where the bot is present, type:
  - `@ai your question here`
- The bot will create a thread and reply in it.
- In a thread, you can continue the conversation with `@ai ...` and the bot will maintain context.
- You can also DM the bot (if you share a server and privacy settings allow) with `@ai ...` and it will reply.

---

## Troubleshooting
- **Bot not responding in DMs?**
  - Make sure you and the bot share a server.
  - Check your server's privacy settings: "Allow direct messages from server members" must be enabled.
  - The bot must be online and running.
- **Bot not responding in server?**
  - Check the bot's permissions in the channel.
  - Make sure the bot has the Message Content Intent enabled in the Developer Portal.
- **API errors?**
  - Check your OpenRouter API key and usage limits.
- **Logs:**
  - Check `discord.log` for errors and activity.

---

## Notes
- Bots cannot be added to group DMs unless they are on your friends list, which is not possible for bot accounts.
- The bot cannot read or respond to DMs between two normal users.
- All AI responses are limited to 1900 characters to fit Discord's message limits.

---

## License
MIT (or your chosen license) 
