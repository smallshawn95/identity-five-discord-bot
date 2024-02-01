import json
import random
import discord
from discord import app_commands
from discord.ext import commands

class CharacterSelector(commands.GroupCog, name = "隨機選角"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "求生者", description = "隨機選擇一位求生者")
    async def survivor(self, interaction: discord.Interaction):
        with open("./database/characters.json", "r", encoding = "utf8") as file:
            characters_data = json.load(file)
        survivor_name = random.choice(characters_data["求生者"])
        await interaction.response.send_message(survivor_name)

    @app_commands.command(name = "監管者", description = "隨機選擇一位監管者")
    async def hunter(self, interaction: discord.Interaction):
        with open("./database/characters.json", "r", encoding = "utf8") as file:
            characters_data = json.load(file)
        hunter_name = random.choice(characters_data["監管者"])
        await interaction.response.send_message(hunter_name)

async def setup(bot: commands.Bot):
    await bot.add_cog(CharacterSelector(bot))
