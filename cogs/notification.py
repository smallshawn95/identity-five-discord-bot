import json
import discord
import datetime
from typing import Optional
from discord import app_commands
from discord.ext import commands, tasks

class RankingTimeNotification(commands.GroupCog, name = "排位時間通知"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "傳統排位", description = "設定傳統排位通知頻道(未選擇頻道為刪除設定)")
    @app_commands.describe(channel = "選擇一個文字頻道")
    async def classic_ranking(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel] = None):
        with open("./database/notification.json", "r", encoding = "utf8") as file:
            notification_data = json.load(file)
        with open("./database/notification.json", "w", encoding = "utf8") as file:
            json.dump(notification_data, file, indent = 4, ensure_ascii = False)
        await interaction.response.send_message()

    @app_commands.command(name = "五人排位", description = "設定五人排位通知頻道(未選擇頻道為刪除設定)")
    @app_commands.describe(channel = "選擇一個文字頻道")
    async def five_player_ranking(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel] = None):
        with open("./database/notification.json", "r", encoding = "utf8") as file:
            notification_data = json.load(file)
        with open("./database/notification.json", "w", encoding = "utf8") as file:
            json.dump(notification_data, file, indent = 4, ensure_ascii = False)
        await interaction.response.send_message()

tz = datetime.timezone(datetime.timedelta(hours = 8))
# 傳統排位（伺服器時間 UTC+8）：每日 04:00-06:00、12:00-14:00、18:00-22:00（五階以上 19:00-21:00）。
classic_ranking_start_time = [
    datetime.time(hour = 4, minute = 0, tzinfo = tz),
    datetime.time(hour = 12, minute = 0, tzinfo = tz),
    datetime.time(hour = 18, minute = 0, tzinfo = tz),
    datetime.time(hour = 19, minute = 0, tzinfo = tz),
]
classic_ranking_end_time = [
    datetime.time(hour = 6, minute = 0, tzinfo = tz),
    datetime.time(hour = 14, minute = 0, tzinfo = tz),
    datetime.time(hour = 21, minute = 0, tzinfo = tz),
    datetime.time(hour = 22, minute = 0, tzinfo = tz),
]
# 五人排位（伺服器時間 UTC+8）：周末 14:00-18:00、21:00-23:00。
five_player_ranking_start_time = [
    datetime.time(hour = 14, minute = 0, tzinfo = tz),
    datetime.time(hour = 21, minute = 0, tzinfo = tz)
]
five_player_ranking_end_time = [
    datetime.time(hour = 18, minute = 0, tzinfo = tz),
    datetime.time(hour = 23, minute = 0, tzinfo = tz)
]

class RankingTimeNotificationTask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.classic_ranking_start.start()
        self.classic_ranking_end.start()
        self.five_player_ranking_start.start()
        self.five_player_ranking_end.start()

    @tasks.loop(time = classic_ranking_start_time)
    async def classic_ranking_start(self):
        hour = datetime.datetime.now().hour
        pass

    @tasks.loop(time = classic_ranking_end_time)
    async def classic_ranking_end(self):
        pass

    @tasks.loop(time = five_player_ranking_start_time)
    async def five_player_ranking_start(self):
        weekday = datetime.datetime.now().weekday()
        if weekday == 5 or weekday == 6:
            pass

    @tasks.loop(time = five_player_ranking_end_time)
    async def five_player_ranking_end(self):
        weekday = datetime.datetime.now().weekday()
        if weekday == 5 or weekday == 6:
            pass

async def setup(bot: commands.Bot):
    await bot.add_cog(RankingTimeNotification(bot))
    await bot.add_cog(RankingTimeNotificationTask(bot))
