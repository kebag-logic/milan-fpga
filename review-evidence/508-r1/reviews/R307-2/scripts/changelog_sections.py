#!/usr/bin/env python3
"""Compare CHANGELOG.md '## ' sections between two revisions byte for byte and
report where processor issue 116/113 lines occur at the second.
Usage: changelog_sections.py <repo> <rev_a> <rev_b>"""
import hashlib, subprocess, sys
repo, a, b = sys.argv[1:4]
def sections(rev):
    t = subprocess.run(["git", "show", f"{rev}:CHANGELOG.md"], cwd=repo, check=True,
                       capture_output=True).stdout.decode()
    out, cur, buf = {}, None, []
    for ln in t.splitlines(keepends=True):
        if ln.startswith("## "):
            if cur: out[cur] = "".join(buf)
            cur, buf = ln.strip(), [ln]
        elif cur: buf.append(ln)
    if cur: out[cur] = "".join(buf)
    return out
sa, sb = sections(a), sections(b)
for k in sb:
    if k in sa:
        st = "IDENTICAL" if sa[k] == sb[k] else "DIFFERS"
    else:
        st = "NEW-AT-B"
    print(f"{st:9} {hashlib.sha256(sb[k].encode()).hexdigest()[:16]} {k}")
for k in sa:
    if k not in sb: print(f"MISSING-AT-B {k}")
for k, v in sb.items():
    for i, ln in enumerate(v.splitlines(), 1):
        if "Processor issue 116" in ln or "Processor issue 113" in ln:
            print(f"  processor 116/113 line in [{k}] +{i}: {ln}")
