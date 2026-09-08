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
- 상단 진행 표시줄, 절 제목 고정 링크(#), 맨 위로 버튼을 자동으로 넣는다.
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
  --bg-sunk: #eef0f4;
  --bg-code: #f2f4f7;
  --fg: #1b1f24;
  --fg-soft: #59636e;
  --fg-faint: #8b959f;
  --border: #dde2e8;
  --border-soft: #e9edf1;
  --accent: #b5502a;
  --accent-strong: #96401f;
  --accent-soft: #fdf3ef;
  --note-bg: #f2f7fd;
  --note-border: #7ba7d7;
  --warn-bg: #fdf6ec;
  --warn-border: #d9a13b;
  --ok: #2f8a4d;
  --shadow-sm: 0 1px 2px rgba(16, 24, 40, 0.05);
  --shadow-md: 0 4px 14px rgba(16, 24, 40, 0.07);
  --radius: 10px;
  --sidebar-w: 306px;
  --maxw: 830px;
}
/* 시스템 설정을 따르되, 사용자가 직접 고른 값이 있으면 그쪽이 이긴다. */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) {
    --bg: #15171b;
    --bg-soft: #1c1f24;
    --bg-sunk: #23272e;
    --bg-code: #20242a;
    --fg: #e4e7eb;
    --fg-soft: #9aa3ad;
    --fg-faint: #737d87;
    --border: #333941;
    --border-soft: #282d34;
    --accent: #e59570;
    --accent-strong: #f0a884;
    --accent-soft: #2b211c;
    --note-bg: #1a2530;
    --note-border: #3f6a99;
    --warn-bg: #2b2418;
    --warn-border: #8a6a2b;
    --ok: #62b981;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.35);
  }
}
/* 어둡게 */
:root[data-theme="dark"] {
  --bg: #15171b;
  --bg-soft: #1c1f24;
  --bg-sunk: #23272e;
  --bg-code: #20242a;
  --fg: #e4e7eb;
  --fg-soft: #9aa3ad;
  --fg-faint: #737d87;
  --border: #333941;
  --border-soft: #282d34;
  --accent: #e59570;
  --accent-strong: #f0a884;
  --accent-soft: #2b211c;
  --note-bg: #1a2530;
  --note-border: #3f6a99;
  --warn-bg: #2b2418;
  --warn-border: #8a6a2b;
  --ok: #62b981;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.35);
}
/* 편하게 보기 — 눈부심을 줄인 따뜻한 배경 */
:root[data-theme="sepia"] {
  --bg: #f6eeda;
  --bg-soft: #efe5cf;
  --bg-sunk: #e7dbc0;
  --bg-code: #ece1c8;
  --fg: #38302a;
  --fg-soft: #6d6252;
  --fg-faint: #948872;
  --border: #ddd0b6;
  --border-soft: #e7dcc5;
  --accent: #a04a1f;
  --accent-strong: #883d17;
  --accent-soft: #f9ebda;
  --note-bg: #e6ebec;
  --note-border: #8aa2b5;
  --warn-bg: #f6e6c8;
  --warn-border: #c69a45;
  --ok: #2f7a48;
  --shadow-sm: 0 1px 2px rgba(80, 60, 30, 0.08);
  --shadow-md: 0 4px 14px rgba(80, 60, 30, 0.1);
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
  line-height: 1.78;
  letter-spacing: -0.003em;
  -webkit-text-size-adjust: 100%;
  -webkit-font-smoothing: antialiased;
  word-break: keep-all;
  overflow-wrap: break-word;
}

:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: 4px;
}

/* ---------- 읽은 분량 표시 ---------- */
#progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  width: 0;
  background: var(--accent);
  z-index: 60;
  transition: width .08s linear;
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
  scrollbar-width: thin;
  scrollbar-color: var(--border) transparent;
  border-right: 1px solid var(--border);
  background: var(--bg-soft);
  padding: 24px 16px 60px 22px;
}
#sidebar::-webkit-scrollbar { width: 8px; }
#sidebar::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 4px;
}
#sidebar .toc-title {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  color: var(--fg-faint);
  text-transform: uppercase;
  margin: 4px 0 10px 8px;
}
#sidebar ul { list-style: none; margin: 0; padding: 0; }
#sidebar ul ul {
  padding-left: 10px;
  margin-left: 6px;
  border-left: 1px solid var(--border-soft);
}
#sidebar li { margin: 1px 0; }
#sidebar a {
  display: block;
  padding: 4px 9px;
  border-radius: 7px;
  font-size: 0.85rem;
  line-height: 1.45;
  color: var(--fg-soft);
  text-decoration: none;
  transition: background .12s, color .12s;
}
#sidebar a:hover { background: var(--accent-soft); color: var(--accent-strong); }
#sidebar a.active {
  color: #fff;
  font-weight: 600;
  background: var(--accent);
}
/* 1단계 항목(부 제목)은 굵게 */
#sidebar > .toc > ul > li { margin-top: 9px; }
#sidebar > .toc > ul > li > a {
  font-weight: 700;
  color: var(--fg);
  font-size: 0.895rem;
}
#sidebar > .toc > ul > li > a.active { color: #fff; }

