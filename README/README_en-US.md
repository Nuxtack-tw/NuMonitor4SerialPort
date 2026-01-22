# 🌐 Language / 語言

[繁體中文](../README.md) | [日本語](README_ja-JP.md) | [Français](README_fr-FR.md) | [Deutsch](README_de-DE.md) | [Italiano](README_it-IT.md) | [Español](README_es-ES.md) | [Português](README_pt-PT.md) | [Türkçe](README_tr-TR.md) | [Русский](README_ru-RU.md) | [العربية](README_ar-SA.md) | [עברית](README_he-IL.md) | [فارسی](README_fa-IR.md) | [हिन्दी](README_hi-IN.md) | [Tiếng Việt](README_vi-VN.md) | [ไทย](README_th-TH.md) | [Bahasa Melayu](README_ms-MY.md) | [Bahasa Indonesia](README_id-ID.md)

---

<div align="center">
  
  # NuMonitor for Serial Port
  
  **Professional Web Serial Port Monitoring and Data Visualization Tool**
  
  [![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Nuxtack-tw/NuMonitor4SerialPort/releases)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](../LICENSE)
  [![Browser](https://img.shields.io/badge/browser-Chrome%20%7C%20Edge%20%7C%20Opera-orange.svg)](#browser-support)
  [![Languages](https://img.shields.io/badge/languages-18-purple.svg)](#multi-language-support)
  
</div>

---

## 📖 Introduction

NuMonitor is a Serial Port monitoring tool designed for **Arduino/ESP32** developers, aimed at replacing the Arduino IDE Serial Monitor with enhanced features and better user experience.

### ✨ Key Features

- 🖥️ **Terminal Monitor** - Real-time serial data display with timestamps, auto-scroll, URL auto-detection
- 📊 **7 Chart Types** - Line, Area, Bar, Scatter, Pie, Gauge, Stacked Area charts
- 🗺️ **GPS Tracking** - OpenStreetMap integration for real-time GPS trajectory display
- 🎯 **X-Axis Cursor** - Mouse hover shows data point values instantly
- 🌐 **18 Languages** - Auto-detects browser language, supports RTL languages
- 📦 **Single File** - No installation required, download and use

---

## 🚀 Quick Start

### 1. Download

```bash
git clone https://github.com/Nuxtack-tw/NuMonitor4SerialPort.git
```

Or download the [latest release](https://github.com/Nuxtack-tw/NuMonitor4SerialPort/releases/latest)

### 2. Open

Open `NuMonitor4SerialPort.html` with Chrome, Edge, or Opera

### 3. Connect

1. Connect your Arduino/ESP32 via USB
2. Click "Select Port" button
3. Choose the corresponding COM Port
4. Start monitoring!

---

## 📊 Data Format

### Basic Format

```cpp
// Auto-naming (CH1, CH2, CH3)
Serial.println("25.5 60.2 1013.2");

// Key:Value format
Serial.println("Temp:25.5 Humidity:60.2 Pressure:1013.2");
```

### Full Format

```cpp
// {GroupName|YMin|YMax|ChartType}#counter Key1:Value1 Key2:Value2 map:lat,lng
Serial.println("{Environment|0|100|line}#1 Temp:25.5°C RH:60.2%");
```

### Chart Types

| Type | Code | Description |
|------|------|-------------|
| Line | `line` | Continuous data changes |
| Area | `area` | Emphasize quantity changes |
| Stacked | `stack` | Show composition ratios |
| Bar | `bar` | Category comparison |
| Scatter | `scatter` | XY coordinate distribution |
| Pie | `pie` | Proportion allocation |
| Gauge | `gauge` | Single value monitoring |

### GPS Tracking

```cpp
// Add map:lat,lng after data
Serial.print("{GPS|0|100|line}Speed:40.5km/h map:");
Serial.print(lat, 6);
Serial.print(",");
Serial.println(lng, 6);
```

---

## 💻 Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Google Chrome | 89+ | ✅ Recommended |
| Microsoft Edge | 89+ | ✅ Supported |
| Opera | 75+ | ✅ Supported |
| Firefox | - | ❌ Not supported |
| Safari | - | ❌ Not supported |

> ⚠️ NuMonitor uses Web Serial API, which is only supported in Chromium-based browsers.

---

## 📝 Version History

### v2.0.0 (2025-01-22)

**New Features**
- 🗺️ GPS map trajectory tracking
- 🎯 X-axis cursor for data points
- 🔗 Terminal URL auto-detection
- 📊 Stacked area chart
- 🔒 Map view lock
- 📖 HTML user manual

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details

---

<div align="center">
  
  **Made with ❤️ by [Nuxtack](https://github.com/Nuxtack)**
  
</div>
