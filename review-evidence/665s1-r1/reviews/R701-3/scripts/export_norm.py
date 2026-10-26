#!/usr/bin/env python3
"""For each file differing raw between base1 and head, compare normalised bytes:
text: drop lines holding a date-time stamp, and sort the LiteX hierarchy-tree
lines (glyph-folded) to the end; ar archives: member names and bytes, without
header times/uids/modes. Prints per file 'same' or the first differing lines.
Usage: export_norm.py <base1> <base2> <head>  (exit 1 on any normalised difference)"""
import hashlib, re, sys, difflib
from pathlib import Path
STAMP = re.compile(rb"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}")
BOX = ("│", "├", "└")
def norm(p: Path) -> bytes:
    d = p.read_bytes()
    if d.startswith(b"!<arch>\n"):
        out, pos = [], 8
        while pos + 60 <= len(d):
            h = d[pos:pos + 60]; n = int(h[48:58].strip())
            out.append(h[0:16] + b"|" + d[pos + 60:pos + 60 + n]); pos += 60 + n + (n & 1)
        return b"\0".join(out)
    ls = [l for l in d.split(b"\n") if not STAMP.search(l)]
    tree = sorted(l.replace("└".encode(), "├".encode()) for l in ls if l.decode("utf-8", "replace").lstrip().startswith(BOX))
    rest = [l for l in ls if not l.decode("utf-8", "replace").lstrip().startswith(BOX)]
    return b"\n".join(rest + tree)
b1, b2, h = map(Path, sys.argv[1:4]); bad = 0
for p in sorted(x for x in b1.rglob("*") if x.is_file()):
    rel = p.relative_to(b1); q = h / rel; r = b2 / rel
    if p.read_bytes() == q.read_bytes(): continue
    if rel.name == "litex.log": print("skip-log", rel); continue
    nb1, nh, nb2 = norm(p), norm(q), norm(r)
    if nb1 == nh: print("same-normalised", rel, "(base-vs-base normalised", "same)" if nb1 == nb2 else "DIFFER)")
    else:
        bad += 1; print("DIFF", rel)
        for l in list(difflib.unified_diff(nb1.decode("latin1").split("\n"), nh.decode("latin1").split("\n"), lineterm="", n=0))[:12]: print("   ", l[:200])
print("normalised differences:", bad); sys.exit(1 if bad else 0)
