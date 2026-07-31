# 多語文件建置原始碼

英文版 repo（`Nuxtack/NuMonitor4SerialPort`）的 `docs/manual.html` 與 `docs/changelog.html`
是**組裝產物**，來源在這個目錄。

## 為什麼要有這一層

那兩份文件各自裝了五種語言的正文（English / 日本語 / Tiếng Việt / Bahasa Indonesia /
Bahasa Melayu），單檔約 150–175KB。直接手改產出檔會有兩個問題：

1. 五份正文共用同一組 CSS 與語言切換腳本，改一處要同步五次
2. 各語言區塊的 `section id` 需要加前綴才不會撞名，那是腳本做的，手改會漏

## 檔案

| 路徑 | 內容 |
|---|---|
| `build.py` | 組裝腳本；語言清單、選單名稱、頁面標題、額外 CSS 與切換邏輯都在裡面 |
| `manual.head.html` | 說明書的 `<head>`（含約 415 行 CSS），五種語言共用 |
| `changelog.head.html` | 變更記錄的 `<head>`，同上 |
| `bodies/<doc>.<lang>.html` | 各語言的 `<body>` 正文，**要改內容就改這裡** |

## 用法

```bash
# 試作：產出到 doc/src/out/
python build.py

# 發佈：產出到英文 repo
python build.py <英文repo路徑>/docs
```

## 加一種語言

1. 複製 `bodies/manual.en-US.html` → `bodies/manual.<語言碼>.html`，翻譯內容
2. changelog 同樣做一份
3. `build.py` 的 `LANGS` 加上語言碼，`LANG_NAMES` 與 `TITLES` 補上對應名稱
4. 跑 `build.py`

**主程式不必動。** `LanguageManager.updateDocLinks()` 只負責把 `?lang=<介面語言>`
帶過去，要顯示哪一版、認不得時怎麼退回，全由文件端自己決定。

## 改完要檢查

- 五份正文的 HTML 標籤數必須一致（標籤數不同 = 有漏標籤或漏段落）
- 各語言的版本號與日期序列必須與英文完全相同
- 導覽列每個 `href="#x"` 都要在同一個語言區塊內找得到對應的 `id`
- 產出檔在瀏覽器裡切過每一種語言，確認同時只有一個 `.doc-lang.active`

## 已知缺口

翻譯版說明書內嵌的 17 張截圖仍是英文介面。
