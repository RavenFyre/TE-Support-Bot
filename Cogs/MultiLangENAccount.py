# cogs file for MultiLangENAccount.py

import discord
from discord.ext import commands
from discord import Client, Intents, Embed, app_commands
import time

# Embed

ENAccount_embed = discord.Embed(title="English Support - Account", description="We're sorry that you're having an issue with your website account.\n\nPlease select one of the account options from the drop-down menu below this message. If none of the options apply, feel free to select 'Miscellaneous'", color=0x388e3c)

# Select Menu for the English Categories panel

# Change PSN
# Change / reset password
# Verify new account
# Change / reset Email address

class ENAccountMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
      
    @discord.ui.select(
        custom_id = "english-category-support",
        placeholder = "What would you like help with today?",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Verify new account",
                description="I need help with the new account verification process"
            ),
            discord.SelectOption(
                label="Reset password",
                description="I have forgotten my password"
            ),
            discord.SelectOption(
                label="Change email address",
                description="I need to change my email address"
            ),
            discord.SelectOption(
                label="Change PSN",
                description="I need to use a different PSN account"
            ),
            discord.SelectOption(
                label="Miscellaneous",
                description="Any other problem or query"
            )
        ]
    )
    async def account_select_callback(self, select, interaction):
      
        if select.values[0] == "Verify new account":
          
            embed = discord.Embed(
                description=f"You chose option 1!",
                color=discord.Colour.orange(),
            )
            embed.set_footer(text="Coded by Raven Fyre")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if select.values[0] == "Reset password":
          
            embed = discord.Embed(
                description=f"You chose option 2!",
                color=discord.Colour.purple(),
            )
            embed.set_footer(text="Coded by Raven Fyre")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if select.values[0] == "Change email address":
          
            embed = discord.Embed(
                description=f"You chose option 3!",
                color=discord.Colour.pink(),
            )
            embed.set_footer(text="Coded by Raven Fyre")
            await interaction.response.send_message(embed=embed, ephemeral=True)























class name_your_command_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="name_your_slash_command", description="Type in a description here")
    async def name_your_slash_command(self, interaction: discord.Interaction):
        
        await interaction.response.send_message(f"Hi, {interaction.user.display_name}! This is a slash command.")

async def setup(bot: commands.Bot):
    await bot.add_cog(name_your_command_cog(bot))