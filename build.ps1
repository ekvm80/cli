# 네 개 문서(한국어/영어 x 2종)를 한 번에 생성한다.
#   PS> .uild.ps1
# 이 파일은 UTF-8 BOM 으로 저장해야 한다. 아니면 Windows PowerShell 5.1 이
# 한글 파일명을 깨뜨려 '입력 파일을 찾을 수 없습니다' 로 실패한다.

$navKo = "터미널 AI 에이전트 입문=index.html,Orca 병렬 에이전트=orca.html"
$navEn = "Terminal AI Agents=en.html,Orca Parallel Agents=orca.en.html"

py md_to_html.py "터미널_AI_에이전트_입문_가이드.md"  "index.html"   --lang ko --alt "en.html"      --nav $navKo --nav-current "터미널 AI 에이전트 입문"
py md_to_html.py "terminal-ai-agent-guide.en.md"      "en.html"      --lang en --alt "index.html"   --nav $navEn --nav-current "Terminal AI Agents"
py md_to_html.py "Orca_병렬_AI에이전트_입문_가이드.md" "orca.html"    --lang ko --alt "orca.en.html" --nav $navKo --nav-current "Orca 병렬 에이전트"
py md_to_html.py "orca-parallel-agents-guide.en.md"   "orca.en.html" --lang en --alt "orca.html"    --nav $navEn --nav-current "Orca Parallel Agents"

# index.html 을 한글 파일명으로도 복사해 둔다 (로컬에서 직접 열어 보는 용도).
Copy-Item "index.html" "터미널_AI_에이전트_입문_가이드.html" -Force
