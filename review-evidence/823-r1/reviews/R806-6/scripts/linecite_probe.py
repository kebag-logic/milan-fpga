#!/usr/bin/env python3
"""Probe the format page drift gate's line-citation rule at a clone's head.

Usage: python3 -I linecite_probe.py <clone>

1. Each citation form is run through the gate's own findings() on the real page
   plus one planted sentence; prints CAUGHT or MISSED per form.
2. The old single-form pattern is restored in a copy of the module, and the
   gate's self-test plant table is replayed against it: each new plant must be
   MISSED by the old pattern (shows the plants can fail).
3. False positives: the rule is run over every tracked docs/**/*.md page and the
   counts are printed (informational; only the format page is gated).
"""
import re
import subprocess
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(clone / "scripts")]
import check_nvm_format_32x32 as g  # noqa: E402

page = g.PAGE.read_text(encoding="utf-8")
index = g.INDEX.read_text(encoding="utf-8")
r = g.compute()
anchors = g.tables.LAYERS + g.tables.VERSION_CHAIN + g.tables.CITED
base = g.findings(page, index, r, anchors)
print(f"baseline findings: {len(base)}")

FORMS = [
    ("backticked single", "`sw/litex/milan_soc.py:179`"),
    ("backticked range", "`sw/litex/milan_soc.py:179-181`"),
    ("backticked list", "`scripts/nvm_klj3.py:408,465`"),
    ("list with spaces", "`scripts/nvm_klj3.py:408, 465`"),
    ("unquoted single", "sw/litex/milan_soc.py:179"),
    ("backticked path line N", "`sw/litex/milan_soc.py` line 179"),
    ("backticked path lines N-M", "`sw/litex/milan_soc.py` lines 179-181"),
    ("#L link", "[map](../../sw/litex/milan_soc.py#L179)"),
    ("#L range link", "[map](../../sw/litex/milan_soc.py#L179-L181)"),
    ("unquoted path line N", "sw/litex/milan_soc.py line 179"),
    ("line N of path", "line 179 of `sw/litex/milan_soc.py`"),
    ("path, line N", "`sw/litex/milan_soc.py`, line 179"),
    ("path:LN", "`sw/litex/milan_soc.py:L179`"),
    ("path (line N)", "`sw/litex/milan_soc.py` (line 179)"),
]
for name, text in FORMS:
    got = g.findings(page + f"\nSee {text}.\n", index, r, anchors)
    new = [x for x in got if x not in base]
    print(f"{'CAUGHT' if any('by line number' in x for x in new) else 'MISSED'}  {name:<28} {text}")

OLD = re.compile(r"`([\w./-]+\.[A-Za-z]\w*):(\d+)`")
print("\nold single-form pattern against the gate's six plants:")
for written, named in g.LINE_CITE_PLANTS:
    hit = OLD.search(f"See {written}.")
    print(f"{'caught' if hit else 'MISSED'} by old pattern: {written}")

print("\nnew pattern over tracked docs pages (informational):")
files = subprocess.run(["git", "-C", str(clone), "ls-files", "docs/*.md", "docs/**/*.md"],
                       capture_output=True, text=True, check=True).stdout.split()
total = 0
for f in sorted(set(files)):
    n = len(list(g.LINE_CITE_RE.finditer((clone / f).read_text(encoding="utf-8", errors="replace"))))
    total += n
    if f.endswith("SAVED_STATE_FORMAT_32X32.md"):
        print(f"  {f}: {n}")
print(f"  all docs pages: {total} matches in {len(set(files))} files")
