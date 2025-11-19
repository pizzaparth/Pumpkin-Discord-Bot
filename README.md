# Pumpkin - Discord Moderation Bot

A comprehensive Discord bot designed to maintain a healthy server environment through automated message filtering, user moderation tools, and AFK status management.

## Features

### 🛡️ Message Filtering
- Automatically detects and removes messages containing banned words
- Customizable banned words list
- Instant user notification when messages are filtered
- Logging of deleted messages for moderation review

### ⏱️ Timeout/Mute System
- Native Discord timeout implementation
- Moderators can mute users for specified durations
- Users cannot send messages while muted
- Easy unmute functionality with `!unmute` command
- Non-permanent solution for temporary user restrictions

### 🚫 Ban Management
- Permanent user bans with custom reasons
- Automatic ban on detected toxic content
- Unban functionality using user IDs
- Prevents banned users from rejoining the server
- Requires `ban_members` permission

### 👢 Kick Functionality
- Temporary user removal without permanent ban
- Ideal for removing inactive members
- Custom kick reasons with logging
- Users can rejoin after being kicked
- Requires `kick_members` permission

### 🚫 AFK Status
- Users can set themselves as Away From Keyboard
- Customizable AFK duration
- Automatic AFK role assignment
- Automatic status removal after timeout
- Notifies other users when mentioning someone who is AFK
- Greetings message when user returns

## Installation

### Prerequisites
- Python 3.8+
- discord.py library
- python-dotenv library

### Setup Steps

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd pumpkin-bot
   ```

2. **Install dependencies**
   ```bash
   pip install discord.py python-dotenv
   ```

3. **Create a Discord Application**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and name it "Pumpkin"
   - Navigate to "Bot" section and click "Add Bot"
   - Copy the bot token

4. **Create configuration file**
   Create a `keys.env` file in the project root:
   ```
   TOKEN=your_bot_token_here
   ```

5. **Set bot permissions**
   - In Developer Portal, go to OAuth2 → URL Generator
   - Select scopes: `bot`
   - Select permissions:
     - Manage Messages
     - Moderate Members
     - Manage Roles
     - Kick Members
     - Ban Members
   - Use the generated URL to add the bot to your server

6. **Run the bot**
   ```bash
   python main.py
   ```

## Configuration

### Adding Banned Words
Edit the `BANNED_WORDS` list in `main.py`:
```python
BANNED_WORDS = [
    "badword1",
    "badword2",
    "offensive",
    # Add more words as needed
]
```

### Creating AFK Role
For full AFK functionality:
1. Go to your Discord server settings
2. Navigate to Roles
3. Create a new role named "AFK"
4. Configure the role permissions as needed

## Commands

### Moderation Commands

| Command | Usage | Permission | Description |
|---------|-------|-----------|-------------|
| `!mute` | `!mute @user <seconds>` | Moderate Members | Timeout a user |
| `!unmute` | `!unmute @user` | Moderate Members | Remove timeout |
| `!ban` | `!ban @user [reason]` | Ban Members | Permanently ban a user |
| `!unban` | `!unban <user_id>` | Ban Members | Unban a user |
| `!kick` | `!kick @user [reason]` | Kick Members | Remove user from server |

### User Commands

| Command | Usage | Permission | Description |
|---------|-------|-----------|-------------|
| `!afk` | `!afk <minutes>` | Everyone | Set AFK status |

## Usage Examples

### Setting AFK Status
```
!afk 30
```
This sets you as AFK for 30 minutes. The bot will automatically remove the status after the time expires.

### Muting a User
```
!mute @username 600
```
Mutes the mentioned user for 600 seconds (10 minutes).

### Banning a User with Reason
```
!ban @username Spam and harassment
```
Bans the user with the specified reason.

### Kicking a User
```
!kick @username Inactive for 2 months
```
Removes the user from the server.

## Permissions Required

The bot requires the following permissions to function properly:

- **View Channels**: See channels where the bot operates
- **Send Messages**: Send status messages and notifications
- **Delete Messages**: Remove messages with banned words
- **Embed Links**: Format messages with embeds
- **Moderate Members**: Apply timeout/mute
- **Manage Roles**: Manage AFK roles
- **Kick Members**: Execute kick command
- **Ban Members**: Execute ban/unban commands

## Error Handling

The bot includes comprehensive error handling for:
- Missing permissions
- Invalid user mentions
- Invalid duration formats
- Discord API errors
- Missing roles (AFK role not found)

## Troubleshooting

### Bot not responding to commands
- Ensure the bot has the required permissions
- Check that the `TOKEN` is correct in `keys.env`
- Verify the bot is online in your server

### Commands not working
- Ensure you have the required permissions for the command
- Check that the bot role is positioned above user roles in the server role hierarchy

### AFK not working
- Create a role named "AFK" in your server
- Ensure the bot has permission to manage roles

### Message filtering not working
- Add words to the `BANNED_WORDS` list in `main.py`
- Ensure the bot has permission to delete messages
- Restart the bot after making changes

## Support

For issues or feature requests, please open an issue in the repository or contact the development team.

## License

This project is open source and available under the MIT License.

## Credits

Developed by the Pumpkin Bot Team. Built with discord.py library.

---

**Note**: Always ensure proper moderation policies are in place when using this bot to maintain a healthy community.
