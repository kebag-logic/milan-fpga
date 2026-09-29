#!/usr/bin/env python3
"""Neutralize local path prefixes in the packet's publishable files, then scan them.

Usage: sanitize.py <packet-dir> <checkout-root> <prefix=token>...
Rewrites each listed prefix to its token in every file outside scratch/, then
applies the checkout's own scripts/docs_check.py SCRUB_RULES (identity and
local-info) to every such file and exits 1 on any remaining hit.
"""
import sys
from pathlib import Path

packet, checkout = Path(sys.argv[1]), Path(sys.argv[2])
pairs = [arg.split('=', 1) for arg in sys.argv[3:]]
sys.path.insert(0, str(checkout / 'scripts'))
import docs_check  # noqa: E402

files = [p for p in sorted(packet.rglob('*'))
         if p.is_file() and 'scratch' not in p.relative_to(packet).parts]
hits = 0
for path in files:
    text = path.read_text(errors='surrogateescape')
    new = text
    for prefix, token in sorted(pairs, key=lambda kv: -len(kv[0])):
        new = new.replace(prefix, token)
    if new != text:
        path.write_text(new, errors='surrogateescape')
    for rule in docs_check.SCRUB_RULES:
        pattern, label = rule[0], rule[1]
        for match in pattern.finditer(new):
            hits += 1
            print(f'HIT {path.relative_to(packet)}: {label}: {match.group(0)!r}')
print(f'scanned {len(files)} files, {hits} hit(s)')
sys.exit(1 if hits else 0)
