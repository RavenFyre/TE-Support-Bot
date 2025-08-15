import os
import json
import re
import discord
from discord.ext import commands
from discord import app_commands
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

settings_file = "language_filter_settings.json"

# Default settings if the file doesn't exist
default_settings = {
    "confidence_threshold": 0.6
}

# Moderator role check for slash command usage
def is_server_moderator():
    def predicate(interaction: discord.Interaction) -> bool:
        return any(role.id == 995028319324098640 for role in interaction.user.roles)
    return app_commands.check(predicate)

LANGUAGE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "pt": "Portuguese",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ru": "Russian",
    "ar": "Arabic",
}

def load_settings():
    if not os.path.exists(settings_file):
        with open(settings_file, "w") as f:
            json.dump(default_settings, f, indent=4)
        return default_settings.copy()
    with open(settings_file, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=4)

class LanguageFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = load_settings()

        credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        if not credentials_path:
            raise Exception("GOOGLE_CREDENTIALS_PATH is not set in the .env file.")

        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.translate_client = translate.Client(credentials=credentials)
        
        # Only monitor these channels
        self.monitored_channels = {
            1109582139231580170,  # #main-chat
            832954831324971080,   # #livestreams
            832364475528904716,   # #clips-and-highlights
            1116529174698532906,  # #anyone-need-3rd
            926143359003787344,   # #suggestions
        }

        self.logging_channel_id = 1403088963417276437   # #language-detection-log
        self.audit_log_channel_id = 832692408042258432  # #audit-log
        self.spanish_channel_id = 1399064382583083119   # #chat-espanol
    
    async def log_api_error(self, error_message: str):
        try:
            channel = self.bot.get_channel(self.audit_log_channel_id)
            if channel:
                embed = discord.Embed(
                title="⚠️ Language Filter API Error",
                description=error_message,
                color=discord.Color.red()
            )
            await channel.send(embed=embed)
        except Exception as e:
            # Fallback in case Discord logging fails
            print(f"Failed to send error to audit-log: {e} | Original error: {error_message}")

    def detect_language(self, text):
        try:
            return self.translate_client.detect_language(text)
        except Exception as e:
            error_message = f"Language detection error: {e}\nText: {text[:500]}"  # truncate long messages
            print(error_message)  # fallback
            if self.bot.is_ready():
                # Schedule async logging
                self.bot.loop.create_task(self.log_api_error(error_message))
            return None

    @commands.Cog.listener()
    async def on_message(self, message):
        # Skip bot's own messages
        if message.author.bot:
            return
        # Only process if message channel is in the monitored list
        if message.channel.id not in self.monitored_channels:
            return
        # Skip emoji-only / no letters
        if not re.search(r"[A-Za-zÀ-ÿ]", message.content):
            return
        result = self.detect_language(message.content)
        if not result:
            return
        lang = result.get("language")
        confidence = result.get("confidence")
        # Skip English or Unknown Language
        if lang == "en" or lang is None:
            return
        # Get readable name for language
        language_name = LANGUAGE_NAMES.get(lang, f"Unknown (`{lang}`)")
        confidence_text = f"{confidence * 100:.2f}%" if isinstance(confidence, (float, int)) else "Unknown"
        # Log non-English messages
        try:
            log_channel = self.bot.get_channel(self.logging_channel_id)
            if log_channel:
                embed = discord.Embed(
                    title="🌐 Non-English Message Detected",
                    color=discord.Color.blue()
                )
                embed.add_field(name="Author", value=message.author.mention, inline=True)
                embed.add_field(name="Channel", value=message.channel.mention, inline=True)
                embed.add_field(name="Detected Language", value=language_name, inline=True)
                embed.add_field(name="Confidence", value=confidence_text, inline=True)
                embed.add_field(name="Message", value=message.content[:1024], inline=False)
                await log_channel.send(embed=embed)
        except Exception as e:
            print(f"Error sending log embed: {e}")
        # Delete certain languages
        confidence_threshold = self.settings.get("confidence_threshold", 0.6)
        try:
            if lang == "es" and isinstance(confidence, (float, int)) and confidence >= confidence_threshold:
                spanish_chat = self.bot.get_channel(self.spanish_channel_id)
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention}, please use English only in this chat. You may speak Spanish in {spanish_chat.mention}"
                )
            elif lang == "pt" and isinstance(confidence, (float, int)) and confidence >= confidence_threshold:
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention}, please use English only in this chat. Portuguese is not permitted here."
                )
            elif lang == "it" and isinstance(confidence, (float, int)) and confidence >= confidence_threshold:
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention}, please use English only in this chat. Italian is not permitted here."
                )
        except Exception as e:
            print(f"Error deleting message or sending warning: {e}")

        await self.bot.process_commands(message)

    # Slash command to see the threshold
    @app_commands.command(name="get_language_threshold", description="See the current language confidence threshold for deleting messages is")
    @is_server_moderator()
    async def get_threshold(self, interaction: discord.Interaction):
        threshold = self.settings.get("confidence_threshold", 0.6)
        await interaction.response.send_message(f"The current confidence threshold for deleting messages is set to {threshold*100:.0f}%.\n\nTo change this percentage, please use the `/set_language_threshold` command, followed by a decimal number between 0 and 1.")
        
    # Slash command to update the threshold
    @app_commands.command(name="set_language_threshold", description="Set the language confidence threshold for deleting messages")
    @is_server_moderator()
    async def set_threshold(self, interaction: discord.Interaction, threshold: float):
        if not 0 <= threshold <= 1:
            await interaction.response.send_message("Threshold must be a decimal number between 0 and 1.\n\nFor example, `0.6` = 60%")
            return
        self.settings["confidence_threshold"] = threshold
        save_settings(self.settings)
        await interaction.response.send_message(f"Confidence threshold updated to {threshold*100:.0f}%")

async def setup(bot):
    await bot.add_cog(LanguageFilter(bot))