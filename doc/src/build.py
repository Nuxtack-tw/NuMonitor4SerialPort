# -*- coding: utf-8 -*-
"""把 bodies/<doc>.<lang>.html 組裝成單檔多語文件。

用法：
    python build.py                 # 產出到本目錄下的 out/（試作用）
    python build.py <英文repo>/docs # 產出到英文版 repo，準備發佈

產出 manual.html 與 changelog.html：每個語言的正文包在
<div class="doc-lang" data-lang="xx">，同時只有一個帶 .active；
右上角固定一個語言選單，語言以 ?lang= → localStorage →
navigator.language → en-US 決定。

**要改文件內容就改 bodies/ 底下的檔案，再跑這支腳本重新組裝。
不要直接改產出的 manual.html / changelog.html，下次組裝就會被蓋掉。**
"""
import io, os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out')

# 順序即選單順序。zh-TW 不在本檔內，選到就跳去中文站。
LANGS = ['en-US', 'de-DE', 'fr-FR', 'es-ES', 'pt-PT', 'it-IT', 'tr-TR',
         'ja-JP', 'vi-VN', 'id-ID', 'ms-MY']
LANG_NAMES = {
    'en-US': 'English',
    'de-DE': 'Deutsch',
    'fr-FR': 'Français',
    'es-ES': 'Español',
    'pt-PT': 'Português',
    'it-IT': 'Italiano',
    'tr-TR': 'Türkçe',
    'ja-JP': '日本語',
    'vi-VN': 'Tiếng Việt',
    'id-ID': 'Bahasa Indonesia',
    'ms-MY': 'Bahasa Melayu',
}
ZH_BASE = 'https://nuxtack-tw.github.io/NuMonitor4SerialPort/doc/'

TITLES = {
    'manual': {
        'en-US': 'NuMonitor {V} — User Manual',
        'de-DE': 'NuMonitor {V} — Benutzerhandbuch',
        'fr-FR': "NuMonitor {V} — Manuel d'utilisation",
        'es-ES': 'NuMonitor {V} — Manual de usuario',
        'pt-PT': 'NuMonitor {V} — Manual do utilizador',
        'it-IT': 'NuMonitor {V} — Manuale utente',
        'tr-TR': 'NuMonitor {V} — Kullanım Kılavuzu',
        'ja-JP': 'NuMonitor {V} — ユーザーマニュアル',
        'vi-VN': 'NuMonitor {V} — Hướng dẫn sử dụng',
        'id-ID': 'NuMonitor {V} — Panduan Pengguna',
        'ms-MY': 'NuMonitor {V} — Panduan Pengguna',
    },
    'changelog': {
        'en-US': 'NuMonitor — Changelog',
        'de-DE': 'NuMonitor — Änderungsprotokoll',
        'fr-FR': 'NuMonitor — Journal des modifications',
        'es-ES': 'NuMonitor — Registro de cambios',
        'pt-PT': 'NuMonitor — Registo de alterações',
        'it-IT': 'NuMonitor — Registro delle modifiche',
        'tr-TR': 'NuMonitor — Değişiklik Günlüğü',
        'ja-JP': 'NuMonitor — 変更履歴',
        'vi-VN': 'NuMonitor — Nhật ký thay đổi',
        'id-ID': 'NuMonitor — Catatan Perubahan',
        'ms-MY': 'NuMonitor — Log Perubahan',
    },
}

VERSION = 'V26.12.0'

EXTRA_CSS = """
        /* ---- 單檔多語：一次只顯示一個語言區塊 ---- */
        .doc-lang { display: none; }
        .doc-lang.active { display: block; }

        .doc-langbar {
            position: fixed;
            top: 10px;
            right: 12px;
            z-index: 500;
        }

        .doc-langbar select {
            background: var(--bg-elevated);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 5px 26px 5px 10px;
            font-family: inherit;
            font-size: 0.85rem;
            cursor: pointer;
            appearance: none;
            background-image: linear-gradient(45deg, transparent 50%, var(--text-secondary) 50%),
                              linear-gradient(135deg, var(--text-secondary) 50%, transparent 50%);
            background-position: calc(100% - 14px) 52%, calc(100% - 9px) 52%;
            background-size: 5px 5px, 5px 5px;
            background-repeat: no-repeat;
        }

        .doc-langbar select:hover { border-color: var(--accent-blue); }
        .doc-langbar select:focus { outline: none; border-color: var(--accent-blue); }

        /* 尚無該語言版本時的提示條 */
        .doc-fallback-note {
            max-width: 900px;
            margin: 16px auto 0;
            padding: 10px 16px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-yellow);
            border-radius: 0 8px 8px 0;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        @media (max-width: 640px) {
            .doc-langbar { top: 6px; right: 6px; }
            .doc-langbar select { font-size: 0.8rem; padding: 4px 22px 4px 8px; }
        }
"""


