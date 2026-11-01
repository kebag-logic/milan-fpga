#!/usr/bin/env python3
"""Print every line a changed correction or source cell cites, and compare moved citations across rounds.

Usage: citations_probe.py REPO OLD_COMMIT
Reads scripts/docs_inventory.json at HEAD and OLD_COMMIT in REPO. Submodule paths read the working tree
(the pinned checkout), so run on a clean tree.
"""
import json, re, subprocess, sys
from pathlib import Path
repo, old = Path(sys.argv[1]), sys.argv[2]
def show(c, p):
    r = subprocess.run(["git", "-C", str(repo), "show", f"{c}:{p}"], capture_output=True)
    return r.stdout.decode("utf-8", "replace").split("\n") if r.returncode == 0 else None
def head_lines(p):
    f = repo / p
    return f.read_text(encoding="utf-8", errors="replace").split("\n") if f.is_file() else None
new_data = json.loads((repo / "scripts/docs_inventory.json").read_text())
old_data = json.loads(subprocess.run(["git", "-C", str(repo), "show", f"{old}:scripts/docs_inventory.json"],
                                     capture_output=True, text=True).stdout)
olds = {f["id"]: f for f in old_data["findings"]}
news = {f["id"]: f for f in new_data["findings"]}
CITE = re.compile(r"`([\w./+-]+\.\w+|[\w./+-]+/Makefile)`(?:'s own [^()]*?)?(?:\s*(?:lines?|\(lines?)\s*([\d, and-]+\d))?")
def citations(text):
    """(path, [(a,b),...]) in reading order; a bare `line N` in the cell refers to the last named path."""
    out, last = [], None
    pos = 0
    for m in re.finditer(r"`([\w./+-]+(?:\.\w+|/Makefile))`|\b[Ll]ines? (\d+(?:-\d+)?(?:(?:, | and )\d+(?:-\d+)?)*)", text):
        if m.group(1):
            last = m.group(1); out.append((last, None))
        elif last:
            out.append((last, m.group(2)))
    return [c for c in out if c[1]]
def spans(s):
    r = []
    for part in re.split(r", | and ", s):
        a, _, b = part.partition("-")
        r.append((int(a), int(b or a)))
    return r
mode = sys.argv[3] if len(sys.argv) > 3 else "changed"
print("removed:", sorted(set(olds) - set(news)), "added:", sorted(set(news) - set(olds)))
chg_corr = [i for i in news if i in olds and olds[i]["correction"] != news[i]["correction"]] + sorted(set(news)-set(olds))
print("corrections added or changed:", chg_corr)
print("source cell changed:", [i for i in news if i in olds and olds[i]["source"] != news[i]["source"]])
for i in chg_corr:
    f = news[i]
    print(f"\n===== {i} page={f['page']}\nCORRECTION: {f['correction']}\nCITED IN CORRECTION CELL: {len(citations(f['correction']))}")
    for field in ("correction", "source"):
        for path, ls in citations(f[field]):
            lines = head_lines(path)
            print(f"--- [{field}] {path} {ls}" + ("  (FILE MISSING)" if lines is None else ""))
            if lines is None: continue
            for a, b in spans(ls):
                for n in range(a, min(b, a + 39) + 1):
                    print(f"{n:6d}: {lines[n-1] if n <= len(lines) else '<past EOF>'}")
print("\n\n######## MOVED CITATIONS: old text at old citation vs new text at new citation")
moved = same = differ = 0
for i, f in news.items():
    if i not in olds: continue
    for field in ("source", "correction"):
        oc, nc = citations(olds[i][field]), citations(f[field])
        if oc == nc:
            # unchanged citation: did the text under it change between rounds?
            for path, ls in nc:
                o, n = show(old, path), head_lines(path)
                if o is None or n is None: continue
                for a, b in spans(ls):
                    ot, nt = o[a-1:b], n[a-1:b]
                    if ot != nt:
                        differ += 1
                        print(f"UNMOVED-BUT-TEXT-CHANGED {i} {field} {path} {a}-{b}\n  old: {ot[:2]}\n  new: {nt[:2]}")
                    else:
                        same += 1
            continue
        if len(oc) != len(nc):
            print(f"CITATION-SET-CHANGED {i} {field}: {oc} -> {nc}")
            continue
        for (op, ol), (np, nl) in zip(oc, nc):
            if (op, ol) == (np, nl):
                o, n = show(old, op), head_lines(np)
                if o is None or n is None: continue
                for a, b in spans(ol):
                    if o[a-1:b] != n[a-1:b]:
                        differ += 1
                        print(f"KEPT-IN-CHANGED-CELL-TEXT-CHANGED {i} {field} {op} {a}-{b}\n  old: {o[a-1:b][:2]}\n  new: {n[a-1:b][:2]}")
                    else:
                        same += 1
                continue
            moved += 1
            o, n = show(old, op), head_lines(np)
            if o is None or n is None: print("MISSING", i, op, np); continue
            ot = [t.strip() for a, b in spans(ol) for t in o[a-1:b]]
            nt = [t.strip() for a, b in spans(nl) for t in n[a-1:b]]
            if ot != nt:
                print(f"MOVED-TEXT-DIFFERS {i} {field} {op} {ol} -> {np} {nl}\n  old: {ot[:3]}\n  new: {nt[:3]}")
print(f"moved={moved} unmoved_same={same} unmoved_differ={differ}")
