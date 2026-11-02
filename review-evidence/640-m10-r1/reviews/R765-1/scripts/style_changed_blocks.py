"""Apply scripts/check_doc_style.py's analyze() to every block of the given pages that the diff touches.

Usage (from the clone's root): python3 style_changed_blocks.py <base> <page> [<page> ...]
Prints one line per finding inside a changed block and a per-page count; exits 1 on any finding.
"""
import re
import subprocess
import sys
from pathlib import Path

root = Path.cwd()
sys.path.insert(0, str(root / "scripts"))
import check_doc_style as c  # noqa: E402

base, pages = sys.argv[1], sys.argv[2:]
total = 0
for page in pages:
    diff = subprocess.run(["git", "diff", "-U0", base, "HEAD", "--", page],
                          capture_output=True, text=True, check=True).stdout
    added = set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", diff, re.M):
        start, count = int(m.group(1)), int(m.group(2) or 1)
        added.update(range(start, start + count))
    text = (root / page).read_text(encoding="utf-8")
    lines = text.splitlines()
    n = 0
    for f in c.analyze(text):
        end = f.line
        while end < len(lines) and lines[end].strip() and not lines[end].lstrip().startswith(("#", "|", "-", "```")):
            end += 1
        if any(f.line <= k <= end for k in added):
            print(f"{page}:{f.line}: {f.reason}")
            n += 1
    print(f"{page}: {len(added)} changed line(s), {n} finding(s) in changed blocks")
    total += n
sys.exit(1 if total else 0)
