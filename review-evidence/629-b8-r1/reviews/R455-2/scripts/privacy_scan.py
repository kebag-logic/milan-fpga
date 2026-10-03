#!/usr/bin/env python3
"""Value-blind privacy scan for the B8 delta.

usage: privacy_scan.py TOKENS_FILE PATH...
TOKENS_FILE holds the masked token(s) derived from the published grader's
mask diff; it is never printed. For each scanned file the scan reports only
counts and line numbers of:
  near   - a masked token within 40 characters of a channel word
  fmt    - a sample-format-name shape (sign letter, bit width, endianness suffix)
  hidden - a claim that the layout or decode is hidden/masked
No matched text is printed.
"""
import os, re, sys
toks = [t for t in open(sys.argv[1]).read().split() if t]
chan = re.compile(r"chan|ch\b|channels", re.I)
fmt = re.compile(r"\b(?:[SU](?:8|16|18|20|24|32)(?:_3)?_?[LB]E|FLOAT(?:64)?_?[LB]E|S24_3[LB]E)\b")
hid = re.compile(r"(layout|byte order|byte width|decode)[^.\n]{0,60}(hidden|masked|withheld|redact)|(hidden|masked|withheld|redact)[^.\n]{0,60}(layout|byte order|byte width|decode)", re.I)
paths = []
for p in sys.argv[2:]:
    if os.path.isdir(p):
        for d, _, fs in os.walk(p):
            paths += [os.path.join(d, f) for f in fs]
    else:
        paths.append(p)
tot = {"near": 0, "fmt": 0, "hidden": 0}
for p in sorted(paths):
    try:
        lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
    except Exception:
        continue
    hits = {"near": [], "fmt": [], "hidden": []}
    for i, l in enumerate(lines, 1):
        for t in toks:
            for m in re.finditer(r"(?<![0-9A-Za-z_.])" + re.escape(t) + r"(?![0-9A-Za-z_])", l):
                w = l[max(0, m.start() - 40): m.end() + 40]
                if chan.search(w):
                    hits["near"].append(i)
        if fmt.search(l):
            hits["fmt"].append(i)
        if hid.search(l):
            hits["hidden"].append(i)
    for k, v in hits.items():
        if v:
            tot[k] += len(v)
            print("%s %s lines %s" % (k, p, sorted(set(v))[:20]))
print("TOTAL", tot, "files", len(paths))
