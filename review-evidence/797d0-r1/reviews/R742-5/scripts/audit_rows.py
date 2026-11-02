"""Compare inventory statuses and findings rows of docs/DOCUMENTATION_AUDIT.md at two commits.
Usage: python3 -I audit_rows.py REPO OLD NEW"""
import re, subprocess, sys
from collections import Counter
repo, old, new = sys.argv[1:4]
def load(rev):
    t = subprocess.run(["git", "-C", repo, "show", f"{rev}:docs/DOCUMENTATION_AUDIT.md"], capture_output=True, text=True, check=True).stdout
    inv, fnd = {}, []
    sec = None
    for line in t.splitlines():
        if line.startswith("## "): sec = line[3:].strip()
        if not line.startswith("| ") or line.startswith("|---"): continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
        if sec == "Inventory" and len(cells) >= 9 and cells[0].startswith("["):
            inv[cells[0]] = cells[5]
        if sec == "Findings" and cells and re.fullmatch(r"D0-\d+", cells[0]):
            fnd.append((cells[0], cells[1], cells[2], cells[4][:20]))
    return inv, fnd
oi, of = load(old); ni, nf = load(new)
print("pages", len(oi), "->", len(ni), "status", dict(Counter(oi.values())), "->", dict(Counter(ni.values())))
for p in sorted(set(oi) | set(ni)):
    if oi.get(p) != ni.get(p): print("  status", p, oi.get(p), "->", ni.get(p))
def copies(f): return [r for r in f if r[3].startswith("Copy of")]
print("finding rows", len(of), "->", len(nf), "copy rows", len(copies(of)), "->", len(copies(nf)))
ok = {(a, b): c for a, b, c, _ in of}; nk = {(a, b): c for a, b, c, _ in nf}
for k in sorted(set(ok) | set(nk)):
    if ok.get(k) != nk.get(k): print("  row", k, ok.get(k), "->", nk.get(k))
print("distinct ids", len({r[0] for r in of}), "->", len({r[0] for r in nf}))
