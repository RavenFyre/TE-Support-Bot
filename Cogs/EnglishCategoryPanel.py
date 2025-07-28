#cogs file for EnglishCategoryPanel.py

import discord
from discord.ext import commands
from discord import app_commands
import time
import SupportPanels

# Select Menu for the English Categories panel

class EnglishCategorySupportButtons(discord.ui.View):
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

# Slash Command to send English categories Panel

class english_category_panel_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="english_category_panel", description="Sends the support panel with a drop-down menu to select a support category.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def send_english_category_panel(self, interaction: discord.Interaction):
        
        await interaction.response.send_message(f"{interaction.user.mention}, the suggestion panel will be posted below!", ephemeral=True)
        time.sleep(1)
        suggestion_panel = await interaction.channel.send(SupportPanels.english_support_message_content, embed=SupportPanels.english_support_embed, view=EnglishCategorySupportButtons())

async def setup(bot: commands.Bot):
    await bot.add_cog(english_category_panel_cog(bot))