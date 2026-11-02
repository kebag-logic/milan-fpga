"""Apply scripts/check_doc_style.py's analyze() to the prose blocks a change
adds or edits on each touched page. Usage:
    python3 -I style_touched.py <repo> <base> <page>...
Prints each finding in a block overlapping an added line; rc 1 on any."""
import re
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
base = sys.argv[2]
pages = sys.argv[3:]
sys.path.insert(0, str(repo / "scripts"))
import check_doc_style as cds  # noqa: E402


def added_lines(page):
    out = subprocess.run(["git", "-C", str(repo), "diff", "-U0", base, "--", page],
                         capture_output=True, text=True, check=True).stdout
    if not out.strip():
        # untracked or new page: every line counts
        text = (repo / page).read_text(encoding="utf-8")
        return set(range(1, len(text.splitlines()) + 1))
    lines = set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", out, re.M):
        start, count = int(m.group(1)), int(m.group(2) or 1)
        lines.update(range(start, start + count))
    return lines


total = 0
for page in pages:
    text = (repo / page).read_text(encoding="utf-8")
    added = added_lines(page)
    blocks = cds.prose_blocks(text)
    src = text.splitlines()
    spans = {}
    for b in blocks:
        end = b.line
        if b.paragraph:
            while end < len(src):
                nxt = src[end]          # line end+1 (1-based)
                s = nxt.strip()
                if (not s or s.startswith(("#", "|", ">", "```", "~~~", "<!--"))
                        or nxt.startswith("    ") or cds.LIST_ITEM.match(nxt)):
                    break
                end += 1
        spans.setdefault(b.line, (b.line, end))
    count = 0
    for f in cds.analyze(text):
        lo, hi = spans.get(f.line, (f.line, f.line))
        # a block ends at the line before the next block or flush; trim to its text
        if any(lo <= n <= hi for n in added):
            count += 1
            print(f"{page}:{f.line}: {f.reason}: {' '.join(f.text.split())[:160]}")
    print(f"{page}: {count} finding(s) in changed blocks")
    total += count
sys.exit(1 if total else 0)