/* ---------- 사이드바 위쪽 전환기 ---------- */
.lang-switch {
  display: flex;
  gap: 4px;
  margin: 0 0 10px;
  padding: 3px;
  border: 1px solid var(--border);
  border-radius: 9px;
  background: var(--bg);
  box-shadow: var(--shadow-sm);
}
.lang-switch a, .lang-switch span {
  flex: 1 1 0;
  text-align: center;
  padding: 5px 0;
  font-size: 0.8rem;
  font-weight: 600;
  border-radius: 6px;
  text-decoration: none;
  line-height: 1.2;
}
.lang-switch span { background: var(--accent); color: #fff; }
.lang-switch a { color: var(--fg-soft); }
.lang-switch a:hover { background: var(--accent-soft); color: var(--accent-strong); }
.doc-nav, .theme-switch {
  margin: 0 0 10px;
  padding: 8px 9px 9px;
  border: 1px solid var(--border);
  border-radius: 9px;
  background: var(--bg);
  box-shadow: var(--shadow-sm);
}
.theme-switch { margin-bottom: 16px; }
.doc-nav .doc-nav-title, .theme-switch-title {
  font-size: 0.66rem;
  font-weight: 800;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--fg-faint);
  margin: 0 0 6px 3px;
}
.doc-nav a, .doc-nav span {
  display: block;
  padding: 4px 8px;
  font-size: 0.8rem;
  border-radius: 6px;
  text-decoration: none;
  line-height: 1.35;
}
.doc-nav span { background: var(--accent); color: #fff; font-weight: 600; }
.doc-nav a { color: var(--fg-soft); }
.doc-nav a:hover { background: var(--accent-soft); color: var(--accent-strong); }
.theme-switch-row { display: flex; gap: 4px; }
.theme-switch button {
  flex: 1 1 0;
  padding: 5px 2px;
  font: inherit;
  font-size: 0.74rem;
  font-weight: 600;
  line-height: 1.2;
  color: var(--fg-soft);
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: 6px;
  cursor: pointer;
  transition: background .12s, color .12s, border-color .12s;
}
.theme-switch button:hover { color: var(--accent-strong); border-color: var(--accent); }
.theme-switch button[aria-pressed="true"] {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

main {
  flex: 1 1 auto;
  min-width: 0;
  padding: 52px 44px 140px;
  display: flex;
  justify-content: center;
}
.content { width: 100%; max-width: var(--maxw); }

/* ---------- 타이포그래피 ---------- */
h1, h2, h3, h4 {
  line-height: 1.38;
  font-weight: 700;
  scroll-margin-top: 24px;
  position: relative;
}

/* 부(部) 제목 — 큰 구획을 한눈에 갈라 준다. */
h1 {
  font-size: 1.86rem;
  letter-spacing: -0.02em;
  margin: 0 0 1.1em;
  padding: 15px 22px 16px;
  color: var(--accent-strong);
  background: var(--accent-soft);
  border-left: 6px solid var(--accent);
  border-radius: 4px 12px 12px 4px;
}
h1 + p, h1 + blockquote { margin-top: 0; }
/* 문서 안의 두 번째 이후 h1(=각 부)은 위쪽 여백을 크게 둔다. */
.content h1 ~ h1 { margin-top: 3.4em; }

/* 절 제목 */
h2 {
  font-size: 1.4rem;
  letter-spacing: -0.015em;
  margin: 3em 0 0.85em;
  padding-bottom: 0.34em;
  border-bottom: 1px solid var(--border);
}
h2::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -1px;
  width: 54px;
  height: 2px;
  background: var(--accent);
}

/* 소절 제목 */
h3 {
  font-size: 1.13rem;
  margin: 2.2em 0 0.55em;
  padding-left: 12px;
  color: var(--accent-strong);
  border-left: 3px solid var(--accent);
}

/* 항목 제목 — 목록·질문 묶음을 시각적으로 끊어 준다. */
h4 {
  font-size: 1rem;
  margin: 1.9em 0 0.6em;
  padding: 7px 14px;
  color: var(--fg);
  background: var(--bg-sunk);
  border-left: 3px solid var(--accent);
  border-radius: 3px 8px 8px 3px;
}
h4 + p, h4 + ul, h4 + ol, h4 + .table-wrap, h4 + .codeblock { margin-top: 0.5em; }

p { margin: 0.9em 0; }

/* 굵은 글씨만으로 된 줄은 작은 머리글처럼 보이게 한다. */
p.lead-label {
  margin: 1.7em 0 0.4em;
  color: var(--fg);
  font-weight: 700;
}
p.lead-label > strong { font-weight: 700; }
p.lead-label::before {
  content: "";
  display: inline-block;
  width: 5px;
  height: 5px;
  margin: 0 8px 3px 0;
  border-radius: 50%;
  background: var(--accent);
  vertical-align: middle;
}
p.lead-label + ul, p.lead-label + ol { margin-top: 0.2em; }

a { color: var(--accent-strong); text-underline-offset: 2px; }
a:hover { color: var(--accent); }

/* 제목 옆 고정 링크 */
.anchor {
  position: absolute;
  right: 100%;
  margin-right: 8px;
  padding: 0 4px;
  color: var(--fg-faint);
  font-weight: 400;
  text-decoration: none;
  opacity: 0;
  transition: opacity .12s;
}
h2:hover .anchor, h3:hover .anchor, .anchor:focus { opacity: 1; }
h4 .anchor { display: none; }

hr {
  border: 0;
  border-top: 1px solid var(--border);
  margin: 3.2em 0;
}

ul, ol { padding-left: 1.35em; margin: 0.85em 0; }
li { margin: 0.34em 0; }
li::marker { color: var(--accent); }
ol li::marker { font-weight: 700; }
li > ul, li > ol { margin: 0.3em 0; }

strong { font-weight: 700; }

/* ---------- 표 ---------- */
.table-wrap {
  overflow-x: auto;
  margin: 1.5em 0;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  background: var(--bg);
}
table {
  border-collapse: collapse;
  width: 100%;
  font-size: 0.925rem;
}
th, td {
  border-bottom: 1px solid var(--border-soft);
  padding: 10px 14px;
  text-align: left;
  vertical-align: top;
}
th + th, td + td { border-left: 1px solid var(--border-soft); }
th {
  background: var(--bg-sunk);
  font-weight: 700;
  white-space: nowrap;
  border-bottom: 1px solid var(--border);
  color: var(--fg);
}
tbody tr:last-child td { border-bottom: 0; }
tbody tr:nth-child(even) td { background: var(--bg-soft); }

/* ---------- 코드 ---------- */
code {
  font-family: "Cascadia Mono", "Consolas", "D2Coding", "Menlo", monospace;
  font-size: 0.875em;
}
p code, li code, td code, th code, h4 code {
  background: var(--bg-code);
  border: 1px solid var(--border);
  border-radius: 5px;
  padding: 1px 5px;
  color: var(--accent-strong);
  white-space: nowrap;
}
.codeblock { position: relative; margin: 1.2em 0; }
.codeblock pre {
  margin: 0;
  background: var(--bg-code);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 62px 14px 16px;
  overflow-x: auto;
  line-height: 1.62;
  box-shadow: var(--shadow-sm);
}
.codeblock pre code {
  background: none;
  border: 0;
  padding: 0;
  color: inherit;
  font-size: 0.895rem;
  white-space: pre;
}
.copy-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--fg-soft);
  border-radius: 7px;
  padding: 3px 10px;
  font-size: 0.73rem;
  font-weight: 600;
  cursor: pointer;
  opacity: 0.45;
  transition: opacity .15s, color .15s, border-color .15s;
  font-family: inherit;
}
.codeblock:hover .copy-btn, .copy-btn:focus { opacity: 1; }
.copy-btn:hover { color: var(--accent-strong); border-color: var(--accent); }
.copy-btn.done { color: var(--ok); border-color: var(--ok); opacity: 1; }

