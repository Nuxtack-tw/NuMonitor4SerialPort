# 🌐 Language / 語言

[English](README/README_en-US.md) | [日本語](README/README_ja-JP.md) | [Français](README/README_fr-FR.md) | [Deutsch](README/README_de-DE.md) | [Italiano](README/README_it-IT.md) | [Español](README/README_es-ES.md) | [Português](README/README_pt-PT.md) | [Türkçe](README/README_tr-TR.md) | [Русский](README/README_ru-RU.md) | [العربية](README/README_ar-SA.md) | [עברית](README/README_he-IL.md) | [فارسی](README/README_fa-IR.md) | [हिन्दी](README/README_hi-IN.md) | [Tiếng Việt](README/README_vi-VN.md) | [ไทย](README/README_th-TH.md) | [Bahasa Melayu](README/README_ms-MY.md) | [Bahasa Indonesia](README/README_id-ID.md)

---

<div align="center">
  <img src="https://raw.githubusercontent.com/Nuxtack-tw/NuMonitor4SerialPort/main/img/logo.svg" alt="NuMonitor Logo" width="120" height="120">
  
  # NuMonitor for Serial Port
  
  **專業的 Web Serial Port 監控與數據視覺化工具**
  
  [![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Nuxtack-tw/NuMonitor4SerialPort/releases)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  [![Browser](https://img.shields.io/badge/browser-Chrome%20%7C%20Edge%20%7C%20Opera-orange.svg)](#瀏覽器支援)
  [![Languages](https://img.shields.io/badge/languages-18-purple.svg)](#多語言支援)
  
  [線上展示](#) · [使用說明書](doc/manual.html) · [版本記錄](doc/changelog.html) · [回報問題](https://github.com/Nuxtack-tw/NuMonitor4SerialPort/issues)
  
</div>

---

## 📖 簡介

NuMonitor 是一款專為 **Arduino/ESP32** 開發者設計的 Serial Port 監控工具，旨在取代 Arduino IDE 的 Serial Monitor，提供更強大的功能和更好的使用體驗。

### ✨ 主要特色

- 🖥️ **終端機監控** - 即時顯示串口數據，支援時間戳記、自動捲動、URL 自動識別
- 📊 **7 種圖表類型** - 折線圖、面積圖、柱狀圖、散點圖、圓餅圖、儀表圖、堆疊圖
- 🗺️ **GPS 軌跡追蹤** - 整合 OpenStreetMap，即時顯示 GPS 移動軌跡
- 🎯 **X 軸遊標** - 滑鼠移動即時顯示數據點數值
- 🌐 **18 種語言** - 自動偵測瀏覽器語言，支援 RTL 語言
- 📦 **單一檔案** - 無需安裝，下載即可使用

---

## 🖼️ 截圖

<div align="center">
  <img src="https://raw.githubusercontent.com/Nuxtack-tw/NuMonitor4SerialPort/main/img/screenshot-terminal.png" alt="Terminal" width="45%">
  <img src="https://raw.githubusercontent.com/Nuxtack-tw/NuMonitor4SerialPort/main/img/screenshot-plotter.png" alt="Plotter" width="45%">
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/Nuxtack-tw/NuMonitor4SerialPort/main/img/screenshot-map.png" alt="GPS Map" width="45%">
  <img src="https://raw.githubusercontent.com/Nuxtack-tw/NuMonitor4SerialPort/main/img/screenshot-charts.png" alt="Charts" width="45%">
</div>

---

## 🚀 快速開始

### 1. 下載

```bash
git clone https://github.com/Nuxtack-tw/NuMonitor4SerialPort.git
```

或直接下載 [最新版本](https://github.com/Nuxtack-tw/NuMonitor4SerialPort/releases/latest)

### 2. 開啟

用 Chrome、Edge 或 Opera 開啟 `NuMonitor4SerialPort.html`

### 3. 連接裝置

1. 將 Arduino/ESP32 透過 USB 連接到電腦
2. 點擊「選擇連接埠」按鈕
3. 選擇對應的 COM Port
4. 開始監控！

---

## 📊 數據格式

### 基本格式

```cpp
// 自動命名 (CH1, CH2, CH3)
Serial.println("25.5 60.2 1013.2");

// Key:Value 格式
Serial.println("Temp:25.5 Humidity:60.2 Pressure:1013.2");
```

### 完整格式

```cpp
// {群組名稱|Y軸最小值|Y軸最大值|圖表類型}#計數器 Key1:Value1 Key2:Value2 map:緯度,經度
Serial.println("{Environment|0|100|line}#1 Temp:25.5°C RH:60.2%");
```

### 圖表類型

| 類型 | 代碼 | 說明 |
|------|------|------|
| 折線圖 | `line` | 連續數據變化 |
| 面積圖 | `area` | 強調數量變化 |
| 堆疊圖 | `stack` | 顯示組成比例 |
| 柱狀圖 | `bar` | 類別比較 |
| 散點圖 | `scatter` | XY 座標分布 |
| 圓餅圖 | `pie` | 比例分配 |
| 儀表圖 | `gauge` | 單一數值監控 |

### GPS 軌跡

```cpp
// 在數據後加上 map:緯度,經度
Serial.print("{GPS|0|100|line}Speed:40.5km/h map:");
Serial.print(lat, 6);
Serial.print(",");
Serial.println(lng, 6);
```

---

## 🌐 多語言支援

| 語言 | 代碼 | 語言 | 代碼 |
|------|------|------|------|
| 繁體中文 | zh-TW | Türkçe | tr-TR |
| English | en-US | العربية | ar-SA |
| 日本語 | ja-JP | עברית | he-IL |
| Français | fr-FR | فارسی | fa-IR |
| Deutsch | de-DE | Русский | ru-RU |
| Italiano | it-IT | हिन्दी | hi-IN |
| Español | es-ES | Tiếng Việt | vi-VN |
| Português | pt-PT | ไทย | th-TH |
| Bahasa Melayu | ms-MY | Bahasa Indonesia | id-ID |

---

## 💻 瀏覽器支援

| 瀏覽器 | 版本 | 狀態 |
|--------|------|------|
| Google Chrome | 89+ | ✅ 推薦 |
| Microsoft Edge | 89+ | ✅ 支援 |
| Opera | 75+ | ✅ 支援 |
| Firefox | - | ❌ 不支援 |
| Safari | - | ❌ 不支援 |

> ⚠️ NuMonitor 使用 Web Serial API，此 API 僅在 Chromium 核心的瀏覽器上支援。

---

## 📁 專案結構

```
NuMonitor4SerialPort/
├── NuMonitor4SerialPort.html    # 主程式
├── NuMonitor4SerialPort.ino     # Arduino 展示程式
├── doc/
│   ├── manual.html              # 使用說明書
│   └── changelog.html           # 版本記錄
├── docs/
│   └── TECHNICAL.md             # 技術文件
├── README/
│   └── [各語言 README]
├── .claude/
│   └── skills/
│       └── NuMonitor_SKILL.md   # 專案技能檔
├── LICENSE
└── README.md
```

---

## 🔧 開發

### 技術棧

- **前端**: 純 HTML5 + CSS3 + JavaScript (ES6+)
- **API**: Web Serial API
- **地圖**: Leaflet.js + OpenStreetMap
- **架構**: 單一檔案應用程式 (SFA)

### 本地開發

由於使用 Web Serial API，需要透過本地伺服器或 `file://` 協議開啟：

```bash
# 使用 Python 啟動本地伺服器
python -m http.server 8080

# 或使用 Node.js
npx serve
```

---

## 📝 版本歷史

### v2.0.0 (2025-01-22)

**新功能**
- 🗺️ GPS 地圖軌跡追蹤
- 🎯 X 軸遊標顯示數據點
- 🔗 終端機 URL 自動識別
- 📊 堆疊面積圖
- 🔒 地圖視界鎖定
- 📖 HTML 使用說明書

查看完整 [版本記錄](doc/changelog.html)

---

## 🤝 貢獻

歡迎提交 Pull Request 或回報問題！

1. Fork 本專案
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

---

## 📄 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案

---

## 🙏 致謝

- [Leaflet.js](https://leafletjs.com/) - 地圖函式庫
- [OpenStreetMap](https://www.openstreetmap.org/) - 地圖圖資
- [JetBrains Mono](https://www.jetbrains.com/lp/mono/) - 等寬字體

---

<div align="center">
  
  **Made with ❤️ by [Nuxtack](https://github.com/Nuxtack)**
  
  ⭐ 如果這個專案對您有幫助，請給我們一顆星！
  
</div>
