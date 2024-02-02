import math
import json
import discord
import datetime
from typing import List
from discord import app_commands
from discord.ext import commands, tasks

class RankingTimeNotification(commands.GroupCog, name = "排位時間通知"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def setting_select_callback(self, interaction: discord.Interaction):
        value = interaction.data["values"][0]
        if value == "classic":
            embed = discord.Embed(title = "傳統排位通知設定")
            view = ClassicRankingSettingView(timeout = 60)
        elif value == "five_player":
            embed = discord.Embed(title = "五人排位通知設定")
            view = ""
        await interaction.response.edit_message(embed = embed, view = view)

    @app_commands.command(name = "設定", description = "排位時間通知設定")
    async def setting(self, interaction: discord.Interaction):
        embed = discord.Embed(title = "排位時間通知設定")
        view = discord.ui.View(timeout = 60)
        select = discord.ui.Select(
            placeholder = "選擇排位時間通知功能",
            options = [
                discord.SelectOption(label = "傳統排位", value = "classic"),
                discord.SelectOption(label = "五人排位", value = "five_player")
            ]
        )
        select.callback = self.setting_select_callback
        view.add_item(select)
        await interaction.response.send_message(embed = embed, view = view)

class ClassicRankingSettingView(discord.ui.View):
    def __init__(self, timeout: float):
        super().__init__(timeout = timeout)

    async def check_guild(self, guild_id: str):
        with open("./database/notification.json", "r+", encoding = "utf8") as file:
            notification_data = json.load(file)
            if guild_id not in notification_data["傳統排位"]:
                notification_data["傳統排位"][guild_id] = {
                    "頻道": None,
                    "身分組": []
                }
                file.seek(0)
                json.dump(notification_data, file, indent = 4, ensure_ascii = False)
                file.truncate()

    async def get_text_channel_view(self, text_channels: List[discord.TextChannel]):
        view = discord.ui.View(timeout = 60)
        total_num = math.ceil(len(text_channels) / 25) if len(text_channels) <= 125 else 5
        for i in range(total_num):
            min_num = i * 25
            if i == total_num - 1 and (i + 1) * 25 > len(text_channels):
                max_num = len(text_channels)
            else:
                max_num = (i + 1) * 25
            select = discord.ui.Select(
                placeholder = f"{str(min_num).zfill(3)}-{str(max_num).zfill(3)}",
                options = [
                    discord.SelectOption(
                        label = text_channels[j].name,
                        value = text_channels[j].id,
                    )
                    for j in range(min_num, max_num)
                ]
            )
            select.callback = self.text_channel_select_callback
            view.add_item(select)
        return view

    async def text_channel_select_callback(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)
        channel_id = interaction.data["values"][0]
        await self.check_guild(guild_id)
        with open("./database/notification.json", "r+", encoding = "utf8") as file:
            notification_data = json.load(file)
            notification_data["傳統排位"][guild_id]["頻道"] = channel_id
            file.seek(0)
            json.dump(notification_data, file, indent = 4, ensure_ascii = False)
            file.truncate()
        await interaction.response.edit_message(view = self)
        await interaction.followup.send("設定文字頻道成功！")

    async def get_role_view(self, roles: List[discord.Role]):
        view = discord.ui.View(timeout = 60)
        total_num = math.ceil(len(roles) / 25) if len(roles) <= 125 else 5
        for i in range(total_num):
            min_num = i * 25
            if i == total_num - 1 and (i + 1) * 25 > len(roles):
                max_num = len(roles)
            else:
                max_num = (i + 1) * 25
            select = discord.ui.Select(
                placeholder = f"{str(min_num).zfill(3)}-{str(max_num).zfill(3)}",
                options = [
                    discord.SelectOption(
                        label = roles[j].name,
                        value = roles[j].id,
                    )
                    for j in range(min_num, max_num)
                ],
                max_values = max_num - min_num
            )
            select.callback = self.role_select_callback
            view.add_item(select)
        return view

    async def role_select_callback(self, interaction: discord.Interaction):
        values = interaction.data["values"]
        guild_id = str(interaction.guild_id)
        await self.check_guild(guild_id)
        with open("./database/notification.json", "r+", encoding = "utf8") as file:
            notification_data = json.load(file)
            roles = notification_data["傳統排位"][guild_id]["身分組"]
            for value in values:
                if value not in roles:
                    notification_data["傳統排位"][guild_id]["身分組"].append(value)
            file.seek(0)
            json.dump(notification_data, file, indent = 4, ensure_ascii = False)
            file.truncate()
        await interaction.response.edit_message(view = self)
        await interaction.followup.send("設定身分組成功！")

    @discord.ui.button(label = "文字頻道", style = discord.ButtonStyle.blurple)
    async def text_channel_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = await self.get_text_channel_view(interaction.guild.text_channels)
        await interaction.response.edit_message(view = view)

    @discord.ui.button(label = "身分組", style = discord.ButtonStyle.blurple)
    async def role_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = await self.get_role_view(interaction.guild.roles)
        await interaction.response.edit_message(view = view)

    @discord.ui.button(label = "重置", style = discord.ButtonStyle.red)
    async def reset_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = str(interaction.guild_id)
        await self.check_guild(guild_id)
        with open("./database/notification.json", "r+", encoding = "utf8") as file:
            notification_data = json.load(file)
            del notification_data["傳統排位"][guild_id]
            file.seek(0)
            json.dump(notification_data, file, indent = 4, ensure_ascii = False)
            file.truncate()
        await interaction.response.defer()
        await interaction.followup.send("設定重置成功！")

class RankingTimeNotificationTask(commands.Cog):
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
