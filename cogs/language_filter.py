import os
import json
import discord
from discord.ext import commands
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

class LanguageFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Load Google credentials from env
        google_creds_raw = os.getenv("GOOGLE_CREDENTIALS_JSON")
        if not google_creds_raw:
            raise Exception("GOOGLE_CREDENTIALS_JSON is not set in the .env file.")

        try:
            google_creds = json.loads(google_creds_raw)
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in GOOGLE_CREDENTIALS_JSON: {e}")

        credentials = service_account.Credentials.from_service_account_info(google_creds)
        self.translate_client = translate.Client(credentials=credentials)

    def detect_language(self, text):
        try:
            result = self.translate_client.detect_language(text)
            return result['language']
        except Exception as e:
            print(f"Language detection error: {e}")
            return None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        # Channel ID for Spanish chat
        spanish_channel_id = 1399064382583083119
        # Ignore messages in the Spanish channel
        if message.channel.id == spanish_channel_id:
            return
        # If no letters at all, skip detection (emoji-only, numbers, punctuation)
        if not re.search(r"[A-Za-zÀ-ÿ]", message.content):
            return
        
        lang = self.detect_language(message.content)
        # If it's English or undetected, skip
        if lang == "en" or lang is None:
            return
        if lang == "es":
            try:
                spanish_chat = self.bot.get_channel(spanish_channel_id)
                await message.delete()
                await message.channel.send(f"{message.author.mention}, please use English only in this chat. You may speak Spanish in {spanish_chat.mention}")
            except Exception as e:
                print(f"Error deleting message: {e}")
        elif lang == "pt":
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, please use English only in this chat. Portuguese is not permitted.")
            except Exception as e:
                print(f"Error deleting message: {e}")

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(LanguageFilter(bot))