#cogs file for scrims_filter.py

import discord
from discord.ext import commands
from discord import app_commands

class ScrimsFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Only monitor these channels
        self.monitored_channels = {
            1406022439535902883,  # #queue-for-teams
            1406022491041824778,   # #queue-for-1v1s
        }

        self.scrims_rules_id = 1406022143732486286   # #scrims-rules
        
    @commands.Cog.listener()
    async def on_message(self, message):

        # Skip bot's own messages
        if message.author.bot:
            return
        # Only process if message channel is in the monitored list
        if message.channel.id not in self.monitored_channels:
            return
        # Locate scrims rules channel and delete message with reminder embed
        scrims_rules_channel = self.bot.get_channel(self.scrims_rules_id)
        await message.delete()
        embed = discord.Embed(
            description=f"{message.author.mention}, your message has been removed as this is a command-only channel. Please review the {scrims_rules_channel.mention} for help on using the bot.",
            color=discord.Colour.red(),
            )
        reply = await message.channel.send(embed=embed, delete_after=15)
        await self.bot.process_commands(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(ScrimsFilter(bot))