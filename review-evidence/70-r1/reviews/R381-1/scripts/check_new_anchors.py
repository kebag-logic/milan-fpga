#!/usr/bin/env python3
"""Check every relative link+anchor on added lines of base..HEAD resolves.

Run from the repository root: check_new_anchors.py <base>
Slugs use GitHub's rule (lowercase, drop punctuation except '-' and '_',
spaces to '-'), plus explicit <a id=...> anchors. Exit 1 on any miss.
"""
import os, re, subprocess, sys
base = sys.argv[1]
diff = subprocess.run(["git", "diff", "-U0", base, "HEAD", "--", "*.md"],
                      capture_output=True, text=True).stdout
cur = None; links = []
for l in diff.splitlines():
    if l.startswith("+++ b/"): cur = l[6:]
    elif l.startswith("+") and not l.startswith("+++"):
        for m in re.finditer(r"\]\(([^)\s]+)\)", l):
            links.append((cur, m.group(1)))
def slugs(path):
    out = set(); counts = {}; fence = False
    for line in open(path, encoding="utf-8"):
        if line.lstrip().startswith("```"): fence = not fence; continue
        for m in re.finditer(r'<a id="([^"]+)"', line): out.add(m.group(1))
        if fence: continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if not m: continue
        t = re.sub(r"<[^>]+>", "", m.group(2)).strip().lower()
        t = re.sub(r"[`*]", "", t)
        s = re.sub(r"[^\w\- ]", "", t).replace(" ", "-")
        n = counts.get(s, 0); counts[s] = n + 1
        out.add(s if n == 0 else f"{s}-{n}")
    return out
bad = 0; seen = set()
for src, link in links:
    if link.startswith("http") or (src, link) in seen: continue
    seen.add((src, link))
    path, _, frag = link.partition("#")
    tgt = os.path.normpath(os.path.join(os.path.dirname(src), path)) if path else src
    ok = os.path.exists(tgt) and (not frag or not tgt.endswith(".md") or frag in slugs(tgt))
    print(("OK  " if ok else "MISS"), src, "->", link); bad += not ok
print("RESULT", "PASS" if not bad else f"FAIL {bad}")
sys.exit(1 if bad else 0)
