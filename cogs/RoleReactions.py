# cogs file for RoleReactions.py

import discord
from discord.ext import commands
from discord import app_commands
import time

# Defining the bot
description = """A bot used for providing a comprehensive self-service guidance and ticketing system for support purposes, coded by Raven Fyre for use in the TLOU Esports Discord server."""
bot = commands.Bot(command_prefix=".", description=description, help_command=None, intents=discord.Intents.all())

# Role Variables

#te_server = bot.get_guild(832364474769997895)
#competitive_role = interaction.guild.get_role(1396216406999040101)
#spectator_role = interaction.guild.get_role(1396218187783340082)
#livestream_role = interaction.guild.get_role(1396218416662188073)
#video_role = interaction.guild.get_role(1396218561139310786)


# Buttons for Competitive / Spectator / Scrims roles

class ParticipationRoleButtons1(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Competitive", custom_id="competitive_role", row=0, style=discord.ButtonStyle.green, emoji="⚔️")    
    async def competitive_role_button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        competitive_role = interaction.guild.get_role(1396216406999040101)
        spectator_role = interaction.guild.get_role(1396218187783340082)
        if competitive_role in interaction.user.roles:
            await interaction.user.remove_roles(competitive_role)
            await interaction.response.send_message(f"{interaction.user.mention}, the {competitive_role.mention} role has been removed. Feel free to click the button again to add it.", ephemeral=True)
        elif spectator_role in interaction.user.roles:
            await interaction.user.remove_roles(spectator_role)
            time.sleep(1)
            await interaction.user.add_roles(competitive_role)
            await interaction.response.send_message(f"{interaction.user.mention}, you have received the {competitive_role.mention} role and the {spectator_role.mention} has been removed.", ephemeral=True)
        else:
            await interaction.user.add_roles(competitive_role)
            await interaction.response.send_message(f"{interaction.user.mention}, you have received the {competitive_role.mention} role! Feel free to click the button again to remove your role.", ephemeral=True)

    @discord.ui.button(label="Scrims", custom_id="scrims_role", row=0, style=discord.ButtonStyle.green, emoji="🗡️")
    async def scrims_role_button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        scrims_role = interaction.guild.get_role(1406213396457848884)
        spectator_role = interaction.guild.get_role(1396218187783340082)
        if scrims_role in interaction.user.roles:
            await interaction.user.remove_roles(scrims_role)
            await interaction.response.send_message(f"{interaction.user.mention}, the {scrims_role.mention} role has been removed. Feel free to click the button again to add it.", ephemeral=True)
        elif spectator_role in interaction.user.roles:
            await interaction.user.remove_roles(spectator_role)
            time.sleep(1)
            await interaction.user.add_roles(scrims_role)
            await interaction.response.send_message(f"{interaction.user.mention}, you have received the {scrims_role.mention} role and the {spectator_role.mention} has been removed.", ephemeral=True)
        else:
            await interaction.user.add_roles(scrims_role)
            await interaction.response.send_message(f"{interaction.user.mention}, you have received the {scrims_role.mention} role! Feel free to click the button again to remove your role.", ephemeral=True)

    @discord.ui.button(label="Spectator", custom_id="spectator_role", row=0, style=discord.ButtonStyle.green, emoji="👀")
    async def spectator_role_button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        competitive_role = interaction.guild.get_role(1396216406999040101)
        spectator_role = interaction.guild.get_role(1396218187783340082)
        if spectator_role in interaction.user.roles:
            await interaction.user.remove_roles(spectator_role)
            await interaction.response.send_message(f"{interaction.user.mention}, the {spectator_role.mention} role has been removed. Feel free to click the button again to add it.", ephemeral=True)
        elif competitive_role in interaction.user.roles:
            await interaction.user.remove_roles(competitive_role)
            time.sleep(1)
            await interaction.user.add_roles(spectator_role)
            await interaction.response.send_message(f"{interaction.user.mention}, you have received the {spectator_role.mention} role and the {competitive_role.mention} has been removed.", ephemeral=True)
        else:
            await interaction.user.add_roles(spectator_role)
            await interaction.response.send_message(f"{interaction.user.mention}, you have received the {spectator_role.mention} role! Feel free to click the button again to remove your role.", ephemeral=True)


# Buttons for livestream / video alerts

class ParticipationRoleButtons2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Livestream Alerts", custom_id="livestream_role", row=0, style=discord.ButtonStyle.green, emoji="🎥")
    async def livestream_role_button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        livestream_role = interaction.guild.get_role(1396218416662188073)
        if livestream_role in interaction.user.roles:
            await interaction.user.remove_roles(livestream_role)
            await interaction.response.send_message(f"{interaction.user.mention}, the {livestream_role.mention} role has been removed. Feel free to click the button again to add it.", ephemeral=True)
        else:
            await interaction.user.add_roles(livestream_role)
            await interaction.response.send_message(f"{interaction.user.mention}, you have received the {livestream_role.mention} role! Feel free to click the button again to remove your role.", ephemeral=True)
    
    @discord.ui.button(label="Video Alerts", custom_id="video_role", row=0, style=discord.ButtonStyle.green, emoji="🎬")
    async def video_role_button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        video_role = interaction.guild.get_role(1396218561139310786)
        if video_role in interaction.user.roles:
            await interaction.user.remove_roles(video_role)
            await interaction.response.send_message(f"{interaction.user.mention}, the {video_role.mention} role has been removed. Feel free to click the button again to add it.", ephemeral=True)
        else:
            await interaction.user.add_roles(video_role)
            await interaction.response.send_message(f"{interaction.user.mention}, you have received the {video_role.mention} role! Feel free to click the button again to remove your role.", ephemeral=True)

# Buttons for Language-specific channel access

class ParticipationRoleButtons3(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Español", custom_id="spanish_access", row=0, style=discord.ButtonStyle.green, emoji="💬")
    async def spanish_role_button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        spanish_role = interaction.guild.get_role(1399067285607546991)
        if spanish_role in interaction.user.roles:
            await interaction.user.remove_roles(spanish_role)
            await interaction.response.send_message(f"{interaction.user.mention}, the {spanish_role.mention} role has been removed. Feel free to click the button again to add it.", ephemeral=True)
        else:
            await interaction.user.add_roles(spanish_role)
            await interaction.response.send_message(f"{interaction.user.mention}, you have received the {spanish_role.mention} role! Feel free to click the button again to remove your role.", ephemeral=True)


# Slash command to send panel messages for reactions

class role_reactions_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reaction_role_panels", description="Sends the various panels for the TLOU Esports reaction roles.")
    async def reaction_role_panel(self, interaction: discord.Interaction):
        
        await interaction.response.send_message(f"{interaction.user.mention}, the reaction role panel will be posted below!\n\nPlease allow several seconds for the bot to process this request.", ephemeral=True)
        competitive_role = interaction.guild.get_role(1396216406999040101)
        time.sleep(1)
        spectator_role = interaction.guild.get_role(1396218187783340082)
        time.sleep(1)
        scrims_role = interaction.guild.get_role(1406213396457848884)
        time.sleep(1)
        reaction_embed_1 = discord.Embed(title="Participation Roles", description=f"⚔️ {competitive_role.mention} - Ready to play esports matches? Ping this role & request other players to accept your match!\n🗡️ {scrims_role.mention} - Ping to get others to join in ranked scrims matches.\n👀 {spectator_role.mention} - A role for all the TLOU lovers, match observers and chat lurkers.\n\n***Please note:** only one role between {competitive_role.mention} and {spectator_role.mention} can be selected at a time; it is not possible to have both of these roles.*", color=0x388e3c)
        reaction_panel_1 = await interaction.channel.send(embed=reaction_embed_1, view=ParticipationRoleButtons1())
        livestream_channel = interaction.guild.get_channel(832954831324971080)
        time.sleep(1)
        video_channel = interaction.guild.get_channel(832364475528904716)
        time.sleep(1)
        livestream_role = interaction.guild.get_role(1396218416662188073)
        time.sleep(1)
        video_role = interaction.guild.get_role(1396218561139310786)
        time.sleep(1)
        reaction_embed_2 = discord.Embed(title="Receive Notifications", description=f"🎥 {livestream_role.mention} - Ping this role if you go-live in {livestream_channel.mention} + get this role to receive notifications.\n🎬 {video_role.mention} - Ping this role if you post a new clip or video in {video_channel.mention} + get this role to receive notifications.", color=0x388e3c)
        reaction_panel_2 = await interaction.channel.send(embed=reaction_embed_2, view=ParticipationRoleButtons2())
        #spanish_role = interaction.guild.get_role(1399067285607546991)
        #time.sleep(2)
        #reaction_embed_3 = discord.Embed(title="Language-specific Channel Access", description=f"💬 {spanish_role.mention} - ¿Hablas español? Receive access to a Spanish-speaking channel.", color=0x388e3c)
        #reaction_panel_3 = await interaction.channel.send(embed=reaction_embed_3, view=ParticipationRoleButtons3())

async def setup(bot: commands.Bot):
    await bot.add_cog(role_reactions_cog(bot))