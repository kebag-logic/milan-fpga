#!/usr/bin/env python3
"""Search with no line-marker stripping and with the markers kept out of the comparison: a wrap before + or - or 1. must still match.
Usage: raw_wrap_search.py REPO"""
import json, re, subprocess, sys
repo = sys.argv[1]
names = subprocess.check_output(["git", "-C", repo, "ls-files"], text=True).split("\n")
pages = [n for n in names if n and (n.endswith(".md") or n.split("/")[-1].upper().startswith("README")) and n != "docs/DOCUMENTATION_AUDIT.md"]
def plain(t):
    t = re.sub(r"(?m)^\s*(?:>\s*)+", "", t)
    t = re.sub(r"[`*]", "", t)
    return re.sub(r"\s+", " ", t.replace("\n\n", " \f ")).casefold()
data = json.load(open(f"{repo}/scripts/docs_inventory.json"))
texts = {p: plain(open(f"{repo}/{p}", encoding="utf-8", errors="replace").read()) for p in pages}
audit = open(f"{repo}/docs/DOCUMENTATION_AUDIT.md").read()
rows = set()
for line in audit.split("\n"):
    m = re.match(r"\| (D0-\d+) \| \[[^\]]*\]\(([^)]*)\) \|", line)
    if m:
        t = m.group(2); rows.add((m.group(1), t[3:] if t.startswith("../") else "docs/" + t))
extra = []
for f in data["findings"]:
    for s in [f["quote"], *f.get("also", [])]:
        n = plain(s).strip()
        for p, t in texts.items():
            if n in t and (f["id"], p) not in rows:
                extra.append((f["id"], p, s))
print("pairs found with markers kept and no row:", len(extra))
for e in extra:
    print("  ", e)
