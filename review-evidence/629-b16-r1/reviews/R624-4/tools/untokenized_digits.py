#!/usr/bin/env python3
"""R624-4: every digit run in the figures check's scope that its TOKEN regex never reads.

usage: untokenized_digits.py <check_b16_figures.py> <findings.md> <out.tsv>

Imports nothing from the check: it reads the check's TOKEN source text and SECTION/scope rules by
re-implementing the scope (the B16 section, the introduction paragraph on lane B16, the Contents entry
and the lane B16 part of the README row) and compiling TOKEN from the check's own source. Each digit run
that no token spans is written with its context, grouped by the characters around it.
"""
import re
import sys
from collections import Counter
from pathlib import Path

CHECK, DOC, OUT = sys.argv[1:4]
src = Path(CHECK).read_text()
ns = {"re": re}
words = re.search(r"^WORDS = (\[.*?\])\n", src, re.S | re.M).group(1)
tens = re.search(r"^TENS = (\[.*?\])", src, re.M).group(1)
ns["WORDS"] = eval(words)
ns["TENS"] = eval(tens)
tok_src = re.search(r"^TOKEN = (re\.compile\(.*?\n\s+r\"\|\\b\(\?P<word>.*?\)\n)", src, re.S | re.M).group(1)
TOKEN = eval(tok_src, ns)

f = Path(DOC).read_text(encoding="utf-8").splitlines()
r = (Path(DOC).parent / "README.md").read_text(encoding="utf-8").splitlines()
scope = {}
s = next(i for i, x in enumerate(f) if x.startswith("## Dev 5603c353, 2026-10-12: lane B16"))
e = next((i for i in range(s + 1, len(f)) if f[i].startswith("## ")), len(f))
for i in range(s, e):
    scope[("page", i + 1)] = (f[i], 0)
i = next(i for i, x in enumerate(f) if x.startswith("Lane B16 tried the reference peer's own loopback"))
while f[i].strip():
    scope[("page", i + 1)] = (f[i], 0)
    i += 1
i = next(i for i, x in enumerate(f) if x.startswith("- **[Dev 5603c353, 2026-10-12: lane B16]"))
scope[("page", i + 1)] = (f[i], 0)
i = next(i for i, x in enumerate(r) if x.startswith("| [629_MEDIA_CLOCK_FOLLOWING_BENCH.md]"))
scope[("README", i + 1)] = (r[i], r[i].index("Lane B16, `5603c353`:"))

rows = []
shape = Counter()
for (d, n), (text, at) in sorted(scope.items()):
    spans = [m.span() for m in TOKEN.finditer(text) if m.start() >= at]
    for m in re.finditer(r"\d+", text):
        if m.start() < at:
            continue
        if any(a <= m.start() and m.end() <= b for a, b in spans):
            continue
        # skip anything inside a link target (URL or anchor) and inside a 64-hex/backtick path
        ctx = text[max(0, m.start() - 25): m.end() + 25]
        pre = re.search(r"[\w\-./#]*$", text[:m.start()]).group(0)
        post = re.match(r"[\w\-./]*", text[m.end():]).group(0)
        word = pre + m.group(0) + post
        inlink = any(a <= m.start() < b for a, b in (x.span() for x in re.finditer(r"\]\([^)]*\)", text)))
        incode = text[:m.start()].count("`") % 2 == 1
        kind = "link-target" if inlink else ("code" if incode else "prose")
        shape[(kind, re.sub(r"\d+", "N", word))] += 1
        rows.append((d, n, kind, word, ctx.replace("\t", " ")))
with open(OUT, "w") as o:
    o.write("doc\tline\tkind\tword\tcontext\n")
    for x in rows:
        o.write("\t".join(map(str, x)) + "\n")
print("untokenized digit runs:", len(rows))
for (k, w), c in sorted(shape.items(), key=lambda x: (x[0][0], -x[1])):
    if k != "link-target":
        print(f"{c:4d}  {k:6s} {w}")
