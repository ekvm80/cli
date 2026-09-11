# 터미널 AI 에이전트 가이드 / Terminal AI Agent Guides

컴퓨터를 잘 몰라도 따라 할 수 있게 만든 CLI AI 에이전트 입문 안내서 두 편입니다. Windows 11 기준입니다.

Two beginner's guides to CLI AI agents, written for people who are not comfortable with computers. Based on Windows 11.

## 읽기 / Read

| 문서 | 한국어 | English |
|---|---|---|
| **터미널 AI 에이전트 입문** — Claude Code · Codex CLI · Antigravity CLI | **[열기](https://ekvm80.github.io/cli/)** | **[Open](https://ekvm80.github.io/cli/en.html)** |
| **Orca 병렬 에이전트 입문** — 여러 에이전트를 동시에 | **[열기](https://ekvm80.github.io/cli/orca.html)** | **[Open](https://ekvm80.github.io/cli/orca.en.html)** |

각 페이지 좌측 상단에 전환기가 셋 있습니다.
Each page has three switchers at the top left.

- **`한국어 / English`** — 같은 문서의 반대 언어 / the same document in the other language
- **`배경: 밝게 / 어둡게 / 편하게`** — 배경 테마. 고른 값은 브라우저에 저장됩니다 / background theme, remembered in your browser
- **`문서`** — 두 문서 사이 이동 / move between the two documents

## 어느 것부터 볼까 / Where to start

터미널을 처음 쓴다면 **터미널 AI 에이전트 입문**부터 보세요. 4부까지 마치면 5부에서 갈림길이 나옵니다 — 터미널에서 계속 연습하거나, Orca로 바로 넘어가거나. **어느 쪽을 먼저 해도 됩니다.**

If terminals are new to you, start with **Terminal AI Agents**. After Part 4 you reach a fork in Part 5 — keep practising in the terminal, or move straight to Orca. **Either order works.**

## 다루는 내용 / Contents

**터미널 AI 에이전트 입문 / Terminal AI Agents**

0. 가장 간단 — 최단 경로 요약 — The short version: the fastest path through
1. 왜 터미널에서 AI를 쓰는가 — Why run AI in a terminal
2. 터미널 기초 (30분) — Terminal basics
3. 설치 준비 (Node.js, Git) — Preparation
4. AI 에이전트 설치 — Installing an agent
5. 첫 사용 (필수 명령어 5개 · 사용량 한도) — Your first session (five essential commands, usage limits)
6. 실제로 시켜볼 만한 일들 — Things worth trying
7. 기능 늘리기 (MCP·플러그인) — Extending it with MCP servers and plugins
8. 안전하게 쓰기 — Using it safely
9. 문제 해결 — Troubleshooting
10. 부록 A~E (용어, 명령어 요약, Mac, WSL, 선택 설정) — Appendices A–E

**Orca 병렬 에이전트 입문 / Orca Parallel Agents**

1. Orca란 무엇인가 — What Orca is
2. 설치 (Windows) — Installing on Windows
3. AI CLI 연결 — Connecting your AI CLIs
4. 프로젝트 만들고 병렬로 쓰기 — Creating a project and working in parallel
5. 실행 위치 (로컬) — Where it runs
6. 주의사항 — Things to be careful about
7. 부록 A~E (Mac·Linux, worktree, CLI 자동화, 원격 실행, 출처) — Appendices A–E

## 이 저장소의 구조 / Repository layout

```
터미널_AI_에이전트_입문_가이드.md     한국어 원본 (source of truth)
terminal-ai-agent-guide.en.md         영어 원본
Orca_병렬_AI에이전트_입문_가이드.md   한국어 원본
orca-parallel-agents-guide.en.md      영어 원본

index.html      한국어 · 터미널 입문 (생성물)
터미널_AI_에이전트_입문_가이드.html   index.html 과 같은 내용 (로컬 배포용 복사본)
en.html         영어  · 터미널 입문
orca.html       한국어 · Orca
orca.en.html    영어  · Orca

md_to_html.py   Markdown -> 단일 HTML 변환기
build.ps1       네 개를 한 번에 생성
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
py md_to_html.py 입력.md 출력.html --lang ko|en --alt 반대언어.html `
                 --nav "라벨=파일.html,라벨=파일.html" --nav-current 라벨
```

> `build.ps1` 은 **UTF-8 BOM** 으로 저장되어야 합니다. BOM이 없으면 Windows PowerShell 5.1 이 한글 파일명을 깨뜨려 빌드가 실패합니다.
> `build.ps1` must be saved as **UTF-8 with BOM**, or Windows PowerShell 5.1 mangles the Korean filenames and the build fails.

## 갱신 기준 / Currency

2026년 9월 기준으로 사실관계를 확인했습니다. 주요 확인 사항:

Facts verified as of September 2026. Key points:

- **Gemini CLI는 2026년 6월 18일 개인 사용자 지원이 종료되었습니다.** 후속 도구는 Antigravity CLI (`agy`) 입니다.
  Gemini CLI stopped serving individual users on 18 June 2026; its successor is Antigravity CLI (`agy`).
- 세 도구 모두 Node.js 없이 설치되는 전용 설치본을 제공합니다. WSL은 필요하지 않습니다.
  All three tools ship dedicated installers that need no Node.js. WSL is not required.
- `npm update -g` 는 최신 버전으로 올라가지 않습니다. `npm install -g <패키지>@latest` 를 쓰세요.
  `npm update -g` does not reach the latest release; use `npm install -g <package>@latest`.
- **Orca는 권한 확인을 건너뛰는 옵션이 기본으로 켜져 있습니다.** 처음에는 `Manual` 로 바꾸세요.
  **Orca ships with permission bypass on by default.** Switch it to `Manual` at first.
- 2.4절의 터미널 명령(`ls`, `pwd`)은 **PowerShell 기준**입니다. 옛 `명령 프롬프트(cmd)`에서는 동작하지 않습니다.
  The terminal commands in section 2.4 (`ls`, `pwd`) assume **PowerShell**; they do not work in the old `Command Prompt (cmd)`.
- 실행 정책·한글 깨짐 설정은 **선택 사항**이므로 부록 E로 옮겼습니다. 문제가 생겼을 때만 하면 됩니다.
  The execution-policy and encoding settings are **optional** and now live in Appendix E — do them only if something breaks.
- 사용량은 회사별로 **5시간·주(7일) 단위 한도**로 관리됩니다. 정확한 수치는 요금제마다 다르므로 `/usage` 로 확인하세요.
  Usage is metered per **5-hour and weekly (7-day) windows**; exact allocations vary by plan, so check with `/usage`.
- 7부에 소개한 확장(kordoc, korean-law-mcp, korean-stats-mcp, gptaku_plugins)은 **제3자 공개 도구**입니다. 저장소와 설치 명령은 2026년 9월 기준으로 확인했습니다.
  The extensions in Part 7 are **third-party open-source tools**; repositories and install commands were checked in September 2026.

도구 쪽 사정이 자주 바뀝니다. 어긋나는 부분을 발견하면 이슈로 알려주세요.
These tools change often. Please open an issue if something no longer matches.

## 라이선스 / License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — 출처를 밝히면 자유롭게 쓰고 고칠 수 있습니다.
Free to use and adapt with attribution.
