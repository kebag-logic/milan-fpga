#!/usr/bin/env python3
"""check_doc_style.py's rules over the lines this round added to each touched Markdown page.

usage (from a clone): doc_style_added.py <from-commit>
check_doc_style.py judges only its audience pages and takes no page argument; this applies its own
analyze() to the added lines of every page, and says which pages the gate itself judges.
"""
import subprocess
import sys

sys.path.insert(0, "scripts")
import check_doc_style as c  # noqa: E402

base = sys.argv[1]
head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
print(f"head {head}, lines added since {base}")
pages = subprocess.run(["git", "diff", "--name-only", base, "HEAD", "--", "*.md"],
                       capture_output=True, text=True, check=True).stdout.split()
for p in pages:
    diff = subprocess.run(["git", "diff", "-U0", base, "HEAD", "--", p], capture_output=True, text=True, check=True).stdout
    added = "\n".join(line[1:] for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++"))
    found = list(c.analyze(added))
    gated = any(str(d).endswith(p) for d in c.DOCUMENTS)
    print(f"{p}: {'judged by the gate' if gated else 'not in the gate population'}; findings on added lines: {len(found)}")
    for f in found:
        print(f"    {f.reason}: {' '.join(f.text.split())[:110]}")
