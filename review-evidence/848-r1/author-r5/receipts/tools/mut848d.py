#!/usr/bin/env python3
"""Plant each mutant in a disposable clone of the head; run --selftest and --check; restore.

usage: mut848d.py <disposable clone>
A mutant is killed by the selftest when --selftest exits non-zero.
"""
import subprocess
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
target = clone / "scripts/docs_inventory.py"
pristine = target.read_text(encoding="utf-8")
ROW = '        verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "D0" if path in checked else "area lane"\n'
RULE = ('RELEASE_FACING = re.compile(r"README\\.md|REQUIREMENTS\\.md|docs/README\\.md|'
        'docs/(guides|integration|reference)/.*")\n')
GUARD = 'if not isinstance(checked, list) or not all(isinstance(page, str) and page in known for page in checked):'
MUTANTS = (
    ("F0 the fix removed: the old path rule decides D0 again",
     ((ROW, ROW.replace("path in checked", "RELEASE_FACING.fullmatch(path)")),
      ("#: The area lane that owns each page", RULE + "#: The area lane that owns each page"))),
    ("F1 every page outside the archive is D0", ((ROW, ROW.replace("path in checked", "True")),)),
    ("F2 no page is D0", ((ROW, ROW.replace("path in checked", "False")),)),
    ("F3 the list check dropped", ((GUARD, GUARD.replace("not isinstance(checked, list) or ", "")),)),
    ("F4 the string check dropped", ((GUARD, GUARD.replace("isinstance(page, str) and ", "")),)),
    ("F5 the tracked check dropped", ((GUARD, GUARD.replace(" and page in known", "")),)),
    ("F6 the population not returned", (('"--")), set(checked), judged', '"--")), set(), judged'),)),
    ("F7 the population not read", (('checked = data.get("verified_pages", [])', 'checked = []'),)),
    ("F8 the wrong key read", (('data.get("verified_pages", [])', 'data.get("verified", [])'),)),
    ("F9 the archive test dropped", ((ROW, ROW.replace('"archive" if path.startswith(ARCHIVE_PREFIX) else ', "")),)),
    ("F10 D0 tested before the archive",
     ((ROW, '        verified = "D0" if path in checked else "archive" if path.startswith(ARCHIVE_PREFIX) '
            'else "area lane"\n'),)),
)
env_run = dict(cwd=clone, capture_output=True, text=True, check=False)
for name, edits in (("IDENTITY no change", ()),) + MUTANTS:
    text = pristine
    for old, new in edits:
        if text.count(old) != 1:
            raise SystemExit(f"{name}: anchor found {text.count(old)} times: {old[:60]}")
        text = text.replace(old, new)
    target.write_text(text, encoding="utf-8")
    selftest = subprocess.run(["python3", "-B", "scripts/docs_inventory.py", "--selftest"], **env_run)
    check = subprocess.run(["python3", "-B", "scripts/docs_inventory.py", "--check"], **env_run)
    fails = [line for line in selftest.stdout.splitlines() if line.startswith("selftest: FAIL")]
    tail = (selftest.stderr.strip().splitlines() or [""])[-1][:120]
    print(f"{name}\n  --selftest rc={selftest.returncode}, {len(fails)} arm(s) failed; --check rc={check.returncode}")
    for line in fails[:6]:
        print("    " + line[:170])
    if tail:
        print("    traceback ends: " + tail)
target.write_text(pristine, encoding="utf-8")
print("restored:", subprocess.run(["git", "status", "--porcelain"], **env_run).stdout.strip() == "")
