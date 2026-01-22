# NuMonitor for Serial Port - 技術說明文件

## 1. 系統架構

### 1.1 整體架構圖

```
┌────────────────────────────────────────────────────────────────────────┐
│                           NuMonitor v2.0.0                             │
├────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Header    │  │  Terminal   │  │   Plotter   │  │  Language   │    │
│  │  (連接控制)  │  │  (終端機)   │  │  (繪圖器)    │  │  (多語言)   │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                │                │                │           │
│  ┌──────▼──────────────────────────────────────────────────▼──────┐    │
│  │                     SerialMonitor (主控制器)                    │    │
│  │  ┌─────────────┐  ┌─────────────┐   ┌─────────────────────┐    │    │
│  │  │SerialManager│  │TerminalMgr  │   │   PlotterManager    │    │    │
│  │  │ (Web Serial)│  │ (輸出顯示)   │   │  ┌───────────────┐  │    │    │
│  │  └─────────────┘  └─────────────┘   │  │PlotterParser  │  │    │    │
│  │                                     │  │ (數據解析)     │  │    │    │
│  │                                     │  ├───────────────┤  │    │    │
│  │                                     │  │ ChartManager  │  │    │    │
│  │                                     │  │ (圖表渲染)     │  │    │    │
│  │                                     │  ├───────────────┤  │    │    │
│  │                                     │  │ ColorManager  │  │    │    │
│  │                                     │  │ (顏色管理)     │  │    │    │
│  │                                     │  └───────────────┘  │    │    │
│  │                                     └─────────────────────┘    │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        外部相依                                  │   │
│  │  • Leaflet.js 1.9.4 (地圖)  • OpenStreetMap (圖資)               │   │
│  │  • Google Fonts (Rubik)     • Web Serial API                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.2 檔案結構

```
NuMonitor/
├── NuMonitor4SerialPort.html    # 主程式 (單一檔案，包含所有功能)
├── NuMonitor4SerialPort.ino     # Arduino 展示程式
├── doc/
│   ├── manual.html              # 使用說明書
│   └── changelog.html           # 版本變更記錄
├── docs/
│   └── TECHNICAL.md             # 技術說明文件 (本文件)
├── README/
│   ├── README_en-US.md          # English
│   ├── README_ja-JP.md          # 日本語
│   └── ...                      # 其他語言
└── README.md                    # 主要說明文件 (繁體中文)
```

---

## 2. Web Serial API 整合

### 2.1 連接流程

```javascript
async connectToPort() {
    // 1. 請求使用者選擇連接埠
    const port = await navigator.serial.requestPort();
    
    // 2. 開啟連接埠
    await port.open({
        baudRate: this.baudRate,
        dataBits: 8,
        stopBits: 1,
        parity: 'none',
        flowControl: 'none'
    });
    
    // 3. 取得讀取器
    this.reader = port.readable.getReader();
    
    // 4. 開始讀取迴圈
    this.readLoop();
}
```

### 2.2 ESP32 USB CDC 相容性處理

ESP32 使用 USB CDC (Communications Device Class) 時，斷開後重新連接需要重新取得 SerialPort 物件：

```javascript
async reconnect() {
    // 關閉現有連接
    if (this.reader) {
        await this.reader.cancel();
        this.reader.releaseLock();
    }
    if (this.port) {
        await this.port.close();
    }
    
    // 重要：必須重新 requestPort()，不能重用舊的 port 物件
    this.port = await navigator.serial.requestPort();
    await this.port.open({ baudRate: this.baudRate });
}
```

### 2.3 讀取迴圈

```javascript
async readLoop() {
    const decoder = new TextDecoder();
    let buffer = '';
    
    while (true) {
        const { value, done } = await this.reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        
        // 處理完整行
        const lines = buffer.split('\n');
        buffer = lines.pop(); // 保留不完整的部分
        
        for (const line of lines) {
            this.processLine(line.trim());
        }
    }
}
```

---

## 3. 數據解析引擎 (PlotterParser)

### 3.1 解析流程圖

```
輸入: "{Temperature|0|100|line}#1 Temp:25.5°C RH:60% map:25.04,121.51"
                    │
                    ▼
        ┌───────────────────────┐
        │  解析群組設定          │
        │  {Name|min|max|type}  │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  解析計數器            │
        │  #counter             │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  解析數據點            │
        │  Key:ValueUnit        │
        │  → 提取數值            │
        │  → 保留原始字串        │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  解析座標 (可選)       │
        │  map:lat,lng          │
        │  → 支援多種格式        │
        └───────────┬───────────┘
                    │
                    ▼
