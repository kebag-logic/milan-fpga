"""Repeat the five R366-2 committed-tree scans without a shell pipeline."""
from pathlib import Path
import subprocess

ROOT = Path('$LANES/602-phc-step-mr')
EXCLUDES = [':!docs/history', ':!protocol-processor', ':!gptp-processor', ':!third_party']
PATTERNS = [
    r"PHC step toggles|toggles `?mr`? once|counts that toggle in MEDIA_RESET",
    r"(phc|step|re-?base|settime|adjtime).{0,80}(\bmr\b|`mr`|media_reset|media reset)|(\bmr\b|`mr`|media_reset).{0,80}(phc step|a step|the step|re-?base|settime|adjtime)",
    r"(phc|gm|grandmaster)[ -]step.{0,100}(toggl|restart)|(toggl|restart).{0,100}(phc|gm|grandmaster)[ -]step|re-?base.{0,60}(toggles|restart request)",
]

def scan(args: list[str]) -> str:
    result = subprocess.run(['rtk', 'proxy', 'git', 'grep', *args], cwd=ROOT,
                            capture_output=True, text=True, check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr)
    return result.stdout

for i, pattern in enumerate(PATTERNS, 1):
    print(f'## scan {i}')
    extra = [':!*.svh'] if i == 2 else []
    print(scan(['-n', '-i', '-E', pattern, 'HEAD', '--', *EXCLUDES, *extra]), end='')
print('## scan 4')
context = scan(['-n', '-i', '-B1', '-A1', 'media_reset\\|media reset', 'HEAD', '--',
                '*.md', 'sw/*', 'scripts/*', 'avdecc/*', ':!docs/history'])
import re
for line in context.splitlines():
    if re.search(r'step|re-?base|phc|settime|adjtime', line, re.I):
        print(line)
print('## scan 5')
hits = scan(['-n', 'ORs both onto restart_p_i', 'HEAD'])
print(hits or 'No hits (git grep rc 1)', end='\n')
