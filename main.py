# --- GENERIC BOT INFORMATION ---

# Libraries to import:

from dotenv import load_dotenv
import os
import discord
from discord import Client, Intents, Embed, app_commands
from discord.ext import commands
from discord.utils import get
from pprint import pprint
import datetime
import time
import linecache
import asyncio
from langdetect import detect
from google.oauth2 import service_account
import SupportPanels
from cogs.MultiLangPanel import MultiLangSupportButtons
from cogs.EnglishCategoryPanel import EnglishCategorySupportButtons
from cogs.RoleReactions import ParticipationRoleButtons1, ParticipationRoleButtons2, ParticipationRoleButtons3

# Bot definition and intents:

description = """A bot used for providing a comprehensive self-service guidance and ticketing system for support purposes, coded by Raven Fyre for use in the TLOU Esports Discord server."""
bot = commands.Bot(command_prefix=".", description=description, help_command=None, intents=discord.Intents.all())

# Universal variables:

bot_id = 929852328226467860

# everytime a new ticket is made, the bot stores the ticket channel ID + author ID.

# Bot Event when bot starts up or restarts:

@bot.event
async def on_ready():
    # Register slash commands
    bot.tree.add_command(sync_commands)
    bot.tree.add_command(load_cog)
    bot.tree.add_command(unload_cog)

    # Load essential/critical cogs manually (if needed early)
    #await bot.load_extension("cogs.EnglishCategoryPanel")
    #await bot.load_extension("cogs.MultiLangPanel")
    #await bot.load_extension("cogs.RoleReactions")

    # Add persistent views
    bot.add_view(MultiLangSupportButtons())
    bot.add_view(EnglishCategorySupportButtons())
    bot.add_view(ParticipationRoleButtons1())
    bot.add_view(ParticipationRoleButtons2())
    bot.add_view(ParticipationRoleButtons3())

    # Automatically load all other cogs in /cogs folder
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("__"):
            ext = f"cogs.{filename[:-3]}"
            try:
                if ext not in bot.extensions:
                    await bot.load_extension(ext)
                    print(f"✅ Auto-loaded: {ext}")
            except Exception as e:
                print(f"❌ Failed to auto-load {ext}: {e}")

    # Set bot presence
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name='TLOU Esports'
    ))

    # Sync slash commands
    print(f"{bot.user} is online!")
    try:
        synced = await bot.tree.sync()
        print("✅ Slash commands synced.")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")


# --- MODALS ---

# --- EXAMPLES ---

# Creating an example 'modal'!

class ExampleModal(discord.ui.Modal, title='Making a Suggestion'):

    suggestion = discord.ui.TextInput(label="Suggestion", custom_id="suggestion", placeholder="Type a suggestion for the Discord server here!", style=discord.TextStyle.long, min_length=10, max_length=500, required=True)
    
    async def on_submit(self, interaction: discord.Interaction):

        await interaction.response.send_message(f'Thanks for your suggestion, {interaction.user.mention}!', ephemeral=True)
        embed = discord.Embed(description=f"**Suggestion:**\n{self.suggestion}\n\n**Suggested by:** {interaction.user.mention}", timestamp=datetime.datetime.now(), color=0xFFA500)
        bot_message = await channel_name.send(embed=embed)

# Moderator role check for slash command usage
def is_server_moderator():
    def predicate(interaction: discord.Interaction) -> bool:
        return any(role.id == 995028319324098640 for role in interaction.user.roles)
    return app_commands.check(predicate)

# --- SLASH COMMANDS ---

# Sync the commands
@app_commands.command(name="sync", description="Sync the commands when the bot has been updated.")
@app_commands.checks.has_permissions(manage_guild=True)
async def sync_commands(interaction: discord.Interaction):
    try:
        synced = await bot.tree.sync()
        await interaction.response.send_message("Commands synced successfully.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Error syncing commands: {e}", ephemeral=True)

# Load the specified cog files
@app_commands.command(name="load", description="Load a specific cog")
@is_server_moderator()
async def load_cog(interaction: discord.Interaction, extension: str):
    try:
        await interaction.response.defer()
        await bot.load_extension(f"cogs.{extension}")
        await interaction.followup.send(f"Cog '{extension}' loaded.")
        print(f"Cog '{extension}' has been loaded.")
    except Exception as e:
        await interaction.followup.send(f"There was an error loading Cog '{extension}': {e}")
        print(f"Error loading Cog '{extension}': {e}")


# Unload the specified cog files
@app_commands.command(name="unload", description="Unload a specific cog")
@is_server_moderator()
async def unload_cog(interaction: discord.Interaction, extension: str):
    await interaction.response.defer()
    await bot.unload_extension(f"cogs.{extension}")
    await interaction.followup.send(f"Cog '{extension}' unloaded.")
    print(f"Cog '{extension}' has been unloaded.")

# --- EXAMPLES ---

# Slash Command to send a modal

@bot.tree.command(name="send_modal", description="An example slash command to send a modal to the user.")
async def send_modal(interaction: discord.Interaction):

    await interaction.response.send_modal(SuggestModal(title="Making a Suggestion", custom_id="suggestion"))

# Run bot:

load_dotenv()
credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
print("GOOGLE_CREDENTIALS_PATH:", credentials_path)
credentials = service_account.Credentials.from_service_account_file(credentials_path)
bot.run(os.getenv("BOT_TOKEN"))