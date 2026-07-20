# Craft of the Titans 英文原文術語紀錄

這份檔案記錄任務書中需要統一處理的英文原文詞。
實際轉換規則以 `quest_terminology_zh_tw.py` 為準；本檔案僅供人工查閱與後續校對。

所有仍出現在漢化文字中的英文片段都必須列在本檔案中；若不屬於下列
保留項目，就視為可能漏譯，必須翻譯或加入「待人工確認」清單。

## 已漢化術語

| 英文原文 | 繁體中文 | 備註 |
|---|---|---|
| Soulium | 離魂 | Soulium Dagger → 離魂匕首 |
| Etherium | 以太 | Pool of Etherium → 以太之池；Liquid Etherium → 液態以太 |
| Grimoire of Gaia | 蓋亞魔典 | `Grimoire of Gaie` 是原任務書拼字錯誤，仍譯為蓋亞魔典 |
| Ethetic | 裝飾用 | Ethetic Quartz Blocks → 裝飾用石英方塊 |
| Gelid Cryotheum | 極寒之凜冰 | Cryotheum → 凜冰 |
| Blazing Pyrotheum | 烈焰之熾焱 | Pyrotheum → 熾焱 |
| Inferium | 下級 | Inferium Essence → 下級精華；Inferium Seeds → 下級種子 |
| Cyanite | 藍晶 | 極限反應爐材料 |
| Abyssalnite | 淵素 | 深淵國度材料 |
| Ludicrite | 鎦 | Ludicrite Block → 鎦方塊 |
| Aum / Aums | 全知草 | Ars Magicka 植物 |
| Occulus | 全知之眼 | 保留原文的雙 `c` 拼字以匹配任務書 |
| Black Aurem | 夜黑之耳 | 原文另有 `black aurum`、`Black Aurum` 與 `aurum` 等不一致拼法 |
| Vinteum Dust / Vinteum | 溫特姆粉末 | 任務敘述中可能只寫 Vinteum |
| Tome of Alkahestry | 萬能溶劑之經 |  |
| Stoneburnt | 燒製石頭 | Stoneburnt blocks → 燒製石頭方塊 |
| Sheepuff / Sheepuffs | 雲跳羊 |  |
| Moa | 恐鳥 | Black Moa → 黑色恐鳥 |
| Grue | 格魯 |  |
| Phyg / Phygs | 飛天豬 |  |
| Kappa Pick / Pickappa | Kappa鎬 | `Pickappa` 是原任務敘述使用的名稱 |
| Casull Cartridge / Casull | 卡蘇爾彈 |  |
| Armor | 護甲 |  |
| Quartz | 石英 |  |
| Guardian | 守護者 |  |
| Pulverizer | 粉碎機 | 與 IC2 的 Macerator 不同 |
| Macerator | 打粉機 | IndustrialCraft 2 機器 |
| Air Guardian | 風之守護者 | Ars Magicka 守護者 |
| Fire Guardian | 火之守護者 | Ars Magicka 守護者 |
| Igneous Extruder | 火成岩擠壓機 | Thermal Expansion 機器 |
| Glacial Precipitator | 冰川沉澱機 | Thermal Expansion 機器 |
| Counter | 流理臺 | Cooking for Blockheads 廚房方塊 |
| Blood Magic | 血魔法 |  |
| Life Essence | 生命源質 | Blood Magic 的生命源質 |
| Uncommon Rune | 罕見符文 | 泰坦符文任務的罕見階級 |
| Laser Drill Precharger / Prechargers | 雷射鑽機預充能器 | 僅用於實際雷射鑽機預充能器任務 |
| Flim Flam Flozzel | 花言巧語的騙子 | `Flozzel` 不再保留英文 |

## 刻意保留英文

### 模組、整合包與品牌名

`Craft of the Titans`、`Craft of Titans`、`CoTT`、`Better Questing`、
`EnderIO`、`Ender IO`、`AbyssalCraft`、`Ars Magica`、`Ars Magica 2`、`Ars Magicka`、
`MekFarm`、`Tinkers I/O`、`MineFactory`、`IndustrialCraft 2`、
`ArmorPlus`、`RFTools`、`Mob Grinding Utils`、`Steve's Carts`、
`iTank`、`Minecraft`、`Doom`、`YouTube`、`Old Spice`、`Vies`。

`Viesoline` 是 ViesCraft 的飛空艇燃料名稱，暫時保留原文。

### 單位、縮寫、介面與操作識別碼

`IC2`、`EU`、`EU/t`、`RF`、`RF/t`、`RF/T`、`GP`、`LP`、`LE`、`XP`、
`TPS`、`RPM`、`mB/t`、`UU`、`GUI`、`AI`、`JEI`、`NEI`、
`RS`、`BSU`、`SAG`、`CFB`、`I/O`、`OSS`、`Tesla`、`Shift`、
`MKI`、`MKII`。

帶數量前綴的 `M LP`、`k LP`、`k RF/t` 也按單位保留。

`Y40`、`Y60`、`Y230`、`X75` 等坐標，以及 `II`、`III`、`IV`、
`V`、`XX`、`XXX` 等等級標記也保留原格式。

`Boss` 與 `Bosses` 依現行翻譯規則保留英文。

### 角色、生物與故事專名

`Brahemic`、`Ju' Li Sioux`、`Aluna Mara`、`Asorah`、
`Silaqui Greyhawke`、`Cha'Garoth`、`Sactoth`、`Stakvik di jon`、
`Greater Tu' Nah`、`Jared`、`Pam`。

`Chagaroth`、`Ju' Li`、`Vies` 等縮寫或拼字變體，依其完整專名處理。

### 介面、物品與特殊名稱

`Levels GUI` 是 Levels 模組的介面名稱；`Kappa` 出現在使用者指定譯名
「Kappa鎬」中。兩者目前保留英文部分。

## 待人工確認的未漢化英文

| 英文片段 | 出現位置／目前處理 | 備註 |
|---|---|---|
| Phosphorous Mandate Sulfur Boilluon | 鑽石稀缺與壓縮煤炭的任務說明 | 原文疑似虛構化合物或刻意寫錯，暫不擅自翻譯 |
| Rogue | 「類《Rogue》地牢」 | 原文是 `Roguelike Dungeons`；需確認要保留遊戲／模組稱呼，或改成「類 Rogue 地牢」等譯名 |

## 特殊原文

- `FUS RO DAH!` 是《上古卷軸 V：無界天際》的龍吼語，保留原文。
- `O-oooooooooo AAAAE-A-A-I-A-U...` 是歌聲擬音，保留原格式。
- 召喚結構圖中的 `O`、`A`、`B`、`C`、`D`、`G`、`L`、`R`、`S`
  是 ASCII 圖案的一部分，不是漏翻。
