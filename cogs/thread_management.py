import discord
from discord.ext import commands, tasks

class ThreadManagement(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.keep_threads_open.start()  # start the loop when the cog is loaded

    def cog_unload(self):
        """Cancel the loop when the cog is unloaded"""
        self.keep_threads_open.cancel()

    @tasks.loop(hours=72)  # run once every 3 days
    async def keep_threads_open(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                for thread in channel.threads:
                    if not thread.locked and not thread.archived:
                        try:
                            # "Touch" the thread by reapplying its auto_archive_duration
                            await thread.edit(auto_archive_duration=thread.auto_archive_duration)
                            print(f"Refreshed {thread.name}")
                        except Exception as e:
                            print(f"Couldn't refresh {thread.name}: {e}")

    @keep_threads_open.before_loop
    async def before_keep_threads_open(self):
        """Wait until the bot is ready before starting the loop"""
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(ThreadManagement(bot))