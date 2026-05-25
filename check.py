import subprocess
import sys
import os

RESET  = "\033[0m"
GREEN  = "\033[92m"
RED    = "\033[91m"
BOLD   = "\033[1m"

def check(label, cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        ok = result.returncode == 0 and result.stdout.strip()
        version = result.stdout.strip().splitlines()[0] if ok else ""
        status = f"{GREEN}✅ OK{RESET}" if ok else f"{RED}❌ 없음{RESET}"
        detail = f"  ({version})" if version else ""
        print(f"  {status}  {label}{detail}")
        return ok
    except Exception:
        print(f"  {RED}❌ 오류{RESET}  {label}")
        return False

def check_extension():
    try:
        result = subprocess.run("code --list-extensions", capture_output=True, text=True, shell=True)
        ok = "anthropic.claude-code" in result.stdout.lower()
        status = f"{GREEN}✅ OK{RESET}" if ok else f"{RED}❌ 없음{RESET}"
        print(f"  {status}  Claude Code 익스텐션")
        return ok
    except Exception:
        print(f"  {RED}❌ 오류{RESET}  Claude Code 익스텐션")
        return False


print()
print(f"{BOLD}===================================={RESET}")
print(f"{BOLD}  워크샵 환경 확인{RESET}")
print(f"{BOLD}===================================={RESET}")
print()

results = []
results.append(check("Git",              "git --version"))
results.append(check("uv",               "uv --version"))
results.append(check("Python",           "python --version"))
results.append(check("VS Code",          "code --version"))
results.append(check_extension())

print()
print(f"{BOLD}------------------------------------{RESET}")

all_ok = all(results)
if all_ok:
    print(f"  {GREEN}{BOLD}🎉 모든 준비가 완료되었습니다!{RESET}")
    print(f"     Notion의 다음 단계로 넘어가세요 → 따라 만들기")
else:
    failed = sum(1 for r in results if not r)
    print(f"  {RED}{BOLD}⚠️  {failed}개 항목을 확인해주세요.{RESET}")
    print(f"     @한서현을 호출하거나 claude \"/basic-set-up\" 을 다시 실행하세요.")

print(f"{BOLD}===================================={RESET}")
print()
