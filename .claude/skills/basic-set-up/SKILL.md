---
name: basic-set-up
description: >
  Windows PowerShell 환경에서 워크샵에 필요한 모든 개발 도구를 자동으로 설치한다.
  VS Code, Claude Code 익스텐션, uv, Python, 프로젝트 의존성을 순서대로 설치하고
  각 단계를 스스로 검증하며 오류 발생 시 자동으로 디버깅한다.
  "basic-set-up", "환경 설치", "설치 시작", "셋업" 등을 언급하거나
  워크샵 참가자가 개발 환경을 처음 구성할 때 반드시 이 스킬을 사용한다.
allowed-tools:
  - Bash
  - PowerShell
---

# basic-set-up — 워크샵 환경 자동 설치

Windows PowerShell 환경에서 워크샵에 필요한 모든 도구를 자동으로 설치한다.
참가자는 오류를 해석하거나 직접 해결할 필요 없다. 스킬이 끝까지 책임진다.

---

## 전제 조건 (이 스킬 실행 전 이미 완료된 것)

- Git 설치 완료 (`git --version` 정상 출력)
- 프로젝트 폴더 안에서 실행 중 (`agent-seminar-poc` 디렉토리)

---

## 설치 순서

아래 순서대로 진행한다. 각 단계는 반드시 검증 후 다음으로 넘어간다.

### Step 0 — Claude Code CLI 설치 확인 및 설치

**확인:**
```powershell
claude --version
```

이미 설치되어 있으면 Step 1로 넘어간다.

**없으면 Node.js 확인:**
```powershell
node --version
```

Node.js 18 이상이 있으면 바로 Claude Code CLI 설치로 넘어간다.

**Node.js가 없으면 winget으로 설치:**
```powershell
winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
```

설치 후 새 PowerShell 세션에서 재확인:
```powershell
node --version
```

**Node.js 확인 후 Claude Code CLI 설치:**
```powershell
npm install -g @anthropic-ai/claude-code
```

설치 후 재확인:
```powershell
claude --version
```

**실패 시 대응:**
- `npm` 명령이 없으면 Node.js 설치 후 새 PowerShell 세션에서 재시도
- 권한 오류 → PowerShell을 관리자 권한으로 열고 재시도
- 네트워크 오류 → 인터넷 연결 확인 후 재시도
- winget이 없으면 Node.js 공식 사이트 안내: `https://nodejs.org` → LTS 버전 다운로드 후 설치

---

### Step 1 — uv 설치 확인 및 설치

**확인:**
```powershell
uv --version
```

이미 설치되어 있으면 Step 2로 넘어간다.

**없으면 설치:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

설치 후 PowerShell을 새로 시작해야 PATH가 적용된다.
새 PowerShell 세션에서 `uv --version`으로 재확인한다.

**실패 시 대응:**
- `ExecutionPolicy` 오류 → `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` 실행 후 재시도
- 네트워크 오류 → 인터넷 연결 확인 후 재시도
- 그 외 오류 → 오류 메시지를 읽고 원인을 파악한 뒤 적절한 방법으로 재시도

---

### Step 2 — Python 설치 확인 및 설치

**확인:**
```powershell
python --version
```

Python 3.8 이상이 있으면 Step 3으로 넘어간다.

**없으면 uv로 설치:**
```powershell
uv python install
```

설치 후 재확인:
```powershell
python --version
```

**실패 시 대응:**
- uv가 없으면 Step 1부터 다시 진행
- `python` 명령이 인식되지 않으면 `uv run python --version`으로 확인
- 여전히 실패하면 `uv python list`로 설치된 Python 목록 확인 후 경로 문제 해결

---

### Step 3 — VS Code 설치 확인 및 설치

**확인:**
```powershell
code --version
```

이미 설치되어 있으면 Step 4로 넘어간다.

**없으면 winget으로 설치:**
```powershell
winget install Microsoft.VisualStudioCode --accept-package-agreements --accept-source-agreements
```