/* ---------- 인용(참고 상자) ---------- */
blockquote {
  margin: 1.4em 0;
  padding: 13px 18px;
  background: var(--note-bg);
  border: 1px solid var(--border-soft);
  border-left: 4px solid var(--note-border);
  border-radius: 3px 10px 10px 3px;
  color: var(--fg);
  font-size: 0.965rem;
}
blockquote p { margin: 0.45em 0; }
blockquote p:first-child { margin-top: 0; }
blockquote p:last-child { margin-bottom: 0; }
/* 상자 첫 줄이 굵은 글씨면 제목처럼 떼어 놓는다. */
blockquote > p:first-child > strong:first-child {
  display: block;
  margin-bottom: 2px;
}
blockquote .codeblock { margin: 0.7em 0; }
blockquote .codeblock pre { background: var(--bg); }

/* ---------- 위로 가기 ---------- */
#to-top {
  position: fixed;
  right: 22px;
  bottom: 22px;
  z-index: 50;
  width: 42px;
  height: 42px;
  border: 1px solid var(--border);
  border-radius: 50%;
  background: var(--bg);
  color: var(--fg-soft);
  font: inherit;
  font-size: 1rem;
  line-height: 1;
  cursor: pointer;
  box-shadow: var(--shadow-md);
  opacity: 0;
  pointer-events: none;
  transition: opacity .18s, color .15s, border-color .15s;
}
#to-top.show { opacity: 1; pointer-events: auto; }
#to-top:hover { color: var(--accent-strong); border-color: var(--accent); }

