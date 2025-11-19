# Discord Moderation Bot - Complete Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [What This Bot Does](#what-this-bot-does)
3. [Prerequisites](#prerequisites)
4. [Setup Guide](#setup-guide)
5. [Features & Commands](#features--commands)
6. [Code Architecture](#code-architecture)
7. [Troubleshooting](#troubleshooting)
8. [Customization Guide](#customization-guide)

---

## Overview

This is a Discord moderation bot built with **discord.py** that helps server moderators and admins manage their Discord community. The bot provides automated content filtering, user status tracking, and moderation tools—all without needing constant human supervision.

**Purpose:** Automate common moderation tasks and maintain server rules automatically.

**Technology:** Python 3.x with discord.py library

---

## What This Bot Does

The bot provides **7 main features**:

| Feature | What It Does | Who Can Use It |
|---------|--------------|----------------|
| **Auto-Filter** | Automatically deletes messages with banned words | Everyone (automatic) |
| **Greeting** | Responds "Hi" when someone says hello | Everyone (automatic) |
| **AFK System** | Marks users as AFK temporarily | Everyone |
| **Mute/Unmute** | Temporarily silences disruptive users | Moderators only |
| **Kick** | Removes users from server (they can rejoin) | Moderators only |
| **Ban/Unban** | Permanently removes users from server | Admins only |

---

## Prerequisites

Before you start, make sure you have:

- ✅ **Python 3.8 or higher** installed on your computer
- ✅ **A Discord account** and **server admin access**
- ✅ **Basic command line knowledge** (how to run Python scripts)
- ✅ **Your bot token** from [Discord Developer Portal](https://discord.com/developers/applications)

### Required Python Libraries
```bash
pip install discord.py python-dotenv
```

---

## Setup Guide

### Step 1: Get Your Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section on the left sidebar
4. Click "Add Bot"
5. Under the bot's username, click "Reset Token" to see your token
6. **Copy this token** (you'll need it in Step 2)

⚠️ **Never share your token publicly!** It's like a password for your bot.

### Step 2: Configure the Token

1. Create a file named `keys.env` in the same folder as `main.py`
2. Add this line to the file:
   ```
   TOKEN=your_bot_token_here
   ```
3. Replace `your_bot_token_here` with the token you copied

### Step 3: Invite Bot to Your Server


1. In Discord Developer Portal, go to "OAuth2" → "URL Generator"
2. Under **Scopes**, check:
   - `bot`
   - `applications.commands`
3. Under **Bot Permissions**, check:
   - `Manage Messages` (to delete inappropriate messages)
   - `Manage Roles` (for AFK role)
   - `Kick Members` (for kick command)
   - `Ban Members` (for ban command)
   - `Moderate Members` (for timeout/mute)
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### Step 4: Create AFK Role (Optional)

For the AFK feature to work:
1. Go to your Discord server settings
2. Click "Roles" 
3. Create a new role named exactly **"AFK"** (case-sensitive)
4. Save changes

### Step 5: Run the Bot

Open your terminal/command prompt in the bot's folder and run:
```bash
python main.py
```

You should see: `Logged in as YourBotName!`

---

## Features & Commands

### 1. 🛡️ Automatic Word Filter

**What it does:** Automatically deletes messages containing banned words and warns the user.

**How it works:**
- The bot constantly monitors all messages in the server
- If a message contains any word from the banned list, it's instantly deleted
- The user gets a warning message mentioning them

**No command needed** - this works automatically!

**Customize the banned words:**
Edit the `BANNED_WORDS` list in `main.py`:
```python
BANNED_WORDS = [
    "badword1",
    "badword2",
    "offensive",
    # Add your own words here
]
```

**Example:**
- User sends: "You are badword1!"
- Bot deletes the message
- Bot responds: "@User, your message contained inappropriate language and has been removed."

---

### 2. 👋 Greeting System

**What it does:** Bot replies "Hi" when users greet it.

**How to use:** 
Just say hello in any channel where the bot can see messages!

**Trigger words:** hello, hi, Hello, Hi

**Example:**
- You: "Hello everyone!"
- Bot: "Hi"

**Customize:** Edit this line in `main.py` to add more greeting words:
```python
if message.content.lower().startswith(("hello", "hi", "howdy", "hey")):
```

---

### 3. 😴 AFK (Away From Keyboard) System

**What it does:** Temporarily marks you as AFK. When someone mentions you, the bot tells them you're away.

**Command:** `!afk <minutes>`

**Who can use:** Everyone

**Parameters:**
- `<minutes>`: How long you'll be AFK (numbers only)

**Examples:**
```
!afk 30        → Marks you AFK for 30 minutes
!afk 120       → Marks you AFK for 2 hours
```

**What happens:**
1. Bot gives you the "AFK" role
2. When someone mentions you, bot replies "This person is AFK."
3. After the time expires, bot automatically removes the AFK role

**Real-world scenario:**
```
You: !afk 60
Bot: @You has been given AFK role for 60 minute(s).

[Someone else mentions you]
Other User: @You, can you help me?
Bot: This person is AFK.

[After 60 minutes]
Bot: @You is no longer AFK.
```

---

### 4. 🔇 Mute/Unmute (Timeout)

**What it does:** Temporarily prevents a user from sending messages, reacting, or speaking in voice channels.

**Who can use:** Moderators with "Moderate Members" permission

#### Mute Command
**Command:** `!mute @user <seconds>`

**Parameters:**
- `@user`: Mention the user you want to mute
- `<seconds>`: How long to mute them (in seconds)

**Example:**
```
!mute @TrollUser 300     → Mutes user for 5 minutes
!mute @Spammer 3600      → Mutes user for 1 hour
```

#### Unmute Command
**Command:** `!unmute @user`

**Example:**
```
!unmute @TrollUser       → Removes timeout immediately
```

**Real-world scenario:**
```
Moderator: !mute @TrollUser 600
Bot: @TrollUser has been timed out for 600 seconds.

[TrollUser cannot send messages for 10 minutes]

Moderator: !unmute @TrollUser
Bot: @TrollUser has been un-timed out.
```

---

### 5. 👢 Kick Command

**What it does:** Removes a user from the server. They can rejoin if they have an invite link.

**Who can use:** Moderators with "Kick Members" permission

**Command:** `!kick @user [reason]`

**Parameters:**
- `@user`: Mention the user to kick
- `[reason]`: Optional explanation (will be shown in audit log)

**Examples:**
```
!kick @Spammer                    → Kicks user without reason
!kick @Spammer Advertising        → Kicks with reason "Advertising"
!kick @TrollUser Breaking rules   → Kicks with custom reason
```

**Important:** 
- Kicked users CAN rejoin if they get a new invite
- Use this for temporary removals
- For permanent removal, use `!ban` instead

---

### 6. 🚫 Ban Command

**What it does:** Permanently removes a user from the server. They cannot rejoin unless unbanned.

**Who can use:** Admins with "Ban Members" permission

**Command:** `!ban @user [reason]`

**Parameters:**
- `@user`: Mention the user to ban
- `[reason]`: Optional explanation

**Examples:**
```
!ban @TrollUser                      → Bans user without reason
!ban @Spammer Repeated violations    → Bans with reason
```

**Important:**
- Banned users CANNOT rejoin unless you unban them
- Use this for serious rule violations
- More severe than kick

---

### 7. ✅ Unban Command

**What it does:** Removes a user from the ban list, allowing them to rejoin.

**Who can use:** Admins with "Ban Members" permission

**Command:** `!unban <user_id>`

**Parameters:**
- `<user_id>`: The Discord ID of the banned user (18-digit number)

**How to get a user's ID:**
1. Enable Developer Mode in Discord (Settings → Advanced → Developer Mode)
2. Right-click the user's name and select "Copy ID"

**Example:**
```
!unban 123456789012345678    → Unbans user with that ID
```

---

## Code Architecture

### File Structure
```
your-bot-folder/
│
├── main.py              # Main bot code
├── keys.env             # Token storage (NEVER share this!)
└── DOCUMENTATION.md     # This file
```

### How the Code is Organized

The bot uses **object-oriented programming** with a custom `Client` class that extends Discord's built-in client.

#### Main Components:

```
main.py
├── Imports                    # Required libraries
├── Token Configuration        # Load bot token from .env file
├── BANNED_WORDS List         # Words to auto-filter
├── Client Class              # Main bot logic
│   ├── __init__()           # Initialize bot with command tree
│   ├── on_ready()           # Runs when bot starts
│   └── on_message()         # Runs for every message sent
│       ├── Word Filter      # Check for banned words
│       ├── AFK Checker      # Check if mentioned users are AFK
│       ├── Greetings        # Respond to hello/hi
│       ├── !afk command     # AFK role management
│       ├── !mute command    # Timeout users
│       ├── !unmute command  # Remove timeout
│       ├── !kick command    # Kick members
│       ├── !ban command     # Ban members
│       └── !unban command   # Unban members
├── Intents Configuration     # Set bot permissions
└── Run Bot                   # Start the bot
```

### Code Flow Diagram

```
User sends message
       ↓
on_message() triggered
       ↓
Is message from the bot itself? → YES → Ignore
       ↓ NO
Check for banned words
       ↓
Contains banned word? → YES → Delete & warn user
       ↓ NO
Check if message mentions AFK users
       ↓
Mentions AFK user? → YES → Reply "This person is AFK"
       ↓ NO
Check if message is a greeting
       ↓
Starts with hi/hello? → YES → Reply "Hi"
       ↓ NO
Check if message is a command (!afk, !mute, etc.)
       ↓
Process command based on user permissions
```

### Key Design Patterns

#### 1. **Event-Driven Architecture**
The bot reacts to events (messages, user joins, etc.) using async event handlers.

```python
async def on_message(self, message):
    # This runs automatically for EVERY message
```

#### 2. **Permission Checking**
Before executing moderation commands, the bot verifies the user has the right permissions:

```python
if not message.author.guild_permissions.moderate_members:
    await message.channel.send("You don't have permission...")
    return
```

#### 3. **Error Handling**
All commands use try-except blocks to handle potential errors gracefully:

```python
try:
    await member.kick(reason=reason)
except discord.Forbidden:
    await message.channel.send("I don't have permission...")
except Exception as e:
    await message.channel.send(f"Failed: {e}")
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. "Error: TOKEN not found in .env file!"

**Problem:** The bot can't find your token.

**Solutions:**
- Check that `keys.env` exists in the same folder as `main.py`
- Make sure the file contains exactly: `TOKEN=your_token_here`
- No spaces around the `=` sign
- No quotes around the token

---

#### 2. Bot doesn't respond to commands

**Possible causes and fixes:**

**a) Bot is offline**
- Check if you see "Logged in as..." in the terminal
- Make sure the terminal/command prompt is still running

**b) Missing permissions**
- Go to Server Settings → Roles
- Make sure bot's role has required permissions
- Bot's role should be ABOVE the roles it needs to moderate

**c) Wrong command format**
- Commands must start with `!` (exclamation mark)
- User mentions must use `@` 
- Check for typos

---

#### 3. "I don't have permission to delete messages"

**Problem:** Bot doesn't have the right permissions in Discord.

**Solution:**
1. Go to Server Settings → Roles
2. Find your bot's role
3. Enable these permissions:
   - Manage Messages
   - Manage Roles
   - Kick Members
   - Ban Members
   - Moderate Members

---

#### 4. AFK role not working

**Solutions:**
- Create a role named exactly **"AFK"** (case-sensitive)
- Make sure bot's role is ABOVE the AFK role in the role hierarchy
- Bot needs "Manage Roles" permission

---

#### 5. Word filter not working

**Check:**
- Bot has "Manage Messages" permission
- Bot's role is high enough in the hierarchy
- The banned word is spelled correctly in `BANNED_WORDS`
- Bot is actually running (check terminal)

---

#### 6. "ModuleNotFoundError: No module named 'discord'"

**Problem:** discord.py is not installed.

**Solution:**
```bash
pip install discord.py python-dotenv
```

If you have multiple Python versions:
```bash
python3 -m pip install discord.py python-dotenv
```

---

## Customization Guide

### 1. Change Banned Words

Edit the `BANNED_WORDS` list at the top of `main.py`:

```python
BANNED_WORDS = [
    "spam",
    "nsfw",
    "offensive_word",
    "another_bad_word",
]
```

**Tips:**
- Words are case-insensitive (automatically converted to lowercase)
- The filter checks if the banned word appears ANYWHERE in the message
- Be careful with short words that might appear in legitimate words

---

### 2. Change Greeting Message

Find this section and modify the reply:

```python
if message.content.lower().startswith(("hello", "hi", "Hello", "Hi")):
    await message.reply("Hi")  # ← Change this to your custom greeting
    return
```

**Examples:**
```python
await message.reply("Hello! How can I help you?")
await message.reply("👋 Welcome!")
await message.reply(f"Hey {message.author.name}!")
```

---

### 3. Change AFK Role Name

If you want to use a different role name instead of "AFK":

1. Search for all instances of `"AFK"` in the code
2. Replace with your custom role name
3. Make sure the role exists in your server

**Example:** Change "AFK" to "Away"
```python
afk_role = discord.utils.get(message.guild.roles, name="Away")
```

---

### 4. Add More Commands

To add a new command, follow this pattern:

```python
elif message.content.startswith("!yourcommand"):
    # Check permissions if needed
    if not message.author.guild_permissions.administrator:
        await message.channel.send("You need admin permission!")
        return
    
    # Your command logic here
    await message.channel.send("Command executed!")
```

---

### 5. Change Command Prefix

To use a different prefix instead of `!`:

Find all instances of:
```python
message.content.startswith("!")
```

Replace with your preferred prefix:
```python
message.content.startswith("?")  # Question mark prefix
message.content.startswith("/")  # Slash prefix
message.content.startswith(".")  # Dot prefix
```

---

## Advanced Concepts Explained

### What is Asynchronous Programming?

You'll notice `async` and `await` throughout the code. Here's what they mean:

**Async functions** can pause and let other code run while waiting for something (like a Discord API response).

```python
async def on_message(self, message):  # async function
    await message.delete()             # await = "wait for this to finish"
```

**Why it matters:** Without async/await, the bot would freeze while waiting for Discord to respond to each action.

---

### What are Discord Intents?

Intents tell Discord what events your bot wants to receive:

```python
intents = discord.Intents.default()
intents.message_content = True  # Let bot read message content
intents.guilds = True           # Let bot see server info
intents.members = True          # Let bot see member info
```

**Important:** Some intents (like `message_content`) must be enabled in the Discord Developer Portal under "Bot" → "Privileged Gateway Intents".

---

### Understanding Discord Permissions

Discord has a **role hierarchy**:
- Higher roles can affect lower roles
- Bot must have a role HIGHER than users it moderates
- Even with permission, bot can't moderate server owner

**Permission check example:**
```python
message.author.guild_permissions.moderate_members  # True or False
```

---

## Best Practices

### 1. Security
- ✅ **Never commit `keys.env` to GitHub** (add it to `.gitignore`)
- ✅ Keep your bot token secret
- ✅ Regenerate token if it's exposed
- ✅ Use environment variables for sensitive data

### 2. Error Handling
- ✅ Always use try-except blocks for Discord API calls
- ✅ Provide helpful error messages to users
- ✅ Log errors for debugging

### 3. User Experience
- ✅ Give clear command usage instructions
- ✅ Confirm actions with feedback messages
- ✅ Use mentions to notify affected users

### 4. Performance
- ✅ Don't block the event loop (use `await`)
- ✅ Keep banned words list reasonable in size
- ✅ Clean up scheduled tasks properly

---

## Additional Resources

### Official Documentation
- [discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs)

### Learning Resources
- [discord.py Guide](https://discordpy.readthedocs.io/en/stable/intro.html)
- [Python Async/Await Tutorial](https://realpython.com/async-io-python/)

### Community Help
- [discord.py Discord Server](https://discord.gg/dpy)
- [Stack Overflow - discord.py tag](https://stackoverflow.com/questions/tagged/discord.py)

---

## Changelog & Version History

**Version 1.0** (Current)
- ✅ Basic moderation commands (mute, kick, ban)
- ✅ Word filtering system
- ✅ AFK role management
- ✅ Greeting functionality

**Planned Features**
- 🔄 Warning system with tracking
- 🔄 Message logging
- 🔄 Custom command prefix per server
- 🔄 Slash commands support

---

## License & Credits

**Created by:** Parth Pancholi
**License:** MIT

---

## Questions?

If you have questions or run into issues not covered here, check:
1. The [Troubleshooting section](#troubleshooting)
2. The [discord.py documentation](https://discordpy.readthedocs.io/)
3. Search existing issues on GitHub/Discord communities

**Happy moderating! 🎉**