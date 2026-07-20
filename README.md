# Craft of the Titans 任務書繁體中文漢化

Craft of the Titans 任務書與遊戲內指南的繁體中文（zh-TW）漢化。

> **本專案只漢化任務書與任務附屬指南，不包含各模組的物品名稱、介面、提示或說明。**

本專案以 Better Questing 2.3.234 使用的 JSON 格式為基礎，只修改玩家可見的
文字內容；任務 ID、物品資料、NBT、座標、格式碼及其他結構資料均維持原樣。

## 適用版本

- 整合包：[Craft of the Titans](https://www.curseforge.com/minecraft/modpacks/craft-of-the-titans)
- 整合包版本：**1.30（作者最終停更版）**
- Minecraft：**1.10.2**
- Better Questing：**2.3.234**

本漢化依 1.30 的原始設定檔逐句製作，不保證適用較舊的整合包版本。

原作由 **BoolymanMC** 製作，其
[CurseForge 原始頁面](https://www.curseforge.com/minecraft/modpacks/craft-of-the-titans)
標示授權為 **Public Domain**。完整來源紀錄及第三方權利說明請參閱
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。

## 漢化範圍

- Better Questing 任務、章節、條件與獎勵文字
- Enchiridion 的 Craft of the Titans 指南
- Enchiridion 的血魔法血之祭壇升級指南
- BloodMagic 設定目錄內的 Enchiridion 副本

不包含模組本身的語言檔、物品名稱、方塊名稱、GUI 或工具提示。

## 模組漢化建議

若需要模組內容的中文翻譯，建議另外安裝
[簡體中文漢化資源包](https://www.curseforge.com/minecraft/texture-packs/simplified-chinese-localization-resource-package)。
其 CurseForge 頁面提供 Minecraft 1.10.2 對應版本。

1. 下載並啟用適用 Minecraft 1.10.2 的資源包。
2. 在遊戲語言設定中切換為 **簡體中文（中國）**。
3. 完整重新啟動遊戲。

必須切換成簡體中文，資源包內的模組語言檔才會生效。本專案直接修改任務書 JSON，
因此任務書仍會顯示本專案提供的繁體中文內容。

## 安裝

### 使用發佈壓縮檔

從 [GitHub Releases](https://github.com/joe910602-stack/craft_of_the_titans/releases/latest)
下載 `craft-of-the-titans-1.30-zh-tw.zip`，再依下列步驟安裝：

1. 備份 Minecraft 實例的 `config` 資料夾。
2. 將 `craft-of-the-titans-1.30-zh-tw.zip` 解壓縮至 Minecraft 實例根目錄。
3. 允許壓縮檔中的 `config` 資料夾合併並覆蓋同名檔案。
4. 完整重新啟動 Minecraft。

發佈壓縮檔亦附有 `LICENSE.md` 與 `THIRD_PARTY_NOTICES.md`，方便下載者離線
查閱非商業授權、原作來源及第三方權利聲明。

### 直接從原始碼安裝

將下列三個目錄依原結構複製到 Minecraft 實例的 `config` 資料夾：

| 專案目錄 | 安裝位置 |
|---|---|
| `translation/betterquesting` | `config/betterquesting` |
| `translation/enchiridion` | `config/enchiridion` |
| `translation/BloodMagic/enchiridion` | `config/BloodMagic/enchiridion` |

不要把 `quest_zh_tw_cache.json` 或 Python 工具複製進遊戲設定目錄。

## 專案結構

```text
original/                       英文原檔
  betterquesting/
  enchiridion/
  BloodMagic/
translation/                    可安裝的漢化成品
  betterquesting/
  enchiridion/
  BloodMagic/enchiridion/
scripts/                        翻譯、稽核與打包工具
  quest_zh_tw_cache.json
  quest_english_terms.md
  *.py
```

`original` 只供翻譯比對；實際安裝內容以 `translation` 為準。

## 驗證

需要 Python 3。若要使用線上翻譯工具，請先安裝依賴：

```powershell
python -m pip install -r scripts/requirements.txt
```

```powershell
python scripts/validate_project.py
```

驗證程式會檢查任務書與翻譯快取是否一致、Minecraft 格式碼、換行、
Enchiridion 結構及編碼，最後建立 ZIP 與 SHA-256 校驗碼。

## 編碼注意事項

Better Questing 漢化檔使用 UTF-8。Enchiridion 漢化檔使用 JSON Unicode 跳脫字元，
避免舊版模組以系統字元集載入時把中文顯示成 `????`。請勿把 Enchiridion 檔案
自動轉換回含有原始中文字元的其他編碼。

## 翻譯原則

- 使用臺灣繁體中文。
- 能自然漢化的普通名詞與遊戲術語優先翻譯。
- 模組名、品牌、單位、介面識別碼及無可靠譯名的專名保留英文。
- 雙關語與冷笑話以中文語意及笑點為優先；無法可靠轉譯時保留原文並列入紀錄。
- 所有保留英文與待確認詞彙記錄於
  [`scripts/quest_english_terms.md`](scripts/quest_english_terms.md)。

詳細校對規則請參閱 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 授權

- 漢化內容與說明文件：CC BY-NC 4.0
- Python 維護腳本與自動化工具：PolyForm Noncommercial 1.0.0
- `original/` 中的作者原始內容不由本專案重新授權

兩種專案授權都允許非商業的使用、修改及分享，但禁止商用與營利；詳細條件請參閱
[`LICENSE.md`](LICENSE.md)。

## 說明

這是非官方社群漢化專案。Minecraft、Craft of the Titans 及各模組名稱與內容的
權利歸其各自權利人所有。
