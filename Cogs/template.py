#cogs file for template.py

import discord
from discord.ext import commands
from discord import app_commands
import time

class name_your_command_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="name_your_slash_command", description="Type in a description here")
    async def name_your_slash_command(self, interaction: discord.Interaction):
        
        await interaction.response.send_message(f"Hi, {interaction.user.display_name}! This is a slash command.")

async def setup(bot: commands.Bot):
    await bot.add_cog(name_your_command_cog(bot))