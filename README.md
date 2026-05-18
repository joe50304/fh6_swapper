# Forza Horizon 6 語音語言交換器 (FH6 Swapper)

[![VirusTotal 掃毒報告 (8/71)](https://img.shields.io/badge/VirusTotal-8/71-orange)](https://www.virustotal.com/gui/file/711344bc7f4ca302327fb0c35ec67ca169d4d278b87c56c244ae05721b0d4ede?nocache=1)
[![Jotti (0/13)](https://img.shields.io/badge/Jotti-0/13-success)](https://virusscan.jotti.org/en-US/filescanjob/4pqqtukt8n)
[![MetaDefender (1/20)](https://img.shields.io/badge/MetaDefender-1/20-yellow)](https://metadefender.com/results/file/bzI2MDUxOHVFcFNXcC13WU9KaUw5MFUxaG0zTGo_mdaas)
[![Kaspersky (Clean)](https://img.shields.io/badge/Kaspersky-Clean-success)](https://opentip.kaspersky.com/711344BC7F4CA302327FB0C35EC67CA169D4D278B87C56C244AE05721B0D4EDE/results?tab=upload)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

這是一個為《極限競速：地平線 6》(Forza Horizon 6) 設計的輕量級工具，可讓玩家自訂「介面文字」與「語音」為不同語言（例如：繁體中文介面 + 日文語音）。工具透過安全交換遊戲的語言資料夾來實現此功能，並內建備份與還原機制。

## 功能特色
- 🎮 **自動偵測遊戲路徑**：支援自動搜尋 Steam / Xbox (Microsoft Store) 的常見安裝路徑。
- 🔄 **一鍵交換語言**：輕鬆實現混搭語言（如：中字日音）。
- ↩️ **安全還原機制**：內建歷史紀錄系統，隨時可一鍵還原至原始語言設定。
- ⚡ **無需安裝依賴**：純 Python 內建標準函式庫編寫，無需使用 pip 安裝任何外部套件。

## 環境需求
- **作業系統**：Windows 10 / 11
- **執行環境**：Python 3.6+
- **依賴套件**：全數使用 Python 內建標準函式庫 (`tkinter`, `os`, `json`, `shutil`, `datetime`, `sys`, `pathlib`)，**不需**安裝任何額外套件。

## 操作步驟

1. **遊戲內設定語音**：
   先開啟遊戲，進入「選項 → 語言」，將語言設定為你想要的**語音語言**（例如：日語），儲存後**完全關閉遊戲**。

2. **開啟交換器工具**：
   透過命令提示字元或 PowerShell 執行以下指令：
   ```bash
   python fh6_swapper.py
   ```
   （或者若系統有設定，也可直接雙擊 `fh6_swapper.py` 啟動）

3. **確認遊戲路徑**：
   程式啟動後會自動搜尋系統中 `Forza Horizon 6\media\Stripped\StringTables` 的路徑。
   - 若顯示綠色勾勾表示偵測成功。
   - 若未自動偵測到，請點擊「瀏覽…」手動選擇該 `StringTables` 資料夾。

4. **選擇語言配置**：
   - **介面文字語言**：選擇你遊戲內想看的**文字/字幕語言**（例如：`CHT` 代表繁體中文）。
   - **語音語言**：選擇你剛剛在遊戲內設定的**語音語言**（例如：`JP` 代表日文）。

5. **執行交換**：
   點擊 **「🔄 交換資料夾」** 按鈕。
   > 看到操作日誌顯示「交換完成」後，重新啟動遊戲即可享受「中文介面 + 日文語音」的體驗！

## 注意事項與還原方法

- **遊戲更新或修復前**：若遊戲準備進行更新或檔案驗證，請先開啟本工具，點擊 **「↩ 還原」** 將資料夾恢復至原始狀態，以避免檔案更新發生衝突或被覆蓋。更新完畢後再重新執行交換即可。
- **資料夾存取權限**：若點擊交換時發生失敗，請確保遊戲已**徹底關閉**。若仍有問題，請嘗試以系統管理員身分執行程式。
- **備份紀錄路徑**：工具的操作紀錄自動存放於 `%APPDATA%\FH6Swapper\state.json`，請勿任意刪除該檔案，以免失去還原功能。

## 安全性報告

本工具原始碼完全公開透明，為讓使用者安心，在此附上由各大知名防毒平台提供的最新掃毒報告（少部分引擎可能因為 Python 打包程式而產生誤判，皆為正常現象）：
- 🛡️ [VirusTotal 掃毒報告](https://www.virustotal.com/gui/file/711344bc7f4ca302327fb0c35ec67ca169d4d278b87c56c244ae05721b0d4ede?nocache=1) (8/71)
- 🛡️ [Jotti 掃毒報告](https://virusscan.jotti.org/en-US/filescanjob/4pqqtukt8n) (0/13)
- 🛡️ [MetaDefender 掃毒報告](https://metadefender.com/results/file/bzI2MDUxOHVFcFNXcC13WU9KaUw5MFUxaG0zTGo_mdaas) (1/20)
- 🛡️ [Kaspersky 掃毒報告](https://opentip.kaspersky.com/711344BC7F4CA302327FB0C35EC67CA169D4D278B87C56C244AE05721B0D4EDE/results?tab=upload) (Clean)

## 特別感謝 (Acknowledgments)

**🕊️ 特別紀念原始作者：Purson**  
感謝 Purson 對此專案核心概念與最初版本的偉大貢獻與啟發。沒有他奠定的基礎，這個方便的工具就不會誕生，感謝他讓這份心意能延續並造福更多玩家。

## 授權條款 (License)

本專案採用 [MIT License](LICENSE) 授權。
您可以自由使用、修改和分發本工具，但請保留原作者版權聲明。
