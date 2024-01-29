import discord
from discord import app_commands
from discord.ext import commands


class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping_prefix(self, ctx: commands.Context):
        await ctx.send(f"{round(self.bot.latency * 1000)}(ms)")

    @app_commands.command(name="ping")
    async def ping_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{round(self.bot.latency * 1000)}(ms)")


async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
