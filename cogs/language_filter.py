import os
import discord
from discord.ext import commands
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

# ISO code to full language name
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
    # Add more if needed
}

class LanguageFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        if not credentials_path:
            raise Exception("GOOGLE_CREDENTIALS_PATH is not set in the .env file.")

        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.translate_client = translate.Client(credentials=credentials)

        # Set your logging channel ID
        self.logging_channel_id = 1403088963417276437
        self.spanish_channel_id = 1399064382583083119

    def detect_language(self, text):
        try:
            result = self.translate_client.detect_language(text)
            return result  # returns a dict with 'language' and 'confidence'
        except Exception as e:
            print(f"Language detection error: {e}")
            return None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Ignore Spanish channel
        if message.channel.id == self.spanish_channel_id:
            return

        result = self.detect_language(message.content)
        if not result:
            return

        lang = result.get("language")
        confidence = result.get("confidence")

        # Skip logging English messages
        if lang == "en":
            return

        # Language full name (fallback to showing ISO code if unknown)
        language_name = LANGUAGE_NAMES.get(lang, f"Unknown (`{lang}`)")

        # Format confidence nicely
        if isinstance(confidence, (float, int)):
            confidence_text = f"{confidence * 100:.2f}%"
        else:
            confidence_text = "Unknown"

        # Send log embed to logging channel
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

        # Language-specific deletion
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
            #elif lang == "ar":
                #await message.delete()
                #await message.channel.send(
                    #f"{message.author.mention}, please use English only in this chat. Arabic is not permitted."
                #)
        except Exception as e:
            print(f"Error deleting message or sending warning: {e}")

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(LanguageFilter(bot))
