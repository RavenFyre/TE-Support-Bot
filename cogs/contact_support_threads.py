import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import asyncio

# Buttons for website / scrims / discord support

class SupportCategoryThreads(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # URLs to my thread messages
        website_support_url = "https://discord.com/channels/832364474769997895/1406663028006588518/1407058248569458768"
        scrims_support_url = "https://discord.com/channels/832364474769997895/1406663438456983584/1407058542925578283"
        discord_support_url = "https://discord.com/channels/832364474769997895/1406663663036928069/1407058713017057350"
        cheat_report_url = "https://discord.com/channels/832364474769997895/1407040526716239882/1407040529262317748"

        # Link buttons (no callback needed!)
        self.add_item(discord.ui.Button(label="Website Support", style=discord.ButtonStyle.link, url=website_support_url, row=0))
        self.add_item(discord.ui.Button(label="Scrims Support", style=discord.ButtonStyle.link, url=scrims_support_url, row=1))
        self.add_item(discord.ui.Button(label="Discord Support", style=discord.ButtonStyle.link, url=discord_support_url, row=2))
        self.add_item(discord.ui.Button(label="Report Cheating", style=discord.ButtonStyle.link, url=cheat_report_url, row=3))

# Button to return to contact support page

class ReturnToSupportPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # URL to my thread message
        contact_support_url = "https://discord.com/channels/832364474769997895/1406546439500206120/1407054159873839155"

        # Link buttons (no callback needed!)
        self.add_item(discord.ui.Button(label="Back to Contact Support", style=discord.ButtonStyle.link, url=contact_support_url))

class ContactSupportThreads(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="contact_support_threads", description="Sends the category selection for the Contact Support threads.")
    async def contact_support_thread_panel(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention}, the contact support category selection panel will be posted below!", ephemeral=True)
        await asyncio.sleep(1)
        embed = discord.Embed(title="Contact Support", description=f"Please select the type of support you’d like help with from the buttons below. This will re-direct you to the appropriate support panel.", color=0x388e3c)
        support_panel = await interaction.channel.send(embed=embed, view=SupportCategoryThreads())

    @app_commands.command(name="contact_support_back_button", description="Sends a 'back' button for the Contact Support threads.")
    async def contact_support_back_button(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention}, the 'back' button will be posted below!", ephemeral=True)
        await asyncio.sleep(1)
        embed = discord.Embed(title="Return to Contact Support", description=f"Click the button below to return to the previous page.", color=0x388e3c)
        back_button_panel = await interaction.channel.send(embed=embed, view=ReturnToSupportPanel())


async def setup(bot: commands.Bot):
    await bot.add_cog(ContactSupportThreads(bot))