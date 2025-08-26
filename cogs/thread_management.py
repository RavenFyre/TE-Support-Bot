import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone

audit_log_channel_id = 832692408042258432  # audit-log channel ID

class ThreadManagement(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.keep_threads_open.start()

    def cog_unload(self):
        """Cancel the loop when the cog is unloaded"""
        self.keep_threads_open.cancel()

    @tasks.loop(hours=72)  # run once every 3 days
    async def keep_threads_open(self):
        audit_log_channel = self.bot.get_channel(audit_log_channel_id)
        refreshed_threads = []
        failed_threads = []

        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                for thread in channel.threads:
                    if not thread.locked and not thread.archived:
                        try:
                            await thread.edit(auto_archive_duration=thread.auto_archive_duration)
                            refreshed_threads.append(f"{thread.mention} (in {channel.mention})")
                            print(f"Refreshed {thread.name}")
                        except Exception as e:
                            failed_threads.append(f"{thread.name} (in #{channel.name}, {guild.name}) → {e}")
                            print(f"Couldn't refresh {thread.name}: {e}")

        # Send one embed if there’s something to report
        if audit_log_channel and (refreshed_threads or failed_threads):
            embed = discord.Embed(
                title="📋 Thread Refresh Summary",
                color=discord.Color.blue(),
                timestamp=datetime.now(timezone.utc)
            )

            if refreshed_threads:
                embed.add_field(
                    name=f"✅ Refreshed {len(refreshed_threads)} thread(s)",
                    value="\n".join(refreshed_threads),
                    inline=False
                )

            if failed_threads:
                embed.add_field(
                    name=f"⚠️ Failed to refresh {len(failed_threads)} thread(s)",
                    value="\n".join(failed_threads)[:1000] + ("…" if len("\n".join(failed_threads)) > 1000 else ""),
                    inline=False
                )

            embed.set_footer(text=f"{self.bot.user}")

            await audit_log_channel.send(embed=embed)

    @keep_threads_open.before_loop
    async def before_keep_threads_open(self):
        """Wait until the bot is ready before starting the loop"""
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(ThreadManagement(bot))