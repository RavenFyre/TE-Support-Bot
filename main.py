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
    bot.tree.add_command(load_cog)
    bot.tree.add_command(unload_cog)
    await bot.load_extension("cogs.ping")
    await bot.load_extension("cogs.EnglishCategoryPanel")
    await bot.load_extension("cogs.MultiLangPanel")
    await bot.load_extension("cogs.RoleReactions")
    bot.add_view(MultiLangSupportButtons())
    bot.add_view(EnglishCategorySupportButtons())
    bot.add_view(ParticipationRoleButtons1())
    bot.add_view(ParticipationRoleButtons2())
    bot.add_view(ParticipationRoleButtons3())
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='TLOU Esports'))
    print(f"{bot.user} is online!")
    try:
        synced = await bot.tree.sync()
        print("Commands synced successfully.")
    except:
        print("Error syncing commands.")

# --- MODALS ---

# --- EXAMPLES ---

# Creating an example 'modal'!

class ExampleModal(discord.ui.Modal, title='Making a Suggestion'):

    suggestion = discord.ui.TextInput(label="Suggestion", custom_id="suggestion", placeholder="Type a suggestion for the Discord server here!", style=discord.TextStyle.long, min_length=10, max_length=500, required=True)
    
    async def on_submit(self, interaction: discord.Interaction):

        await interaction.response.send_message(f'Thanks for your suggestion, {interaction.user.mention}!', ephemeral=True)
        embed = discord.Embed(description=f"**Suggestion:**\n{self.suggestion}\n\n**Suggested by:** {interaction.user.mention}", timestamp=datetime.datetime.now(), color=0xFFA500)
        bot_message = await channel_name.send(embed=embed)

# --- SLASH COMMANDS ---

# Sync the commands
@app_commands.command(name="sync", description="Sync the commands when the bot has been updated.")
@app_commands.checks.has_permissions(manage_guild=True)
async def sync_commands(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
        synced = await bot.tree.sync()
        await interaction.followup.send("Commands synced successfully.")
    except:
        await interaction.followup.send("Error syncing commands.")

# Load the specified cog files
@app_commands.command(name="load", description="Load a specific cog")
@app_commands.checks.has_permissions(manage_guild=True)
async def load_cog(interaction: discord.Interaction, extension: str):
    try:
        await interaction.response.defer()
        await bot.load_extension(f"cogs.{extension}")
        await interaction.followup.send(f"Cog '{extension}' loaded.")
        print(f"Cog '{extension}' has been loaded.")
    except:
        await interaction.response.send_message(f"There was an error loading Cog '{extension}'.")
        print(f"Error loading Cog '{extension}'.")

# Unload the specified cog files
@app_commands.command(name="unload", description="Unload a specific cog")
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
bot.run(os.getenv("BOT_TOKEN"))