輸出: {
    groupName: "Temperature",
    chartType: "line",
    yMin: 0, yMax: 100,
    counter: 1,
    dataPoints: [
        { label: "Temp", value: 25.5, rawValue: "25.5°C" },
        { label: "RH", value: 60, rawValue: "60%" }
    ],
    mapCoord: { lat: 25.04, lng: 121.51 }
}
```

### 3.2 數值提取正則

```javascript
extractNumber(str) {
    // 匹配開頭的數值部分（包含負號和小數點）
    const match = str.match(/^(-?\d+\.?\d*)/);
    return match ? parseFloat(match[1]) : NaN;
}
```

### 3.3 座標解析

```javascript
parseCoordinate(coordStr) {
    // 格式 1: 十進位度 (DD)
    // 25.039684,121.512357 或 25.039684N,121.512357E
    
    // 格式 2: 度分 (DM)
    // 25°2.381'N,121°30.741'E
    
    // 格式 3: 度分秒 (DMS)
    // 25°2'22.9"N,121°30'44.5"E
    
    // 統一轉換為十進位度
    return { lat, lng };
}
```

---

## 4. 圖表渲染系統 (ChartManager)

### 4.1 圖表類別繼承

```
BaseChart (抽象基類)
├── LineChart      (折線圖)
│   └── drawCursor()  // X軸遊標
├── AreaChart      (面積圖)
│   └── drawCursor()
├── StackedAreaChart (堆疊面積圖)
│   └── drawCursor()
├── BarChart       (柱狀圖)
├── ScatterChart   (散點圖)
├── PieChart       (圓餅圖)
└── GaugeChart     (儀表圖)
```

### 4.2 渲染流程

```javascript
renderChart(group) {
    const ctx = group.canvas.getContext('2d');
    
    // 1. 清除畫布
    ctx.clearRect(0, 0, width, height);
    
    // 2. 繪製背景
    ctx.fillStyle = group.bgColor;
    ctx.fillRect(0, 0, width, height);
    
    // 3. 計算比例尺
    const scale = this.calculateScale(group);
    
    // 4. 繪製網格
    this.drawGrid(ctx, scale);
    
    // 5. 繪製數據
    this.drawData(ctx, group, scale);
    
    // 6. 繪製遊標 (如果有)
    if (group.cursorX !== null) {
        this.drawCursor(ctx, group, scale);
    }
}
```

### 4.3 X軸遊標實作

```javascript
drawCursor(ctx, group, scale) {
    const { cursorX, counters, series } = group;
    
    // 1. 計算最近的數據點索引
    const index = Math.round(cursorX / pointSpacing);
    
    // 2. 繪製垂直線
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
    ctx.stroke();
    
    // 3. 繪製數值標籤
    const labels = [];
    if (counters[index]) {
        labels.push(`#${counters[index]}`);
    }
    for (const [label, values] of Object.entries(series)) {
        labels.push(`${label}: ${values[index].toFixed(2)}`);
    }
    
    // 4. 繪製標籤背景和文字
    this.drawCursorLabels(ctx, labels, x, y);
}
```

---

## 5. 地圖整合 (Leaflet.js)

### 5.1 動態載入

```javascript
async loadLeaflet() {
    if (window.L) return; // 已載入
    
    // 載入 CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(link);
    
    // 載入 JS
    return new Promise((resolve) => {
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
        script.onload = resolve;
        document.head.appendChild(script);
    });
}
```

### 5.2 地圖初始化

```javascript
initMap(group) {
    const map = L.map(container).setView([lat, lng], 16);
    
    // 圖層
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);
    
    // 軌跡線
    group.trackLine = L.polyline([], {
        color: '#58a6ff',
        weight: 3,
        opacity: 0.8
    }).addTo(map);
    
    // 標記圖層
    group.trackMarkers = L.layerGroup().addTo(map);
    
    group.leafletMap = map;
}
```

### 5.3 軌跡更新

```javascript
renderMap(group) {
    // 更新軌跡線
    const latLngs = group.mapPoints.map(p => [p.lat, p.lng]);
    group.trackLine.setLatLngs(latLngs);
    
    // 更新標記
    group.trackMarkers.clearLayers();
    group.mapPoints.forEach((point, idx) => {
        const isLast = idx === group.mapPoints.length - 1;
        const marker = L.circleMarker([point.lat, point.lng], {
            radius: isLast ? 8 : 4,
            fillColor: isLast ? '#f85149' : '#58a6ff'
        });
        
        // Tooltip (包含數據點)
        marker.bindTooltip(this.buildTooltip(point));
        group.trackMarkers.addLayer(marker);
    });
    
    // 移動視圖 (除非鎖定)
    if (!group.mapLocked) {
        const lastPoint = group.mapPoints[group.mapPoints.length - 1];
        group.leafletMap.panTo([lastPoint.lat, lastPoint.lng]);
    }
}
```

---

## 6. 多語言系統 (LanguageManager)

### 6.1 翻譯機制

```javascript
class LanguageManager {
    constructor() {
        this.translations = {
            'zh-TW': { /* 繁體中文翻譯 */ },
            'en-US': { /* 英文翻譯 */ },
            // ... 其他語言
        };
        this.currentLang = this.detectLanguage();
    }
    
