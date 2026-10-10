#!/usr/bin/env python3
"""Replace host-specific path prefixes in receipts with neutral placeholders, in place.
Each --map PREFIX=LABEL is applied in the order given (longest prefixes first); a home directory
(/home/<user>) left after them becomes <home>.
Usage: sanitize.py --map PREFIX=LABEL [--map ...] -- <file>..."""
import argparse, re
ap = argparse.ArgumentParser()
ap.add_argument("--map", action="append", default=[], metavar="PREFIX=LABEL")
ap.add_argument("files", nargs="+")
args = ap.parse_args()
subs = [(re.escape(p), label) for p, _, label in (m.partition("=") for m in args.map)]
subs.append((r"/home/[^/\s]+", "<home>"))
for name in args.files:
    text = open(name, encoding="utf-8", errors="replace").read()
    new = text
    for pat, rep in subs:
        new = re.sub(pat, rep, new)
    if new != text:
        open(name, "w", encoding="utf-8").write(new)