/* ---------- 모바일 ---------- */
#toc-toggle { display: none; }
@media (max-width: 980px) {
  .layout { display: block; }
  #sidebar {
    position: sticky;
    top: 0;
    z-index: 40;
    width: auto;
    height: auto;
    border-right: 0;
    border-bottom: 1px solid var(--border);
    padding: 10px 16px;
    max-height: 78vh;
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
    padding: 6px 2px;
    cursor: pointer;
  }
  #sidebar .toc, #sidebar .lang-switch,
  #sidebar .doc-nav, #sidebar .theme-switch { display: none; }
  #sidebar.open .toc, #sidebar.open .doc-nav,
  #sidebar.open .theme-switch { display: block; }
  #sidebar.open .lang-switch { display: flex; }
  #sidebar .toc-title { display: none; }
  main { padding: 26px 17px 90px; }
  body { font-size: 16px; }
  h1 { font-size: 1.5rem; padding: 12px 16px 13px; }
  h2 { font-size: 1.24rem; margin-top: 2.4em; }
  h3 { font-size: 1.08rem; }
  .anchor { display: none; }
  #to-top { right: 14px; bottom: 14px; }
}

/* ---------- 움직임을 줄이는 설정 ---------- */
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { transition: none !important; }
}

/* ---------- 인쇄 ---------- */
@media print {
  #sidebar, .copy-btn, .lang-switch, .doc-nav, .theme-switch,
  #to-top, #progress, .anchor { display: none !important; }
  body { font-size: 10.5pt; color: #000; background: #fff; }
  main { padding: 0; }
  .content { max-width: none; }
  h1 { color: #000; background: none; border-left: 4px solid #000; }
  h2, h3, h4 { page-break-after: avoid; color: #000; background: none; }
  .codeblock pre, table, blockquote { page-break-inside: avoid; box-shadow: none; }
  .table-wrap { box-shadow: none; }
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
<div id="progress"></div>
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
<button id="to-top" type="button" title="__TOP__" aria-label="__TOP__">&#8593;</button>

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

  // 굵은 글씨 한 줄로만 된 문단은 작은 머리글처럼 표시한다.
  document.querySelectorAll('.content > p').forEach(function (p) {
    var kids = Array.prototype.filter.call(p.childNodes, function (n) {
      return !(n.nodeType === 3 && !n.nodeValue.trim());
    });
    // 문장이 아니라 '묶음 이름'일 때만 머리글 취급한다.
    // (짧고, 마침표로 끝나지 않는 줄)
    var label = p.textContent.trim();
    if (kids.length === 1 && kids[0].nodeName === 'STRONG' &&
        label.length <= 40 && !/[.!?]$/.test(label)) {
      p.classList.add('lead-label');
    }
  });

  // 절 제목에 고정 링크(#) 달기
  document.querySelectorAll('.content h2[id], .content h3[id]').forEach(function (h) {
    var a = document.createElement('a');
    a.className = 'anchor';
    a.href = '#' + h.id;
    a.textContent = '#';
    a.setAttribute('aria-label', '__ANCHOR__');
    h.insertBefore(a, h.firstChild);
  });

  // 읽은 분량 표시줄 + 위로가기 버튼
  var bar = document.getElementById('progress');
  var top = document.getElementById('to-top');
  var onScroll = function () {
    var doc = document.documentElement;
    var max = (doc.scrollHeight - doc.clientHeight) || 1;
    var ratio = Math.min(1, Math.max(0, doc.scrollTop / max));
    if (bar) { bar.style.width = (ratio * 100).toFixed(2) + '%'; }
    if (top) { top.classList.toggle('show', doc.scrollTop > 600); }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
  if (top) {
    top.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
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
        "top": "맨 위로",
        "anchor": "이 절의 주소",
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
        "top": "Back to top",
        "anchor": "Link to this section",
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
        .replace("__TOP__", ui["top"])
        .replace("__ANCHOR__", ui["anchor"])
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
