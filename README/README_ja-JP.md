# 🌐 Language / 言語

[繁體中文](../README.md) | [English](README_en-US.md) | [Français](README_fr-FR.md) | [Deutsch](README_de-DE.md) | [Italiano](README_it-IT.md) | [Español](README_es-ES.md) | [Português](README_pt-PT.md) | [Türkçe](README_tr-TR.md) | [Русский](README_ru-RU.md) | [العربية](README_ar-SA.md) | [עברית](README_he-IL.md) | [فارسی](README_fa-IR.md) | [हिन्दी](README_hi-IN.md) | [Tiếng Việt](README_vi-VN.md) | [ไทย](README_th-TH.md) | [Bahasa Melayu](README_ms-MY.md) | [Bahasa Indonesia](README_id-ID.md)

---

<div align="center">
  
  # NuMonitor for Serial Port
  
  **プロフェッショナルなWeb シリアルポート監視・データ可視化ツール**
  
  [![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Nuxtack-tw/NuMonitor4SerialPort/releases)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](../LICENSE)
  [![Browser](https://img.shields.io/badge/browser-Chrome%20%7C%20Edge%20%7C%20Opera-orange.svg)](#ブラウザサポート)
  [![Languages](https://img.shields.io/badge/languages-18-purple.svg)](#多言語サポート)
  
</div>

---

## 📖 概要

NuMonitor は **Arduino/ESP32** 開発者向けに設計されたシリアルポート監視ツールです。Arduino IDE のシリアルモニターを置き換え、より強力な機能と優れたユーザーエクスペリエンスを提供します。

### ✨ 主な機能

- 🖥️ **ターミナル監視** - リアルタイムシリアルデータ表示、タイムスタンプ、自動スクロール、URL自動検出
- 📊 **7種類のチャート** - 折れ線、面積、棒、散布、円、ゲージ、積み上げ面積グラフ
- 🗺️ **GPS追跡** - OpenStreetMap統合によるリアルタイムGPS軌跡表示
- 🎯 **X軸カーソル** - マウスホバーでデータポイント値を即時表示
- 🌐 **18言語対応** - ブラウザ言語自動検出、RTL言語サポート
- 📦 **単一ファイル** - インストール不要、ダウンロードしてすぐ使用可能

---

## 🚀 クイックスタート

### 1. ダウンロード

```bash
git clone https://github.com/Nuxtack-tw/NuMonitor4SerialPort.git
```

または[最新リリース](https://github.com/Nuxtack-tw/NuMonitor4SerialPort/releases/latest)をダウンロード

### 2. 開く

Chrome、Edge、または Opera で `NuMonitor4SerialPort.html` を開く

### 3. 接続

1. Arduino/ESP32 を USB で接続
2. 「ポートを選択」ボタンをクリック
3. 対応する COM ポートを選択
4. 監視開始！

---

## 📊 データ形式

### 基本形式

```cpp
// 自動命名 (CH1, CH2, CH3)
Serial.println("25.5 60.2 1013.2");

// Key:Value 形式
Serial.println("Temp:25.5 Humidity:60.2 Pressure:1013.2");
```

### 完全形式

```cpp
// {グループ名|Y軸最小|Y軸最大|チャートタイプ}#カウンター Key1:Value1 Key2:Value2 map:緯度,経度
Serial.println("{Environment|0|100|line}#1 Temp:25.5°C RH:60.2%");
```

### チャートタイプ

| タイプ | コード | 説明 |
|--------|--------|------|
| 折れ線 | `line` | 連続データ変化 |
| 面積 | `area` | 数量変化を強調 |
| 積み上げ | `stack` | 構成比を表示 |
| 棒 | `bar` | カテゴリ比較 |
| 散布 | `scatter` | XY座標分布 |
| 円 | `pie` | 比率配分 |
| ゲージ | `gauge` | 単一値監視 |

---

## 💻 ブラウザサポート

| ブラウザ | バージョン | 状態 |
|----------|------------|------|
| Google Chrome | 89+ | ✅ 推奨 |
| Microsoft Edge | 89+ | ✅ サポート |
| Opera | 75+ | ✅ サポート |
| Firefox | - | ❌ 非サポート |
| Safari | - | ❌ 非サポート |

> ⚠️ NuMonitor は Web Serial API を使用しており、Chromium ベースのブラウザでのみサポートされています。

---

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています - 詳細は [LICENSE](../LICENSE) ファイルをご覧ください

---

<div align="center">
  
  **Made with ❤️ by [Nuxtack](https://github.com/Nuxtack)**
  
</div>