    detectLanguage() {
        // 1. 檢查 localStorage
        const saved = localStorage.getItem('numonitor_language');
        if (saved && this.translations[saved]) return saved;
        
        // 2. 檢查瀏覽器語言
        const browserLang = navigator.language;
        if (this.translations[browserLang]) return browserLang;
        
        // 3. 嘗試匹配語系
        const langCode = browserLang.split('-')[0];
        for (const lang of Object.keys(this.translations)) {
            if (lang.startsWith(langCode)) return lang;
        }
        
        // 4. 預設繁體中文
        return 'zh-TW';
    }
    
    t(key) {
        return this.translations[this.currentLang][key] 
            || this.translations['zh-TW'][key] 
            || key;
    }
}
```

### 6.2 DOM 更新

```javascript
updateUI() {
    // 更新 data-i18n 屬性的元素
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.textContent = this.t(key);
    });
    
    // 更新 data-i18n-tip 屬性的元素
    document.querySelectorAll('[data-i18n-tip]').forEach(el => {
        const key = el.getAttribute('data-i18n-tip');
        el.setAttribute('data-tip', this.t(key));
    });
    
    // RTL 語言處理
    if (['ar-SA', 'he-IL', 'fa-IR'].includes(this.currentLang)) {
        document.body.setAttribute('dir', 'rtl');
    } else {
        document.body.removeAttribute('dir');
    }
}
```

---

## 7. 效能優化

### 7.1 Canvas 渲染優化

```javascript
// 使用 requestAnimationFrame 節流
let pendingRender = false;
function scheduleRender(group) {
    if (pendingRender) return;
    pendingRender = true;
    requestAnimationFrame(() => {
        renderChart(group);
        pendingRender = false;
    });
}

// 離屏 Canvas (大量數據時)
const offscreenCanvas = document.createElement('canvas');
const offscreenCtx = offscreenCanvas.getContext('2d');
```

### 7.2 數據管理

```javascript
// 限制數據點數量
const MAX_POINTS = 2000;
while (series.length > MAX_POINTS) {
    series.shift();
}

// 地圖點數獨立控制 (1-100)
while (mapPoints.length > mapMaxPoints) {
    mapPoints.shift();
}
```

### 7.3 事件節流

```javascript
// 滑鼠移動事件節流
let lastMoveTime = 0;
canvas.addEventListener('mousemove', (e) => {
    const now = Date.now();
    if (now - lastMoveTime < 16) return; // ~60fps
    lastMoveTime = now;
    handleMouseMove(e);
});
```

---

## 8. 安全考量

### 8.1 URL 處理 (防 XSS)

```javascript
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function linkifyUrls(text) {
    // 先轉義 HTML
    const escaped = escapeHtml(text);
    
    // 再處理 URL
    return escaped.replace(urlRegex, (url) => {
        const href = url.startsWith('www.') ? 'https://' + url : url;
        return `<a href="${href}" target="_blank" rel="noopener">${url}</a>`;
    });
}
```

### 8.2 localStorage 存取

```javascript
function safeGetItem(key, defaultValue) {
    try {
        const value = localStorage.getItem(key);
        return value !== null ? value : defaultValue;
    } catch (e) {
        console.warn('localStorage access denied:', e);
        return defaultValue;
    }
}
```

---

## 9. 瀏覽器相容性

### 9.1 Web Serial API 支援

| 瀏覽器 | 版本 | 支援狀態 |
|--------|------|----------|
| Chrome | 89+ | ✅ 完整支援 |
| Edge | 89+ | ✅ 完整支援 |
| Opera | 75+ | ✅ 完整支援 |
| Firefox | - | ❌ 不支援 |
| Safari | - | ❌ 不支援 |

### 9.2 特性檢測

```javascript
function checkCompatibility() {
    if (!('serial' in navigator)) {
        showError('browser.unsupported', 
            'Web Serial API is not supported. Please use Chrome, Edge, or Opera.');
        return false;
    }
    return true;
}
```

---

## 10. 除錯指南

### 10.1 Console 日誌

```javascript
// 開發模式日誌
const DEBUG = false;
function log(...args) {
    if (DEBUG) console.log('[NuMonitor]', ...args);
}

// 數據解析日誌
log('[Parser] Input:', line);
log('[Parser] Output:', parsed);

// 圖表渲染日誌
log('[Chart] Rendering:', group.name, 'Points:', series.length);
```

### 10.2 常見問題排查

| 問題 | 可能原因 | 解決方案 |
|------|----------|----------|
| 連接埠看不到 | 驅動程式未安裝 | 安裝 USB 驅動 |
| 收到亂碼 | 鮑率不匹配 | 調整鮑率設定 |
| 圖表不出現 | 數據格式錯誤 | 檢查 Key:Value 格式 |
| 地圖不顯示 | 無網路連線 | 確認可連接 OSM |
| ESP32 斷線 | USB CDC 問題 | 重新選擇連接埠 |

---

## 授權資訊

NuMonitor for Serial Port © 2025 Nuwa Robotics

Licensed under MIT License
