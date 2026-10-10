#!/usr/bin/env python3
"""Replace workspace-identifying absolute paths in receipts with neutral placeholders (in place)."""
import gzip, re, sys
from pathlib import Path
# Generic shapes only, most specific first: container tool roots, the review packet and
# clone (any "<name>-packet" / review directory under a reviews tree), other work trees, homes.
SUBS = [(re.compile(r"/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff"), "<tool-root>"),
        (re.compile(r"/data/[^/\s]+/reviews/[^/\s]*-packet"), "<packet>"),
        (re.compile(r"/data/[^/\s]+/reviews/[^/\s]+"), "<clone>"),
        (re.compile(r"/data/[^/\s]+/tools"), "<tools>"),
        (re.compile(r"/data/[^/\s]+"), "<work>"),
        (re.compile(r"/home/[^/\s]+"), "<home>")]
def red(t):
    for rx, s in SUBS: t = rx.sub(s, t)
    return t
for root in sys.argv[1:]:
    for p in Path(root).rglob("*"):
        if not p.is_file(): continue
        if p.suffix == ".gz":
            raw = gzip.decompress(p.read_bytes()).decode("utf-8", "replace"); new = red(raw)
            if new != raw: p.write_bytes(gzip.compress(new.encode(), mtime=0)); print("redacted", p)
            continue
        try: raw = p.read_text()
        except UnicodeDecodeError: continue
        new = red(raw)
        if new != raw: p.write_text(new); print("redacted", p)
