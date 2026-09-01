# 두 언어판 HTML을 한 번에 생성한다.
#   PS> .\build.ps1
py md_to_html.py "터미널_AI_에이전트_입문_가이드.md" "index.html" --lang ko --alt "en.html"
py md_to_html.py "terminal-ai-agent-guide.en.md"     "en.html"    --lang en --alt "index.html"
