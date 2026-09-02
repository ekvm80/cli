"""
Markdown -> 단일 HTML 변환기 (자체 완결형)

사용법:
    py md_to_html.py 입력.md 출력.html [--lang ko|en] [--alt 대체언어파일명]
                     [--nav "라벨=파일명,라벨=파일명"] [--nav-current 라벨]

특징
- 외부 CSS/JS/폰트를 전혀 불러오지 않는다. 인터넷 없이도 열린다.
- 좌측 목차(TOC) 자동 생성, 모바일에서는 상단 접이식 목차로 전환.
- 코드 블록마다 '복사' 버튼 추가 (초보자가 명령어를 그대로 복사할 수 있도록).
- 배경 테마 3종(밝게/어둡게/편하게) 전환 버튼. 선택은 브라우저에 저장된다.
- --alt 를 주면 한국어/영어 전환 버튼을 사이드바 상단에 넣는다.
"""

import sys
import re
from pathlib import Path

import markdown


# --------------------------------------------------------------------------
# HTML 템플릿
# --------------------------------------------------------------------------
TEMPLATE = """<!DOCTYPE html>
<html lang="__LANG__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root {
  --bg: #ffffff;
  --bg-soft: #f6f7f9;
  --bg-code: #f4f5f7;
  --fg: #1f2328;
  --fg-soft: #59636e;
  --border: #d8dde3;
  --accent: #b5502a;
  --accent-soft: #fdf3ef;
  --note-bg: #f2f7fd;
  --note-border: #7ba7d7;
  --warn-bg: #fdf6ec;
  --warn-border: #d9a13b;
  --sidebar-w: 300px;
  --maxw: 860px;
}
/* 시스템 설정을 따르되, 사용자가 직접 고른 값이 있으면 그쪽이 이긴다. */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) {
    --bg: #16181c;
    --bg-soft: #1e2126;
    --bg-code: #22262c;
    --fg: #e3e6ea;
    --fg-soft: #9aa3ad;
    --border: #333941;
    --accent: #e08b63;
    --accent-soft: #2a211d;
    --note-bg: #1b2530;
    --note-border: #3f6a99;
    --warn-bg: #2b2418;
    --warn-border: #8a6a2b;
  }
}
/* 어둡게 */
:root[data-theme="dark"] {
  --bg: #16181c;
  --bg-soft: #1e2126;
  --bg-code: #22262c;
  --fg: #e3e6ea;
  --fg-soft: #9aa3ad;
  --border: #333941;
  --accent: #e08b63;
  --accent-soft: #2a211d;
  --note-bg: #1b2530;
  --note-border: #3f6a99;
  --warn-bg: #2b2418;
  --warn-border: #8a6a2b;
}
/* 편하게 보기 — 눈부심을 줄인 따뜻한 배경 */
:root[data-theme="sepia"] {
  --bg: #f5ecd9;
  --bg-soft: #efe4cd;
  --bg-code: #ece0c6;
  --fg: #3a322a;
  --fg-soft: #6d6252;
  --border: #ddd0b6;
  --accent: #a04a1f;
  --accent-soft: #f8e9d9;
  --note-bg: #e6ebec;
  --note-border: #8aa2b5;
  --warn-bg: #f6e6c8;
  --warn-border: #c69a45;
}

* { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: "Pretendard", "Pretendard Variable", -apple-system,
               BlinkMacSystemFont, "Segoe UI", "Malgun Gothic", "맑은 고딕",
               "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
  font-size: 16.5px;
  line-height: 1.75;
  -webkit-text-size-adjust: 100%;
  word-break: keep-all;
  overflow-wrap: break-word;
}

/* ---------- 레이아웃 ---------- */
.layout { display: flex; align-items: flex-start; }

#sidebar {
  width: var(--sidebar-w);
  flex: 0 0 var(--sidebar-w);
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  border-right: 1px solid var(--border);
  background: var(--bg-soft);
  padding: 28px 18px 60px 24px;
}
#sidebar .toc-title {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--fg-soft);
  text-transform: uppercase;
  margin-bottom: 14px;
}
#sidebar ul { list-style: none; margin: 0; padding: 0; }
#sidebar ul ul { padding-left: 13px; }
#sidebar li { margin: 1px 0; }
#sidebar a {
  display: block;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.855rem;
  line-height: 1.45;
  color: var(--fg-soft);
  text-decoration: none;
  border-left: 2px solid transparent;
}
#sidebar a:hover { background: var(--accent-soft); color: var(--accent); }
#sidebar a.active {
  color: var(--accent);
  font-weight: 600;
  border-left-color: var(--accent);
  background: var(--accent-soft);
}
/* 1단계 항목(부 제목)은 굵게 */
#sidebar > .toc > ul > li > a { font-weight: 600; color: var(--fg); font-size: 0.9rem; }
.lang-switch {
  display: flex;
  gap: 4px;
  margin: 0 0 14px;
  padding: 3px;
  border: 1px solid var(--border);
  border-radius: 7px;
  background: var(--bg-soft);
}
.lang-switch a, .lang-switch span {
  flex: 1 1 0;
  text-align: center;
  padding: 5px 0;
  font-size: 0.8rem;
  font-weight: 600;
  border-radius: 5px;
  text-decoration: none;
  line-height: 1.2;
}
.lang-switch span { background: var(--accent); color: #fff; }
.lang-switch a { color: var(--fg-soft); }
.lang-switch a:hover { background: var(--accent-soft); color: var(--accent); }
.doc-nav {
  margin: 0 0 14px;
  padding: 8px 9px 9px;
  border: 1px solid var(--border);
  border-radius: 7px;
  background: var(--bg-soft);
}
.doc-nav .doc-nav-title {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--fg-soft);
  margin-bottom: 5px;
}
.doc-nav a, .doc-nav span {
  display: block;
  padding: 4px 7px;
  font-size: 0.8rem;
  border-radius: 5px;
  text-decoration: none;
  line-height: 1.35;
}
.doc-nav span { background: var(--accent); color: #fff; font-weight: 600; }
.doc-nav a { color: var(--fg-soft); }
.doc-nav a:hover { background: var(--accent-soft); color: var(--accent); }
.theme-switch {
  margin: 0 0 16px;
  padding: 8px 9px 9px;
  border: 1px solid var(--border);
  border-radius: 7px;
  background: var(--bg-soft);
}
.theme-switch-title {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--fg-soft);
  margin-bottom: 5px;
}
.theme-switch-row { display: flex; gap: 4px; }
.theme-switch button {
  flex: 1 1 0;
  padding: 5px 2px;
  font: inherit;
  font-size: 0.74rem;
  font-weight: 600;
  line-height: 1.2;
  color: var(--fg-soft);
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 5px;
  cursor: pointer;
}
.theme-switch button:hover { color: var(--accent); border-color: var(--accent); }
.theme-switch button[aria-pressed="true"] {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

main {
  flex: 1 1 auto;
  min-width: 0;
  padding: 46px 40px 120px;
  display: flex;
  justify-content: center;
}
.content { width: 100%; max-width: var(--maxw); }

/* ---------- 타이포그래피 ---------- */
h1, h2, h3, h4 { line-height: 1.35; font-weight: 700; scroll-margin-top: 20px; }
h1 {
  font-size: 2.05rem;
  margin: 0 0 0.6em;
  padding-bottom: 0.35em;
  border-bottom: 3px solid var(--accent);
}
h2 {
  font-size: 1.5rem;
  margin: 2.6em 0 0.8em;
  padding-bottom: 0.3em;
  border-bottom: 1px solid var(--border);
}
h3 { font-size: 1.16rem; margin: 2em 0 0.6em; color: var(--accent); }
h4 { font-size: 1.02rem; margin: 1.6em 0 0.5em; }
p { margin: 0.85em 0; }
a { color: var(--accent); }

hr {
  border: 0;
  border-top: 1px solid var(--border);
  margin: 3em 0;
}

ul, ol { padding-left: 1.4em; margin: 0.8em 0; }
li { margin: 0.32em 0; }
li > ul, li > ol { margin: 0.3em 0; }

strong { font-weight: 700; }

/* ---------- 표 ---------- */
.table-wrap { overflow-x: auto; margin: 1.4em 0; }
table {
  border-collapse: collapse;
  width: 100%;
  font-size: 0.93rem;
}
th, td {
  border: 1px solid var(--border);
  padding: 9px 13px;
  text-align: left;
  vertical-align: top;
}
th { background: var(--bg-soft); font-weight: 700; white-space: nowrap; }
tbody tr:nth-child(even) td { background: color-mix(in srgb, var(--bg-soft) 45%, transparent); }

/* ---------- 코드 ---------- */
code {
  font-family: "Cascadia Mono", "Consolas", "D2Coding", "Menlo", monospace;
  font-size: 0.88em;
}
p code, li code, td code, th code {
  background: var(--bg-code);
  border: 1px solid var(--border);
  border-radius: 5px;
  padding: 1px 5px;
}
.codeblock { position: relative; margin: 1.15em 0; }
.codeblock pre {
  margin: 0;
  background: var(--bg-code);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px 60px 14px 16px;
  overflow-x: auto;
  line-height: 1.6;
}
.codeblock pre code { background: none; border: 0; padding: 0; font-size: 0.9rem; }
.copy-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--fg-soft);
  border-radius: 6px;
  padding: 3px 9px;
  font-size: 0.74rem;
  cursor: pointer;
  opacity: 0;
  transition: opacity .15s;
  font-family: inherit;
}
.codeblock:hover .copy-btn, .copy-btn:focus { opacity: 1; }
.copy-btn:hover { color: var(--accent); border-color: var(--accent); }
.copy-btn.done { color: #2f8a4d; border-color: #2f8a4d; opacity: 1; }

/* ---------- 인용(참고 상자) ---------- */
blockquote {
  margin: 1.3em 0;
  padding: 12px 18px;
  background: var(--note-bg);
  border-left: 4px solid var(--note-border);
  border-radius: 0 8px 8px 0;
  color: var(--fg);
}
blockquote p { margin: 0.4em 0; }
blockquote p:first-child { margin-top: 0; }
blockquote p:last-child { margin-bottom: 0; }

/* ---------- 모바일 ---------- */
#toc-toggle { display: none; }
@media (max-width: 980px) {
  .layout { display: block; }
  #sidebar {
    position: static;
    width: auto;
    height: auto;
    border-right: 0;
    border-bottom: 1px solid var(--border);
    padding: 14px 18px;
    max-height: 50vh;
  }
  #toc-toggle {
    display: block;
    width: 100%;
    text-align: left;
    background: none;
    border: 0;
    color: var(--fg);
    font: inherit;
    font-weight: 700;
    padding: 6px 0;
    cursor: pointer;
  }
  #sidebar .toc { display: none; }
  #sidebar.open .toc { display: block; }
  #sidebar .toc-title { display: none; }
  main { padding: 26px 18px 80px; }
  body { font-size: 16px; }
  h1 { font-size: 1.6rem; }
  h2 { font-size: 1.3rem; }
}

/* ---------- 인쇄 ---------- */
@media print {
  #sidebar, .copy-btn, .lang-switch, .doc-nav, .theme-switch { display: none !important; }
  body { font-size: 10.5pt; color: #000; background: #fff; }
  main { padding: 0; }
  .content { max-width: none; }
  h2 { page-break-after: avoid; }
  .codeblock pre, table, blockquote { page-break-inside: avoid; }
  a { color: #000; text-decoration: none; }
}
</style>
<script>
(function () {
  try {
    var saved = localStorage.getItem('guide-theme');
    if (saved) { document.documentElement.setAttribute('data-theme', saved); }
  } catch (e) {}
})();
</script>
</head>
<body>
<div class="layout">
  <nav id="sidebar">
    <button id="toc-toggle" type="button">__TOC_TOGGLE__</button>
__LANG_SWITCH__
    <div class="theme-switch">
      <div class="theme-switch-title">__THEME_TITLE__</div>
      <div class="theme-switch-row">
        <button type="button" data-theme-value="light">__THEME_LIGHT__</button>
        <button type="button" data-theme-value="dark">__THEME_DARK__</button>
        <button type="button" data-theme-value="sepia">__THEME_SEPIA__</button>
      </div>
    </div>
__DOC_NAV__
    <div class="toc-title">__TOC_TITLE__</div>
    __TOC__
  </nav>
  <main>
    <article class="content">
__BODY__
    </article>
  </main>
</div>

<script>
(function () {
  // 배경 테마 전환: 고른 값을 브라우저에 저장해 다음 방문에도 유지한다.
  var root = document.documentElement;
  var buttons = Array.prototype.slice.call(
    document.querySelectorAll('.theme-switch button[data-theme-value]'));
  if (!buttons.length) { return; }

  var read = function () {
    try { return localStorage.getItem('guide-theme'); } catch (e) { return null; }
  };
  var systemTheme = function () {
    return (window.matchMedia &&
      window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
  };
  var mark = function (value) {
    buttons.forEach(function (b) {
      b.setAttribute('aria-pressed',
        b.getAttribute('data-theme-value') === value ? 'true' : 'false');
    });
  };

  mark(read() || systemTheme());

  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      var value = b.getAttribute('data-theme-value');
      root.setAttribute('data-theme', value);
      try { localStorage.setItem('guide-theme', value); } catch (e) {}
      mark(value);
    });
  });
})();

(function () {
  // 표를 가로 스크롤 가능한 래퍼로 감싼다 (좁은 화면 대응)
  document.querySelectorAll('table').forEach(function (t) {
    if (t.parentElement.classList.contains('table-wrap')) return;
    var w = document.createElement('div');
    w.className = 'table-wrap';
    t.parentNode.insertBefore(w, t);
    w.appendChild(t);
  });

  // 코드 블록에 복사 버튼 달기
  document.querySelectorAll('pre').forEach(function (pre) {
    var box = document.createElement('div');
    box.className = 'codeblock';
    pre.parentNode.insertBefore(box, pre);
    box.appendChild(pre);

    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.type = 'button';
    btn.textContent = '__COPY__';
    btn.addEventListener('click', function () {
      var text = pre.innerText;
      var done = function () {
        btn.textContent = '__COPIED__';
        btn.classList.add('done');
        setTimeout(function () {
          btn.textContent = '__COPY__';
          btn.classList.remove('done');
        }, 1400);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done);
      } else {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
    });
    box.appendChild(btn);
  });

  // 모바일 목차 토글
  var sidebar = document.getElementById('sidebar');
  var toggle = document.getElementById('toc-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () { sidebar.classList.toggle('open'); });
    sidebar.querySelectorAll('.toc a').forEach(function (a) {
      a.addEventListener('click', function () { sidebar.classList.remove('open'); });
    });
  }

  // 스크롤 위치에 따라 현재 항목 강조
  var links = Array.prototype.slice.call(document.querySelectorAll('#sidebar .toc a'));
  var map = {};
  links.forEach(function (a) {
    var id = decodeURIComponent(a.getAttribute('href') || '').replace(/^#/, '');
    var el = id ? document.getElementById(id) : null;
    if (el) map[id] = a;
  });
  var targets = Object.keys(map).map(function (id) { return document.getElementById(id); });
  if ('IntersectionObserver' in window && targets.length) {
    var current = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var a = map[e.target.id];
        if (!a || a === current) return;
        if (current) current.classList.remove('active');
        a.classList.add('active');
        current = a;
      });
    }, { rootMargin: '0px 0px -75% 0px', threshold: 0 });
    targets.forEach(function (t) { io.observe(t); });
  }
})();
</script>
</body>
</html>
"""


