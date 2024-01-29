# IdentityV Discord Dot

這是一臺第五人格相關功能的 Discord Bot。

## 開始使用
1. 設置 `.env.example` 中的 Bot Token 並將檔名重新命名為 `.env`。
```
DISCORD_BOT_TOKEN=Your_Discord_Bot_Token
```
2. 使用 Dockerfile 建置 docker 映像檔。
```bash
docker build -t image_name .
```
3. 使用剛建置好的映像檔運行 docker 容器。
```bash
docker run --name container_name -d image_name
```

## 貢獻人員
* [j1110543](https://github.com/j1110543)
* [smallshawn95](https://github.com/smallshawn95)
