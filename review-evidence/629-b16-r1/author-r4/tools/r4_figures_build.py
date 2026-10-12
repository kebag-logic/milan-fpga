#!/usr/bin/env python3
"""Lane B16, round 4: write check_b16_figures.py's ROWS_TSV and EXCLUDE blocks from r4_figures_spec.py.

usage: r4_figures_build.py <findings.md> <r4_figures_spec.py> <check_b16_figures.py> <out check.py>

An authoring aid: it resolves each spec anchor to its line number on the page (or in the findings index
beside it), resolves each marked figure to its occurrence on that line, and writes the rows, one per
line, into a copy of the check. Run on the committed page and the packet's spec, it reproduces the
packet's check byte for byte. It reads nothing else.

Round 3's r3_figures_build.py, with two changes: a row may give its occurrence index itself (a fifth
field), and the spec's GEN3, when present, is given every covered line, the README row's from the column
its lane B16 part starts at, with the check's token regex, so it can emit one row per token it selects.
"""
import re
import runpy
import sys

DOC, SPEC, CHK, OUT = sys.argv[1:5]
doc = open(DOC, encoding="utf-8").read().splitlines()
readme = open(DOC.rsplit("/", 1)[0] + "/README.md", encoding="utf-8").read().splitlines()
s = next(i for i, x in enumerate(doc) if x.startswith("## Dev 5603c353, 2026-10-12: lane B16"))
e = next((i for i in range(s + 1, len(doc)) if doc[i].startswith("## ")), len(doc))
intro = next(i for i, x in enumerate(doc) if x.startswith("Lane B16 tried the reference peer's own loopback"))
SCOPE = (list(range(s, e)) + [i for i in range(intro, intro + 40) if all(doc[j].strip() for j in range(intro, i + 1))]
         + [next(i for i, x in enumerate(doc) if x.startswith("- **[Dev 5603c353, 2026-10-12: lane B16]"))])
RROW = next(i for i, x in enumerate(readme) if x.startswith("| [629_MEDIA_CLOCK_FOLLOWING_BENCH.md]"))
csrc = open(CHK).read()
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
TENS = ["thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand"]
TOK = eval("re.compile(" + re.search(r"TOKEN = re.compile\((.*?)\)\n\n", csrc, re.S).group(1) + ")")
spec = runpy.run_path(SPEC)
out, errs = [], 0


def occurrence(line, shown):
    """A marked figure `pre «fig» post`: the figure and its occurrence index on the line."""
    pre, rest = shown.split("«", 1)
    fig, post = rest.split("»", 1)
    pos = line.find(pre + fig + post)
    assert pos >= 0 and line.find(pre + fig + post, pos + 1) < 0, (pre + fig + post)
    starts = [m.start() for m in TOK.finditer(line) if m.group(0) == fig]
    return fig, starts.index(pos + len(pre))


def emit(where, line, row):
    shown, src, key, fmt = row[:4]
    k = row[4] if len(row) > 4 else None
    if "«" in shown:
        shown, k = occurrence(line, shown)
    if src and f"'{src}'" in key and "d[" not in key and "(d," not in key and "(d)" not in key and " d " not in key:
        src = ""
    out.append(f"{where}\t{shown}\t{src}\t{fmt}" + ("" if k is None else f"#{k}") + f"\t{key}")


for anchor, n, rows, comment, off, dname in spec["L"]:
    lines = readme if dname else doc
    hits = [i + 1 for i in (range(len(readme)) if dname else SCOPE) if anchor in lines[i]]
    if not hits or (n is None and len(hits) != 1) or (n is not None and n >= len(hits)):
        print("ANCHOR", repr(anchor), hits)
        errs += 1
        continue
    ln = hits[0 if n is None else n] + off
    if comment:
        out.append(f"# {comment}")
    for row in rows:
        emit(f"{dname}:{ln}" if dname else str(ln), lines[ln - 1], row)
out.append("# hash tables: one row per byte count and SHA-256")
for ln, rows in spec["GEN"](doc, s, e) + spec["GEN2"](doc, s, e):
    for row in rows:
        emit(str(ln), doc[ln - 1], row)
if "GEN3" in spec:
    covered = [(str(i + 1), doc[i], 0) for i in sorted(set(SCOPE))]
    covered.append((f"README.md:{RROW + 1}", readme[RROW], readme[RROW].index("Lane B16, `5603c353`:")))
    out.append("# round 4: rows GEN3 selects by token")
    for where, rows in spec["GEN3"](covered, TOK):
        line = readme[RROW] if where.startswith("README.md:") else doc[int(where) - 1]
        for row in rows:
            emit(where, line, row)
assert not errs
assert '"""' not in "\n".join(out)
a, b = csrc.index("# ROWS-BEGIN\n") + len("# ROWS-BEGIN\n"), csrc.index("# ROWS-END")
csrc = csrc[:a] + "\n".join(out) + "\n" + csrc[b:]
a, b = csrc.index("# EXCLUDE-BEGIN\n") + len("# EXCLUDE-BEGIN\n"), csrc.index("# EXCLUDE-END")
csrc = csrc[:a] + spec["X"].strip("\n") + "\n" + csrc[b:]
open(OUT, "w").write(csrc)
print("rows", sum(1 for x in out if not x.startswith("#")))
