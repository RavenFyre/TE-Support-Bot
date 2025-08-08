import os
import re
import discord
from discord.ext import commands
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

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

class LanguageFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        if not credentials_path:
            raise Exception("GOOGLE_CREDENTIALS_PATH is not set in the .env file.")

        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.translate_client = translate.Client(credentials=credentials)

        self.logging_channel_id = 1403088963417276437
        self.spanish_channel_id = 1399064382583083119

    def detect_language(self, text):
        try:
            return self.translate_client.detect_language(text)
        except Exception as e:
            print(f"Language detection error: {e}")
            return None

    @commands.Cog.listener()
    async def on_message(self, message):
        # Skip bot's own messages
        if message.author.bot:
            return
        # Skip Spanish channel monitoring
        if message.channel.id == self.spanish_channel_id:
            return
        # Skip emoji-only / no letters
        if not re.search(r"[A-Za-zÀ-ÿ]", message.content):
            return
        result = self.detect_language(message.content)
        if not result:
            return
        lang = result.get("language")
        confidence = result.get("confidence")
        # Skip English
        if lang == "en" or lang is None:
            return
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
        try:
            if lang == "es":
                spanish_chat = self.bot.get_channel(self.spanish_channel_id)
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention}, please use English only in this chat. You may speak Spanish in {spanish_chat.mention}"
                )
            elif lang == "pt":
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention}, please use English only in this chat. Portuguese is not permitted."
                )
        except Exception as e:
            print(f"Error deleting message or sending warning: {e}")

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(LanguageFilter(bot))