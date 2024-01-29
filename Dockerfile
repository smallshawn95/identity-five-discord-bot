# 使用 Python 3.10 的 slim 版本作為基礎鏡像
FROM python:3.10-slim

# 設置工作初始目錄 /app
WORKDIR /app

# 將本機 requirements.txt 檔案複製到容器 /app 目錄
COPY requirements.txt ./

# 執行 Python 套件更新和安裝
RUN pip install --upgrade pip && pip install -r requirements.txt

# 將本機機器人檔案複製容器 /app 目錄
COPY .env bot.py ./
COPY cogs ./cogs

# 定義容器啟動時執行的指令
CMD ["python", "bot.py"]
