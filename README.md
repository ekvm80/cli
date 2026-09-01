# 터미널 AI 에이전트 입문 가이드 / Terminal AI Agents — Beginner's Guide

컴퓨터를 잘 몰라도 따라 할 수 있게 만든 CLI AI 에이전트(Claude Code · Codex CLI · Antigravity CLI) 입문 안내서입니다. Windows 11 기준입니다.

A beginner's guide to terminal AI agents (Claude Code, Codex CLI, Antigravity CLI), written for people who are not comfortable with computers. Based on Windows 11.

## 읽기 / Read

| | |
|---|---|
| 한국어 | **[가이드 열기](https://ekvm80.github.io/cli/)** |
| English | **[Open the guide](https://ekvm80.github.io/cli/en.html)** |

두 판은 페이지 좌측 상단의 `한국어 / English` 버튼으로 서로 전환됩니다.
The two versions switch via the `한국어 / English` button at the top left of each page.

## 다루는 내용 / Contents

1. 왜 터미널에서 AI를 쓰는가 — Why run AI in a terminal
2. 터미널 기초 (30분) — Terminal basics
3. 설치 준비 (Node.js, Git, 실행 정책) — Preparation
4. AI 에이전트 설치 — Installing an agent
5. 첫 사용 — Your first session
6. 실제로 시켜볼 만한 일들 — Things worth trying
7. 안전하게 쓰기 — Using it safely
8. 문제 해결 — Troubleshooting
9. 부록 A~D (용어, 명령어 요약, Mac, WSL) — Appendices A–D

## 이 저장소의 구조 / Repository layout

```
터미널_AI_에이전트_입문_가이드.md   한국어 원본 (source of truth)
terminal-ai-agent-guide.en.md       영어 원본
index.html                          한국어 웹페이지 (생성물)
en.html                             영어 웹페이지 (생성물)
md_to_html.py                       Markdown -> 단일 HTML 변환기
build.ps1                           두 언어판을 한 번에 생성
```

`.html` 파일은 **생성물입니다.** 내용을 고칠 때는 `.md` 를 고치고 다시 빌드하세요.
The `.html` files are **build artifacts.** Edit the `.md` sources and rebuild.

## 빌드 / Build

`markdown` 패키지만 있으면 됩니다. 외부 CSS·JS·폰트를 전혀 불러오지 않는 단일 HTML 파일이 나오므로, 인터넷 없이도 열립니다.

Only the `markdown` package is required. The output is a single self-contained HTML file with no external CSS, JS or fonts, so it opens offline.

```powershell
pip install markdown
.\build.ps1
```

개별 실행 / Individual runs:

```powershell
py md_to_html.py 입력.md 출력.html --lang ko|en --alt 반대언어파일.html
```

## 갱신 기준 / Currency

2026년 9월 기준으로 사실관계를 확인했습니다. 주요 확인 사항:

Facts verified as of September 2026. Key points:

- **Gemini CLI는 2026년 6월 18일 개인 사용자 지원이 종료되었습니다.** 후속 도구는 Antigravity CLI (`agy`) 입니다.
  Gemini CLI stopped serving individual users on 18 June 2026; its successor is Antigravity CLI (`agy`).
- 세 도구 모두 Node.js 없이 설치되는 전용 설치본을 제공합니다. WSL은 필요하지 않습니다.
  All three tools ship dedicated installers that need no Node.js. WSL is not required.
- `npm update -g` 는 최신 버전으로 올라가지 않습니다. `npm install -g <패키지>@latest` 를 쓰세요.
  `npm update -g` does not reach the latest release; use `npm install -g <package>@latest`.

도구 쪽 사정이 자주 바뀝니다. 어긋나는 부분을 발견하면 이슈로 알려주세요.
These tools change often. Please open an issue if something no longer matches.

## 라이선스 / License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — 출처를 밝히면 자유롭게 쓰고 고칠 수 있습니다.
Free to use and adapt with attribution.
