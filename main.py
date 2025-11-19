# Imports ------------------------
import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import asyncio
import discord.utils
from datetime import timedelta
#---------------------------------


# Token configuration ------------------------------
load_dotenv(dotenv_path="keys.env")
token = os.getenv("TOKEN")
if token is None:
    print("Error: TOKEN not found in .env file!")
    exit(1)
#---------------------------------------------------


# List of abusive/banned words ----
BANNED_WORDS = [
    "badword1",
    "badword2",
    "offensive",
    # Add more words as needed
]
#----------------------------------


class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Logged in as {self.user}!")

    async def on_message(self, message):
        print(f"Message from user: {message.author} : {message.content}")
        if message.author == self.user: #
            return

        # Word filtering - check for banned words
        message_content_lower = message.content.lower()
        for banned_word in BANNED_WORDS:
            if banned_word.lower() in message_content_lower:
                try:
                    await message.delete()
                    await message.channel.send(
                        f"{message.author.mention}, your message contained inappropriate language and has been removed."
                    )
                    print(
                        f"Deleted message from {message.author}: contained '{banned_word}'"
                    )
                    return  # Stop processing this message further
                except discord.Forbidden:
                    await message.channel.send(
                        "I don't have permission to delete messages."
                    )
                    return

        # Check if any mentioned user has AFK role
        if message.mentions:
            afk_role = discord.utils.get(message.guild.roles, name="AFK")
            if afk_role:
                for mentioned_member in message.mentions:
                    if afk_role in mentioned_member.roles:
                        await message.reply("This person is AFK.")
                        break

        # Simple greetings
        if message.content.lower().startswith(("hello", "hi", "Hello", "Hi")):
            await message.reply("Hi")
            return

        # AFK command: !afk duration_in_minutes
        if message.content.startswith("!afk"):

            parts = message.content.split()
            if len(parts) != 2:
                await message.channel.send("Usage: !afk <duration_in_minutes>")
                return

            try:
                duration = int(parts[1])
            except ValueError:
                await message.channel.send(
                    "Please specify the duration in minutes as an integer."
                )
                return

            afk_role = discord.utils.get(message.guild.roles, name="AFK")
            if not afk_role:
                await message.channel.send(
                    "AFK role not found. Please create a role named 'AFK'."
                )
                return

            try:
                await message.author.add_roles(afk_role)
                await message.channel.send(
                    f"{message.author.mention} has been given AFK role for {duration} minute(s)."
                )
            except discord.Forbidden:
                await message.channel.send(
                    "I don't have permission to add roles to this user."
                )
                return

            # Remove AFK role after duration
            async def remove_afk():
                await asyncio.sleep(duration * 60)
                refreshed_member = message.guild.get_member(message.author.id)
                if refreshed_member and afk_role in refreshed_member.roles:
                    try:
                        await refreshed_member.remove_roles(afk_role)
                        await message.channel.send(
                            f"{refreshed_member.mention} is no longer AFK."
                        )
                    except discord.Forbidden:
                        pass

            asyncio.create_task(remove_afk())
            return

        # Mute command: !mute @user seconds using native timeout
        if message.content.startswith("!mute"):
            if not message.author.guild_permissions.moderate_members:
                await message.channel.send(
                    "You don't have permission to mute (timeout)."
                )
                return

            parts = message.content.split()
            if len(parts) != 3:
                await message.channel.send("Usage: !mute @user duration_in_seconds")
                return

            try:
                member = message.mentions[0]
            except IndexError:
                await message.channel.send("Please mention a user to mute.")
                return

            try:
                duration = int(parts[2])
            except ValueError:
                await message.channel.send(
                    "Please specify the duration in seconds as an integer."
                )
                return

            timeout_until = discord.utils.utcnow() + timedelta(seconds=duration)

            try:
                await member.edit(timed_out_until=timeout_until)
                await message.channel.send(
                    f"{member.mention} has been timed out for {duration} seconds."
                )
            except discord.Forbidden:
                await message.channel.send(
                    "I don't have permission to timeout this user."
                )
            except Exception as e:
                await message.channel.send(f"Failed to timeout user: {e}")

        # Unmute command: !unmute @user using native timeout removal
        elif message.content.startswith("!unmute"):
            if not message.author.guild_permissions.moderate_members:
                await message.channel.send("You don't have permission to unmute.")
                return

            try:
                member = message.mentions[0]
            except IndexError:
                await message.channel.send("Please mention a user to unmute.")
                return

            try:
                await member.edit(timed_out_until=None)
                await message.channel.send(f"{member.mention} has been un-timed out.")
            except discord.Forbidden:
                await message.channel.send(
                    "I don't have permission to remove timeout from this user."
                )
            except Exception as e:
                await message.channel.send(f"Failed to remove timeout: {e}")

        # Kick command: !kick @user [reason]
        elif message.content.startswith("!kick"):
            if not message.author.guild_permissions.kick_members:
                await message.channel.send("You don't have permission to kick members.")
                return

            try:
                member = message.mentions[0]
            except IndexError:
                await message.channel.send("Please mention a user to kick.")
                return

            # Extract reason (optional)
            parts = message.content.split(maxsplit=2)
            reason = parts[2] if len(parts) > 2 else "No reason provided"

            try:
                await member.kick(reason=reason)
                await message.channel.send(
                    f"{member.mention} has been kicked. Reason: {reason}"
                )
            except discord.Forbidden:
                await message.channel.send("I don't have permission to kick this user.")
            except Exception as e:
                await message.channel.send(f"Failed to kick user: {e}")

        # Ban command: !ban @user [reason]
        elif message.content.startswith("!ban"):
            if not message.author.guild_permissions.ban_members:
                await message.channel.send("You don't have permission to ban members.")
                return

            try:
                member = message.mentions[0]
            except IndexError:
                await message.channel.send("Please mention a user to ban.")
                return

            # Extract reason (optional)
            parts = message.content.split(maxsplit=2)
            reason = parts[2] if len(parts) > 2 else "No reason provided"

            try:
                await member.ban(reason=reason)
                await message.channel.send(
                    f"{member.mention} has been banned. Reason: {reason}"
                )
            except discord.Forbidden:
                await message.channel.send("I don't have permission to ban this user.")
            except Exception as e:
                await message.channel.send(f"Failed to ban user: {e}")

        # Unban command: !unban user_id
        elif message.content.startswith("!unban"):
            if not message.author.guild_permissions.ban_members:
                await message.channel.send(
                    "You don't have permission to unban members."
                )
                return

            parts = message.content.split()
            if len(parts) != 2:
                await message.channel.send("Usage: !unban <user_id>")
                return

            try:
                user_id = int(parts[1])
            except ValueError:
                await message.channel.send("Please provide a valid user ID.")
                return

            try:
                user = await self.fetch_user(user_id)
                await message.guild.unban(user)
                await message.channel.send(f"{user.mention} has been unbanned.")
            except discord.NotFound:
                await message.channel.send("User not found or not banned.")
            except discord.Forbidden:
                await message.channel.send("I don't have permission to unban users.")
            except Exception as e:
                await message.channel.send(f"Failed to unban user: {e}")


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Required for member and role management


client = Client(intents=intents)
client.run(token)
