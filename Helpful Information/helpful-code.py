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

# Bot definition and intents:

description = """A bot used for providing a comprehensive self-service guidance and ticketing system for support purposes, coded by Raven Fyre for use in the TLOU Esports Discord server."""
bot = commands.Bot(command_prefix=".", description=description, help_command=None, intents=discord.Intents.all())

# Universal variables:

# bot_id = 
# everytime a new ticket is made, the bot stores the ticket channel ID + author ID.

# Bot Event when bot starts up or restarts:

@bot.event
async def on_ready():
    bot.add_view(SuggestionPanelButton())
    bot.add_view(ViewVotesButton())
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='The discord server'))
    print(f"{bot.name} is online!")
    try:
        synced = await bot.tree.sync()
        print("Commands synced successfully.")
    except:
        print("Error syncing commands.")

# ~ ~ ~ ~ ~ BOT COMPONENTS ~ ~ ~ ~ ~

# --- SELECT MENUS ---

# --- EXAMPLES ---

# Creating an example Select Menu!

class SelectMenuTemplate(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
      
    @discord.ui.select(
        custom_id = "name-your-select",
        placeholder = "Please select an option",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Option 1",
                description="This is the first option"
            ),
            discord.SelectOption(
                label="Option 2",
                description="This is the second option"
            ),
            discord.SelectOption(
                label="Option 3",
                description="This is the third option"
            )
        ]
    )
    async def select_callback(self, select, interaction):
      
        if select.values[0] == "Option 1":
          
            embed = discord.Embed(
                description=f"You chose option 1!",
                color=discord.Colour.orange(),
            )
            embed.set_footer(text="Coded by Raven Fyre")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if select.values[0] == "Option 2":
          
            embed = discord.Embed(
                description=f"You chose option 2!",
                color=discord.Colour.purple(),
            )
            embed.set_footer(text="Coded by Raven Fyre")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if select.values[0] == "Option 3":
          
            embed = discord.Embed(
                description=f"You chose option 3!",
                color=discord.Colour.pink(),
            )
            embed.set_footer(text="Coded by Raven Fyre")
            await interaction.response.send_message(embed=embed, ephemeral=True)

# --- MODALS ---

# --- EXAMPLES ---

# Creating an example 'modal'!

class ExampleModal(discord.ui.Modal, title='Making a Suggestion'):

    suggestion = discord.ui.TextInput(label="Suggestion", custom_id="suggestion", placeholder="Type a suggestion for the Discord server here!", style=discord.TextStyle.long, min_length=10, max_length=500, required=True)
    
    async def on_submit(self, interaction: discord.Interaction):

        await interaction.response.send_message(f'Thanks for your suggestion, {interaction.user.mention}!', ephemeral=True)
        embed = discord.Embed(description=f"**Suggestion:**\n{self.suggestion}\n\n**Suggested by:** {interaction.user.mention}", timestamp=datetime.datetime.now(), color=0xFFA500)
        bot_message = await channel_name.send(embed=embed)

# --- BUTTONS ---

# --- EXAMPLES ---

# Creating an example button

class ExampleButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Click Me", custom_id="click_me", row=0, style=discord.ButtonStyle.blurple)
    
    async def click_me_button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
    
        await interaction.response.send_message("Button pressed!")

# --- SLASH COMMANDS ---

# --- EXAMPLES ---

# Slash Command to send a modal

@bot.tree.command(name="send_modal", description="An example slash command to send a modal to the user.", guild_ids=my_server)
async def send_modal(interaction: discord.Interaction):

    await interaction.response.send_modal(SuggestModal(title="Making a Suggestion", custom_id="suggestion"))

# Slash Command to send a 'panel' with a button that only administrators can use

@bot.tree.command(name="send_button", description="Sends an example panel with a button for the server.", guild_ids=my_server)
@app_commands.checks.has_permissions(manage_guild=True)
async def send_button(interaction: discord.Interaction):

    await interaction.response.send_message(f"{interaction.user.mention}, the suggestion panel will be posted below!", ephemeral=True)
    time.sleep(1)
    embed = discord.Embed(description="**Example Panel**\n\nClick the button below!", color=0x00FF00)
    example_panel = await interaction.channel.send(f"```yaml\n\nExample Panel\n\n```\n• Click the button below!", embed=embed, view=ExampleButton())

# Slash Command with Arguments

@bot.tree.command(name="multiple_arguments", description="An example slash command with multiple arguments.", guild_ids=my_server)
@app_commands.checks.has_permissions(manage_guild=True)
@app_commands.describe(arg1='What info do you need to provide?')
@app_commands.describe(arg2='What more info do you need?')
@app_commands.rename(arg1='new_name_here')
@app_commands.rename(arg2='new_name_here_2')
async def multiple_arguments(interaction: discord.Interaction, arg1: str, arg2: str):

    embed = discord.Embed(description=f"{interaction.user.mention} said {arg1} and {arg2}.", timestamp=datetime.datetime.now(), color=0x00FF00)
    embed.set_footer(text=f"{bot.user.display_name}")
    await interaction.response.send_message(f"{interaction.user.mention}, thank you for using this slash command!", ephemeral=True)

# ~ ~ ~ ~ ~ BOT EVENTS ~ ~ ~ ~ ~

# --- EXAMPLES ---

# Welcome new members with the membership role to the server

@bot.event
async def on_member_update(before, after):

    if before.roles == after.roles:
        print("No role change!")

    else:
        membership_role = before.guild.get_role(id)
  
        if membership_role in after.roles:
            if not membership_role in before.roles:
                chat_channel = bot.get_channel(id)
                await chat_channel.send(f"Welcome to the server, {after.mention}!")

# Alert when a member leaves the server

@bot.event
async def on_member_remove(member):
  
    role_name = interaction.guild.get_role(id)
    if role_name in member.roles:
      
        leave_channel = bot.get_channel(id)
        leave_embed = discord.Embed(
        description=f"One of our members, {member.mention} ({member}), has left the server!",
            color=discord.Colour.orange(),
        )
        await leave_channel.send(embed=leave_embed)

# Bot Event to limit reactions per user

#@bot.event
#async def on_raw_reaction_add(payload):
#    channel = await bot.fetch_channel(payload.channel_id)
#    suggestion = await channel.fetch_message(payload.message_id)
#    user = await bot.fetch_user(payload.user_id)
    
#    if user != bot.user:
#        if suggestion.author.id == bot_id: # ID of Suggestions Bot
          
#            if payload.emoji.name == "✅":
#                cross_reaction = get(suggestion.reactions, emoji="❌")
#                await cross_reaction.remove(user)
              
#            elif payload.emoji.name == "❌":
#                tick_reaction = get(suggestion.reactions, emoji="✅")
#                await tick_reaction.remove(user)

# Bot Event to delete messages in a certain channel

#@bot.event
#async def on_message(message):

#    channel_name = bot.get_channel(id)

#    if message.author.bot:

#        return
#        await bot.process_commands(message)

#        else:

#            await message.delete()
#            embed = discord.Embed(
#                description=f"{message.author.mention}, your message has been removed as this is a command-only channel. Please type `.suggest` (including the full stop) at the start of your message, followed by your suggestion.",
#                color=discord.Colour.red(),
#                )
#            reply = await message.channel.send(embed=embed, delete_after=15)
            # await reply.delete(delay=10)  # Delete the reply after 10 seconds
#            await bot.process_commands(message)

# Run bot:

load_dotenv()
bot.run(os.getenv("BOT_TOKEN"))