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

# Slash Command with Arguments

@bot.tree.command(name="multiple_arguments", description="An example slash command with multiple arguments.")
@app_commands.checks.has_permissions(manage_guild=True)
@app_commands.describe(arg1='What info do you need to provide?')
@app_commands.describe(arg2='What more info do you need?')
@app_commands.rename(arg1='new_name_here')
@app_commands.rename(arg2='new_name_here_2')
async def multiple_arguments(interaction: discord.Interaction, arg1: str, arg2: str):

    embed = discord.Embed(description=f"{interaction.user.mention} said {arg1} and {arg2}.", timestamp=datetime.datetime.now(), color=0x00FF00)
    embed.set_footer(text=f"{bot.user.display_name}")
    await interaction.response.send_message(f"{interaction.user.mention}, thank you for using this slash command!", ephemeral=True)

# Run bot:

load_dotenv()
bot.run(os.getenv("BOT_TOKEN"))