# 翻譯與校對規範

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

`original/` 只供翻譯比對；實際安裝內容以 `translation/` 為準。

## 可修改內容

只修改玩家可見的文字值，例如：

- Better Questing 的 `name`、`desc`
- Enchiridion 的 `displayName`、`text`、`templatename`

不要修改任務 ID、物品 ID、NBT 鍵、座標、圖片路徑、依賴關係或數值設定。

## 格式要求

- 保留 `§0`～`§f`、`§k`～`§r` 等 Minecraft 格式碼及原有順序。
- 保留原文的開頭／結尾空白與換行數量。
- 保留網址、縮寫、座標、單位及必要的模組名稱。
- 不要加入「英文（中文）」或「中文（英文）」形式的重複對照，除非內容本身需要。
- JSON 必須能正常解析，不得加入註解或尾端逗號。
- Enchiridion 成品必須保持 ASCII JSON Unicode 跳脫格式。

Better Questing 漢化檔使用 UTF-8。Enchiridion 漢化檔使用 JSON Unicode 跳脫字元，
避免舊版模組以系統字元集載入時把中文顯示成 `????`。請勿把 Enchiridion 檔案
自動轉換回含有原始中文字元的其他編碼。

## 用詞

- 使用臺灣繁體中文。
- 能自然漢化的普通名詞與遊戲術語優先翻譯。
- 模組名、品牌、單位、介面識別碼及無可靠譯名的專名保留英文。
- 雙關語與冷笑話以中文語意及笑點為優先；無法可靠轉譯時保留原文並列入紀錄。

新增或修改譯名時，請同步檢查：

- `scripts/quest_terminology_zh_tw.py`
- `scripts/quest_zh_tw_cache.json`
- `scripts/quest_english_terms.md`

任何仍出現在漢化句子中的英文片段，都必須是已記錄的保留詞，或列入待確認清單。

## 提交前檢查

驗證工具需要 Python 3。若要執行線上翻譯工具，請先安裝其依賴：

```powershell
python -m pip install -r scripts/requirements.txt
```

```powershell
python scripts/validate_project.py
```

驗證程式會檢查任務書與翻譯快取是否一致、Minecraft 格式碼、換行、
Enchiridion 結構及編碼，最後建立 ZIP 與 SHA-256 校驗碼。所有稽核錯誤數
應為 0，打包腳本也必須成功解析壓縮檔內的全部 JSON。

## 貢獻授權

提交漢化文字或文件即表示同意依 CC BY-NC 4.0 授權該貢獻；提交 Python 腳本、
GitHub Actions 或其他維護程式碼即表示同意依 PolyForm Noncommercial 1.0.0
授權該貢獻。
授權範圍與完整條件請參閱 [`LICENSE.md`](LICENSE.md)。
