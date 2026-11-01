#!/usr/bin/env python3
"""Search every recorded statement and spelling with a normaliser written apart from the generator, and compare with the audit rows.
A stronger normaliser than the generator's: also drops link targets, underscore emphasis, HTML breaks and table escapes.
Usage: independent_search.py REPO"""
import json, re, subprocess, sys, unicodedata
repo = sys.argv[1]
names = subprocess.check_output(["git", "-C", repo, "ls-files"], text=True).split("\n")
pages = [n for n in names if n and (n.endswith(".md") or n.split("/")[-1].upper().startswith("README"))]
AUDIT = "docs/DOCUMENTATION_AUDIT.md"
def strong(text):
    t = unicodedata.normalize("NFKC", text)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<br\s*/?>", " ", t, flags=re.I)
    t = t.replace("\\|", "|")
    lines = []
    for line in t.split("\n"):
        line = re.sub(r"^\s*(?:>\s*)*(?:[-*+]\s+|\d+[.)]\s+)?", "", line)
        lines.append(line if line.strip() else "\f")
    t = " ".join(lines)
    t = re.sub(r"[`*]|(?<![A-Za-z0-9])_+|_+(?![A-Za-z0-9])", "", t)
    return re.sub(r"[ \t]+", " ", t).casefold()
data = json.load(open(f"{repo}/scripts/docs_inventory.json"))
texts = {p: strong(open(f"{repo}/{p}", encoding="utf-8", errors="replace").read()) for p in pages if p != AUDIT}
audit = open(f"{repo}/{AUDIT}", encoding="utf-8").read()
rows = set()
for line in audit.split("\n"):
    m = re.match(r"\| (D0-\d+) \| \[[^\]]*\]\(([^)]*)\) \| ([^|]*) \|", line)
    if m:
        target = m.group(2)
        path = target[3:] if target.startswith("../") else "docs/" + target
        rows.add((m.group(1), path))
want = {}
for f in data["findings"]:
    want[(f["id"], f["page"])] = "recorded"
    for s in [f["quote"], *f.get("also", [])]:
        needle = strong(s).strip()
        for p, t in texts.items():
            if re.search(r"(?<!\w)" + re.escape(needle) + r"(?!\w)", t) or (not needle[-1].isalnum() and needle in t):
                want.setdefault((f["id"], p), s)
print("recorded findings", len(data["findings"]), "pages searched", len(texts), "rows on audit", len(rows), "pairs found", len(want))
print("found by the independent search but no row:")
missing = sorted(set(want) - rows)
for k in missing:
    print("  ", k, "::", want[k])
print("row on the audit but not found by the independent search:")
for k in sorted(rows - set(want)):
    print("  ", k)