설치 후 새 PowerShell 세션에서 `code --version`으로 재확인한다.

**winget이 없는 경우:**
참가자에게 아래 안내를 전달한다:
```
VS Code를 직접 설치해야 합니다.
1. Chrome에서 https://code.visualstudio.com/download 를 열어주세요
2. Windows x64 User Installer를 다운로드하고 실행해주세요
3. 설치가 끝나면 강사에게 알려주세요
```
참가자가 설치를 완료하면 `code --version`으로 다시 확인하고 계속 진행한다.

---

### Step 4 — Claude Code VS Code 익스텐션 설치 확인 및 설치

**확인:**
```powershell
code --list-extensions | findstr -i claude
```

`anthropic.claude-code`가 출력되면 Step 5로 넘어간다.

**없으면 설치:**
```powershell
code --install-extension anthropic.claude-code
```

설치 후 재확인:
```powershell
code --list-extensions | findstr -i claude
```

**실패 시 대응:**
- `code` 명령이 없으면 Step 3으로 돌아가 VS Code 먼저 설치
- 익스텐션 ID 오류가 나면 `anthropic.claude-code`가 정확한지 확인
- 네트워크 오류면 재시도

---

### Step 5 — 프로젝트 의존성 설치

**확인:**
```powershell
python -X utf8 .claude/skills/naver-ad-rank/fetch_powerlink.py "테스트"
```

JSON이 정상 출력되면 이미 완료 상태. Step 6(최종 검증)으로 바로 이동.

**없으면 설치:**
```powershell
uv pip install -r requirements.txt
```

`requirements.txt`가 없으면:
```powershell
uv pip install requests beautifulsoup4
```

설치 후 재확인:
```powershell
python -X utf8 .claude/skills/naver-ad-rank/fetch_powerlink.py "테스트"
```

**실패 시 대응:**
- `ModuleNotFoundError` → 해당 모듈만 별도 설치: `uv pip install [모듈명]`
- `python` 명령 없음 → Step 2로 돌아가 Python 먼저 설치
- 파일 경로 오류 → 현재 디렉토리가 `agent-seminar-poc`인지 확인: `pwd`

---

### Step 6 — 최종 검증

모든 설치가 끝나면 아래 명령어로 전체 동작을 검증한다:

```powershell
python -X utf8 .claude/skills/naver-ad-rank/fetch_powerlink.py "테스트"
```

**성공 기준:**
아래와 같이 JSON이 출력되면 완료.
```json
{
  "keyword": "테스트",
  "ads": [ ... ]
}
```

**성공 시 출력 메시지:**
```
✅ 설치 완료!

모든 준비가 끝났습니다.
이제 Notion의 다음 단계로 넘어가세요 → [따라 만들기]
```

---

## 강사 호출이 필요한 경우

스스로 해결할 수 없는 상황에서만 참가자에게 아래 메시지를 전달한다:

```
⚠️ 강사 호출이 필요합니다.

[문제 상황을 한 줄로 설명]

손을 들어주세요. 강사가 직접 확인하겠습니다.
```

강사 호출 판단 기준:
- 같은 오류가 3회 이상 반복되고 원인을 파악할 수 없을 때
- 시스템 권한 문제로 설치 자체가 불가능할 때
- 회사 보안 정책으로 특정 프로그램 설치가 차단된 것이 명확할 때

그 외의 오류는 스스로 원인을 파악하고 해결을 시도한다.
참가자에게 오류 메시지를 해석해달라거나 직접 해결하라고 요청하지 않는다.

---

## 진행 원칙

- 각 단계 시작 시 "Step N 진행 중..." 형태로 현재 상태를 참가자에게 알린다
- 이미 설치된 도구는 스킵하고 "이미 설치되어 있습니다 ✓" 로 표시한다
- 오류가 나도 참가자에게 당황하지 말라고 안내하고 스스로 해결한다
- 해결 과정을 짧게 설명해서 참가자가 무슨 일이 일어나는지 알 수 있게 한다