def slugify(value, separator="-"):
    """한글을 그대로 보존하는 헤딩 ID 생성기."""
    value = re.sub(r"[^\w\s가-힣-]", "", value, flags=re.UNICODE).strip().lower()
    return re.sub(r"[\s]+", separator, value, flags=re.UNICODE)


NEWLINE = chr(10)


UI = {
    "ko": {
        "toc_toggle": "목차 열기/닫기 ▾",
        "toc_title": "목차",
        "copy": "복사",
        "copied": "복사됨",
        "docs": "문서",
        "theme": "배경",
        "light": "밝게",
        "dark": "어둡게",
        "sepia": "편하게",
        "self": "한국어",
        "other": "English",
    },
    "en": {
        "toc_toggle": "Show/hide contents ▾",
        "toc_title": "Contents",
        "copy": "Copy",
        "copied": "Copied",
        "docs": "Documents",
        "theme": "Background",
        "light": "Light",
        "dark": "Dark",
        "sepia": "Easy",
        "self": "English",
        "other": "한국어",
    },
}


def convert(src: Path, dst: Path, lang: str = "ko", alt: str = "",
            nav: str = "", nav_current: str = "") -> None:
    text = src.read_text(encoding="utf-8")

    md = markdown.Markdown(
        extensions=["extra", "toc", "sane_lists", "nl2br"],
        extension_configs={
            "toc": {"toc_depth": "1-3", "slugify": slugify},
        },
    )
    body = md.convert(text)
    toc = md.toc

    # 문서 제목: 첫 번째 H1 사용
    m = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    title = m.group(1).strip() if m else src.stem

    ui = UI.get(lang, UI["ko"])
    if alt:
        # 현재 언어는 눌린 상태(span), 다른 언어는 링크(a)로 둔다.
        other_code = "en" if lang == "ko" else "ko"
        switch = "\n".join([
            '    <div class=\"lang-switch\">',
            '      <span>%s</span>' % ui['self'],
            '      <a href=\"%s\" hreflang=\"%s\">%s</a>' % (alt, other_code, ui['other']),
            '    </div>',
        ])
    else:
        switch = ""

    # 문서 전환기: "라벨=파일명" 을 콤마로 구분. 현재 문서는 눌린 상태로 둔다.
    if nav:
        rows = []
        for entry in nav.split(","):
            entry = entry.strip()
            if not entry or "=" not in entry:
                continue
            label, href = entry.split("=", 1)
            label, href = label.strip(), href.strip()
            if label == nav_current:
                rows.append("      <span>%s</span>" % label)
            else:
                rows.append('      <a href="%s">%s</a>' % (href, label))
        doc_nav = NEWLINE.join(
            ['    <div class="doc-nav">',
             '      <div class="doc-nav-title">%s</div>' % ui["docs"]]
            + rows
            + ["    </div>"]
        )
    else:
        doc_nav = ""

    html = (
        TEMPLATE.replace("__TITLE__", title)
        .replace("__TOC__", toc)
        .replace("__BODY__", body)
        .replace("__LANG__", lang)
        .replace("__LANG_SWITCH__", switch)
        .replace("__DOC_NAV__", doc_nav)
        .replace("__THEME_TITLE__", ui["theme"])
        .replace("__THEME_LIGHT__", ui["light"])
        .replace("__THEME_DARK__", ui["dark"])
        .replace("__THEME_SEPIA__", ui["sepia"])
        .replace("__TOC_TOGGLE__", ui["toc_toggle"])
        .replace("__TOC_TITLE__", ui["toc_title"])
        .replace("__COPIED__", ui["copied"])
        .replace("__COPY__", ui["copy"])
    )
    dst.write_text(html, encoding="utf-8")
    print(f"생성 완료: {dst}  ({len(html):,} bytes)")


def main() -> int:
    args = sys.argv[1:]
    lang, alt, nav, nav_current = "ko", "", "", ""
    positional = []
    i = 0
    while i < len(args):
        if args[i] == "--lang" and i + 1 < len(args):
            lang = args[i + 1]
            i += 2
        elif args[i] == "--alt" and i + 1 < len(args):
            alt = args[i + 1]
            i += 2
        elif args[i] == "--nav" and i + 1 < len(args):
            nav = args[i + 1]
            i += 2
        elif args[i] == "--nav-current" and i + 1 < len(args):
            nav_current = args[i + 1]
            i += 2
        else:
            positional.append(args[i])
            i += 1

    if len(positional) != 2:
        print(__doc__)
        return 1
    src, dst = Path(positional[0]), Path(positional[1])
    if not src.exists():
        print(f"입력 파일을 찾을 수 없습니다: {src}")
        return 1
    convert(src, dst, lang=lang, alt=alt, nav=nav, nav_current=nav_current)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
