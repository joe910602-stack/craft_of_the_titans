# 翻譯與校對規範

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

## 用詞

新增或修改譯名時，請同步檢查：

- `scripts/quest_terminology_zh_tw.py`
- `scripts/quest_zh_tw_cache.json`
- `scripts/quest_english_terms.md`

任何仍出現在漢化句子中的英文片段，都必須是已記錄的保留詞，或列入待確認清單。

## 提交前檢查

```powershell
python scripts/validate_project.py
```

所有稽核的錯誤數應為 0，打包腳本也必須成功解析壓縮檔內的全部 JSON。

## 貢獻授權

提交漢化文字或文件即表示同意依 CC BY-NC 4.0 授權該貢獻；提交 Python 腳本、
GitHub Actions 或其他維護程式碼即表示同意依 PolyForm Noncommercial 1.0.0
授權該貢獻。
授權範圍與完整條件請參閱 [`LICENSE.md`](LICENSE.md)。