def langbar_html(available):
    # 只列真的組進來的語言 —— 列出沒有正文的語言，選下去會整頁空白
    opts = []
    for code in available:
        opts.append('            <option value="%s">%s</option>' % (code, LANG_NAMES[code]))
    opts.append('            <option value="zh">繁體中文</option>')
    return (
        '    <div class="doc-langbar">\n'
        '        <select id="docLangSelect" aria-label="Document language">\n'
        + '\n'.join(opts) + '\n'
        '        </select>\n'
        '    </div>\n'
    )


SCRIPT = """    <script>
    (function () {
        // 文件語言：?lang= → localStorage → 瀏覽器語言 → en-US
        // 主程式（NuMonitor4SerialPort.html）連過來時會帶 ?lang=<介面語言>，
        // 帶的若是本檔沒有的語言（例如 de-DE），就退回英文並顯示提示條。
        var LANGS = %(langs)s;
        var TITLES = %(titles)s;
        var ZH_URL = %(zh)s;
        var KEY = 'numonitor_doc_lang';
        var sel = document.getElementById('docLangSelect');
        var requested = new URLSearchParams(location.search).get('lang');

        function resolve(code) {
            if (!code) return null;
            if (LANGS.indexOf(code) >= 0) return code;
            var base = code.split('-')[0];
            for (var i = 0; i < LANGS.length; i++) {
                if (LANGS[i].split('-')[0] === base) return LANGS[i];
            }
            return null;
        }

        function pick() {
            var cands = [requested];
            try { cands.push(localStorage.getItem(KEY)); } catch (e) {}
            cands.push(navigator.language);
            (navigator.languages || []).forEach(function (l) { cands.push(l); });
            for (var i = 0; i < cands.length; i++) {
                var hit = resolve(cands[i]);
                if (hit) return hit;
            }
            return 'en-US';
        }

        function apply(lang, remember) {
            var blocks = document.querySelectorAll('.doc-lang');
            for (var i = 0; i < blocks.length; i++) {
                blocks[i].classList.toggle('active', blocks[i].dataset.lang === lang);
            }
            document.documentElement.lang = lang;
            if (TITLES[lang]) document.title = TITLES[lang];
            sel.value = lang;
            if (remember) { try { localStorage.setItem(KEY, lang); } catch (e) {} }
            // 同語言的姊妹文件連結帶上 ?lang=，切過去不會又變回英文
            var links = document.querySelectorAll('a[data-sibling]');
            for (var j = 0; j < links.length; j++) {
                links[j].href = links[j].dataset.sibling + '?lang=' + lang;
            }
        }

        var active = pick();
        apply(active, false);

        // 主程式帶了語言過來、但本檔還沒有那個語言 → 說清楚為什麼看到英文
        if (requested && !resolve(requested) && active === 'en-US') {
            var note = document.createElement('div');
            note.className = 'doc-fallback-note';
            note.textContent = 'This document is not available in your language yet '
                + '(' + requested + '), so the English version is shown.';
            var host = document.querySelector('.doc-lang.active');
            if (host) host.insertBefore(note, host.firstChild);
        }

        sel.addEventListener('change', function () {
            if (sel.value === 'zh') { location.href = ZH_URL; return; }
            apply(sel.value, true);
            var url = new URL(location.href);
            url.searchParams.set('lang', sel.value);
            history.replaceState(null, '', url);
            window.scrollTo(0, 0);
        });
    })();
    </script>
"""


def build(doc, zh_file):
    head = io.open(os.path.join(HERE, '%s.head.html' % doc), encoding='utf-8').read()
    head = head.replace('    </style>', EXTRA_CSS + '    </style>', 1)

    titles = {}
    parts = []
    for code in LANGS:
        path = os.path.join(HERE, 'bodies', '%s.%s.html' % (doc, code))
        if not os.path.exists(path):
            continue
        body = io.open(path, encoding='utf-8').read()
        # 五個語言區塊同處一份文件，section id 會撞名，錨點會跳到隱藏區塊。
        # en-US 保留原始 id（外部連結 manual.html#faq 仍然有效），其餘語言加前綴。
        if code != 'en-US':
            body = re.sub(r'id="([\w-]+)"', 'id="%s--\\1"' % code, body)
            body = re.sub(r'href="#([\w-]+)"', 'href="#%s--\\1"' % code, body)
        parts.append('    <div class="doc-lang" data-lang="%s">\n%s\n    </div>\n' % (code, body))
        titles[code] = TITLES[doc][code].replace('{V}', VERSION)

    script = SCRIPT % {
        'langs': json.dumps([c for c in LANGS if c in titles]),
        'titles': json.dumps(titles, ensure_ascii=False),
        'zh': json.dumps(ZH_BASE + zh_file),
    }

    out = (head + '<body>\n' + langbar_html([c for c in LANGS if c in titles])
           + ''.join(parts) + script + '</body>\n</html>\n')
    dest = os.path.join(OUT, '%s.html' % doc)
    io.open(dest, 'w', encoding='utf-8', newline='').write(out)
    print('%-10s %2d 語言 %s  %6d bytes' % (doc, len(titles), ','.join(titles), len(out)))


if __name__ == '__main__':
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    build('manual', 'manual.html')
    build('changelog', 'changelog.html')
