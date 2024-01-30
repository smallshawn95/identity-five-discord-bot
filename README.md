# IdentityV Discord Dot

這是一臺第五人格相關功能的 Discord Bot。

## 開始使用
1. 下載本儲存庫到本機上。
```bash
git clone https://github.com/smallshawn95/identity-five-discord-bot.git
```
2. 將 `.env.example` 檔名重新命名為 `.env` 並設置 Discord Bot Token。
```env
DISCORD_BOT_TOKEN=Your_Discord_Bot_Token
```
3. 使用 Dockerfile 建置 docker 映像檔。
```bash
docker build -t image_name .
```
4. 使用剛建置好的映像檔運行 docker 容器。
```bash
docker run --name container_name -d image_name
```

## 開發人員
* [j1110543](https://github.com/j1110543)
* [SmallShawn95](https://github.com/smallshawn95)

## 版權說明
本儲存庫基於 [MIT 許可證](LICENSE)。
點擊 [這裡](https://opensource.org/licenses/MIT) 查看完整 MIT 許可證文本。
