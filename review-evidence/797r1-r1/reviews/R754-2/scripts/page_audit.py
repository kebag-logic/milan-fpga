#!/usr/bin/env python3
"""Audit the published page without the generator: prose blocks, table cells, one-column tables,
heading and summary resets against simulated reset, and rows for strobe-like access codes.
Usage: page_audit.py <page> <sim_reset.txt>"""
import re, sys
page, simr = sys.argv[1:3]
L = open(page, encoding="utf-8").read().split("\n")
rst = {0: {}, 1: {}}
for ln in open(simr):
    _, pat, a, v, ok = ln.split(); rst[int(pat)][int(a, 16)] = int(v, 16)
incode = False; blocks = []; cur = []; cells = []; onecol = 0; tbl_words = 0
for i, l in enumerate(L, 1):
    if l.startswith("```"):
        incode = not incode
        if cur: blocks.append(cur); cur = []
        continue
    if incode: continue
    if l.startswith("|"):
        if cur: blocks.append(cur); cur = []
        cs = [c.strip() for c in re.split(r"(?<!\\)\|", l)[1:-1]]
        if len(cs) == 1: onecol += 1
        for c in cs:
            n = len(c.split()); cells.append((n, i)); tbl_words += n
        continue
    if not l.strip() or l.startswith("#") or l.startswith("!["):
        if cur: blocks.append(cur); cur = []
        continue
    cur.append((i, l))
if cur: blocks.append(cur)
def words(b): return sum(len(l.split()) for _, l in b)
big = [(words(b), b[0][0]) for b in blocks if words(b) > 20]
print("prose blocks", len(blocks), "words", sum(words(b) for b in blocks), "over-20", big[:20])
print("one-column table rows", onecol, "table words", tbl_words)
cells.sort(reverse=True)
print("largest cells", cells[:12])
for t in (20, 50, 100, 150, 200):
    print(f"cells > {t}:", sum(1 for n, _ in cells if n > t))
hdr = re.compile(r"^### (\S+) registers? \(offset (0x[0-9A-Fa-f]+)(?: to (0x[0-9A-Fa-f]+), stride (0x[0-9A-Fa-f]+))?\)\s*\[reset = ([^\]]+)\]")
bad = n = 0
for i, l in enumerate(L, 1):
    m = hdr.match(l)
    if not m: continue
    n += 1
    a = int(m.group(2), 16); r = m.group(5).replace("_", "")
    if "see" in r or "`" in r: print("heading-other", l[:100]); continue
    mh = re.fullmatch(r"0x([0-9A-FaX-]{8})", r)
    if not mh: print("heading-fmt", l[:100]); continue
    h = mh.group(1)
    for k in range(8):
        c = h[k]; sh = (7 - k) * 4; hw0 = (rst[0][a] >> sh) & 15; hw1 = (rst[1][a] >> sh) & 15
        if c in "X-": continue
        if int(c, 16) != hw0:
            bad += 1; print("HEADING-RESET", m.group(1), hex(a), r, hex(rst[0][a]))
            break
print("headings", n, "mismatch", bad)
sum_bad = 0; ns = 0
for l in L:
    m = re.match(r"^\| `?(0x[0-9A-F]{3})`? \| .*\| `?(0x[0-9A-FX_]{8,})`? \| \[", l)
    if m:
        ns += 1
        a = int(m.group(1), 16); r = m.group(2).replace("_", "")
        for k, c in enumerate(r[2:]):
            sh = (7 - k) * 4
            if c != "X" and int(c, 16) != (rst[0].get(a, 0) >> sh) & 15:
                sum_bad += 1; print("SUMMARY-RESET", l[:110], hex(rst[0][a])); break
print("summary rows", ns, "mismatch", sum_bad)
