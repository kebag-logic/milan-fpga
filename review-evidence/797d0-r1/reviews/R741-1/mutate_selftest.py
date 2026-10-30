#!/usr/bin/env python3
"""Apply single source mutants to a copy of scripts/docs_inventory.py and run --selftest and --check.

Usage: python3 -I mutate_selftest.py SOURCE_CLONE WORKDIR
For each mutant: copy the clone's tracked tree (git archive HEAD, plus a .git
from a no-local clone so the git listing path runs), rewrite one line of the
generator, then record whether --selftest (rc != 0 = KILLED) and --check on the
real tree (rc != 0 = CAUGHT) notice it.
"""
import shutil
import subprocess
import sys
from pathlib import Path

src, work = Path(sys.argv[1]), Path(sys.argv[2])
GEN = "scripts/docs_inventory.py"
MUTANTS = [
    ("check-always-fresh", "    if actual == expected:\n        print(f\"documentation inventory: OK",
     "    if True:\n        print(f\"documentation inventory: OK"),
    ("check-returns-0-when-stale", "    print(\"regenerate with: python3 scripts/docs_inventory.py --write\")\n    return 1",
     "    print(\"regenerate with: python3 scripts/docs_inventory.py --write\")\n    return 0"),
    ("git-listing-includes-untracked", "[\"git\", \"-C\", str(root), \"ls-files\", \"-z\"]",
     "[\"git\", \"-C\", str(root), \"ls-files\", \"-z\", \"--cached\", \"--others\"]"),
    ("git-listing-keeps-gitlinks", "if p and p not in modules]", "if p]"),
    ("locate-never-finds", "        if quote in line:\n            return number", "        if False:\n            return number"),
    ("stale-rule-removed", "    if page_findings:\n        return \"stale\"", "    if False:\n        return \"stale\""),
    ("release-facing-empty", "RELEASE_FACING = re.compile(r\"README", "RELEASE_FACING = re.compile(r\"NEVER|README"),
    ("lines-off-by-one", "    return text.count(\"\\n\") + (1 if text and not text.endswith(\"\\n\") else 0)",
     "    return text.count(\"\\n\") + 1"),
    ("readme-only-not-a-document", "    return path.endswith(\".md\") or name.upper().startswith(\"README\")",
     "    return path.endswith(\".md\")"),
    ("banner-scan-1-line", "BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 1"),
]


def run(cwd: Path, *args: str) -> int:
    return subprocess.run(["python3", "-I", GEN, *args], cwd=cwd, capture_output=True, text=True).returncode


work.mkdir(parents=True, exist_ok=True)
base = work / "base"
if base.exists():
    shutil.rmtree(base)
subprocess.run(["git", "clone", "-q", "--no-local", str(src), str(base)], check=True)
head = subprocess.run(["git", "-C", str(src), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
subprocess.run(["git", "-C", str(base), "checkout", "-q", "--detach", head], check=True)
original = (base / GEN).read_text(encoding="utf-8")
print(f"baseline selftest rc={run(base, '--selftest')} check rc={run(base, '--check')}")
for name, old, new in MUTANTS:
    if original.count(old) != 1:
        print(f"{name}: PATTERN-NOT-UNIQUE ({original.count(old)})")
        continue
    (base / GEN).write_text(original.replace(old, new), encoding="utf-8")
    st, ck = run(base, "--selftest"), run(base, "--check")
    print(f"{name}: selftest {'KILLED' if st else 'SURVIVED'} (rc={st}); "
          f"check on real tree {'CAUGHT' if ck else 'PASSED'} (rc={ck})")
(base / GEN).write_text(original, encoding="utf-8")
print(f"restored selftest rc={run(base, '--selftest')} check rc={run(base, '--check')}")
