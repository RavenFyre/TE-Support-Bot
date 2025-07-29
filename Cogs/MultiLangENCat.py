# cogs file for MultiLangENCat.py

# Libraries to import:

import discord
from discord.ext import commands
from discord import Client, Intents, Embed, app_commands
import time

# Embed

ENCategory_embed = discord.Embed(title="English Support", description="Please select one of the options from the drop-down menu below this message to get started! If none of the options apply, feel free to select 'Miscellaneous'", color=0x388e3c)

# Select Menu for the English Categories panel

class ENCategoryMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
      
    @discord.ui.select(
        custom_id = "english-category-support",
        placeholder = "What would you like help with today?",
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