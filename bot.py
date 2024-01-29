import os, discord, asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = commands.when_mentioned_or("!"), intents = intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"{bot.user} is online")
    print(f"Synced {len(synced)} slash commands.")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
