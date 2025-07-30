#cogs file for MultiLangPanel.py

import discord
from discord.ext import commands
from discord import app_commands
import time
import SupportPanels
import cogs.MultiLangENCat
from cogs.MultiLangENCat import ENCategoryMenu

# Buttons for multi-language support: English, Spanish, Portuguese & Arabic

class MultiLangSupportButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="English", custom_id="english_multi_lang", row=0, style=discord.ButtonStyle.blurple)    
    async def english_button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message("", embed=cogs.MultiLangENCat.ENCategory_embed, view=ENCategoryMenu(), ephemeral=True)
    
    @discord.ui.button(label="Español", custom_id="spanish_multi_lang", row=0, style=discord.ButtonStyle.blurple)
    async def spanish_button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message("Spanish Button pressed!", ephemeral=True)
    
    @discord.ui.button(label="Português", custom_id="portuguese_multi_lang", row=0, style=discord.ButtonStyle.blurple)    
    async def portuguese_button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message("Portuguese Button pressed!", ephemeral=True)
    
    @discord.ui.button(label="العربي", custom_id="arabic_multi_lang", row=0, style=discord.ButtonStyle.blurple)
    async def arabic_button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message("Arabic Button pressed!", ephemeral=True)


# Slash Command to send Multi-Language Panel

class multi_lang_panel_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="multi_lang_panel", description="Sends the support panel with English, Spanish, Portuguese & Arabic support.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def send_multi_lang_panel(self, interaction: discord.Interaction):
        
        await interaction.response.send_message(f"{interaction.user.mention}, the suggestion panel will be posted below!", ephemeral=True)
        time.sleep(1)
        suggestion_panel = await interaction.channel.send(embed=SupportPanels.multi_lang_embed, view=MultiLangSupportButtons())

async def setup(bot: commands.Bot):
    await bot.add_cog(multi_lang_panel_cog(bot))