"""Compare a base and a head LiteX export made from one tree path into one output path.

Usage: compare_same.py <base-out> <head-out> <report.json>
Exit 0 when every file is byte-identical or differs only by one of the stated
normalisations; 1 otherwise. The normalisations, and nothing else:
  stamp  a line carrying the run's date or time (LiteX headers, litex.log);
  ar     an ar archive's member header mtime (members compared name and bytes);
  tree   the generated Verilog's date lines and its comment-only hierarchy
         tree, the tree compared as a multiset of lines (its order varies);
  log    litex.log, a record of the run and not a build input or output,
         compared as a multiset of lines without its date lines (parallel
         make prints in any order).
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

base, head, report = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
STAMP = re.compile(rb"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}")


def ar_members(data: bytes):
    """(name, bytes) of every member of a System V / GNU ar archive."""
    if not data.startswith(b"!<arch>\n"):
        return None
    out, pos = [], 8
    while pos + 60 <= len(data):
        hdr = data[pos:pos + 60]
        size = int(hdr[48:58].strip())
        out.append((hdr[0:16], data[pos + 60:pos + 60 + size]))
        pos += 60 + size + (size & 1)
    return out


BOX = ("\u2502", "\u251c", "\u2514")


def tree_split(data: bytes):
    """The Verilog without its date lines and hierarchy-tree lines, and the tree's lines."""
    keep, tree = [], []
    for ln in data.split(b"\n"):
        text = ln.decode("utf-8", errors="replace")
        if STAMP.search(ln):
            continue
        if text.lstrip().startswith(BOX):
            tree.append(ln)
            continue
        keep.append(ln)
    return b"\n".join(keep), collections.Counter(tree)


files = sorted({p.relative_to(base) for p in base.rglob("*") if p.is_file()} |
               {p.relative_to(head) for p in head.rglob("*") if p.is_file()})
res = {"files": len(files), "identical": 0, "stamp": [], "ar": [], "tree": [], "log": [], "different": [],
       "missing": []}
for rel in files:
    b, h = base / rel, head / rel
    if not (b.is_file() and h.is_file()):
        res["missing"].append(str(rel))
        continue
    bd, hd = b.read_bytes(), h.read_bytes()
    if bd == hd:
        res["identical"] += 1
        continue
    entry = {"file": str(rel), "base_sha256": hashlib.sha256(bd).hexdigest(),
             "head_sha256": hashlib.sha256(hd).hexdigest()}
    ba, ha = ar_members(bd), ar_members(hd)
    if ba is not None and ha is not None:
        if ba == ha:
            res["ar"].append(entry)
        else:
            res["different"].append(entry)
        continue
    if rel.suffix == ".v":
        (bk, bt), (hk, ht) = tree_split(bd), tree_split(hd)
        if bk == hk and bt == ht:
            res["tree"].append(entry)
            continue
    if rel.name == "litex.log":
        bc = collections.Counter(x for x in bd.split(b"\n") if not STAMP.search(x))
        hc = collections.Counter(x for x in hd.split(b"\n") if not STAMP.search(x))
        (res["log"] if bc == hc else res["different"]).append(entry)
        continue
    bl, hl = bd.split(b"\n"), hd.split(b"\n")
    if len(bl) == len(hl) and all(x == y or (STAMP.search(x) and STAMP.search(y)) for x, y in zip(bl, hl)):
        res["stamp"].append(entry)
        continue
    res["different"].append(entry)
report.write_text(json.dumps(res, indent=1) + "\n")
summary = {k: (len(v) if isinstance(v, list) else v) for k, v in res.items()}
print(json.dumps(summary))
for d in res["different"] + [{"file": m} for m in res["missing"]]:
    print("DIFFERENT", d["file"])
sys.exit(1 if res["different"] or res["missing"] else 0)
