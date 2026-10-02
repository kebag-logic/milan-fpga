#!/usr/bin/env python3
"""List numeric figures (and short hex/commit tokens) present in an older PR
body but absent from a newer one.  usage: figures_kept.py OLD.md NEW.md"""
import collections, re, sys
TOK = re.compile(r"(?<![\w.])(?:\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?:\s*(?:/|of|<=|==|=|\+|x)\s*\d[\d,]*)?(?![\w])|`[0-9a-f]{7,12}`")
def toks(p):
    return collections.Counter(m.group(0).replace(" ", "") for m in TOK.finditer(open(p).read()))
old, new = toks(sys.argv[1]), toks(sys.argv[2])
missing = sorted(t for t in old if t not in new)
print(f"distinct figures: old {len(old)}, new {len(new)}; in old but absent from new: {len(missing)}")
for t in missing:
    print("  ", t)
