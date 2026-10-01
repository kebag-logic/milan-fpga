#!/usr/bin/env python3
"""R425-5: the masked RAW-ARTIFACTS.json against the page's artifact table.

Usage: r425_5_rawindex.py <page.md> <author/RAW-ARTIFACTS.json>
Per entry: SHA-256 present, size an integer or withheld, and, where the page
lists the same SHA-256, whether the page's Bytes cell matches or is withheld.
Prints no path, size or value.
"""
import json, re, sys

page, raw = sys.argv[1:3]
d = json.load(open(raw))
ents = d if isinstance(d, list) else next(v for v in d.values() if isinstance(v, list))
rows = {h: b for b, h in re.findall(r'^\| [^|]+ \| (\w+) \| `([0-9a-f]{64})` \|', open(page).read(), re.M)}
ns = nz = nw = 0
for e in ents:
    sha, size = e.get('sha256'), e.get('bytes')
    ok = isinstance(sha, str) and re.fullmatch(r'[0-9a-f]{64}', sha) is not None
    withheld = isinstance(size, str) and size.startswith('<withheld')
    every = bool(re.search(r'all|every', json.dumps(e), re.I))
    ns += ok; nz += isinstance(size, int); nw += withheld
    pg = rows.get(sha)
    st = '-' if pg is None else ('withheld' if pg == 'withheld' else ('match' if str(size) == pg else 'MISMATCH'))
    print(f"sha={'ok' if ok else 'MISSING'} size={'int' if isinstance(size, int) else ('withheld' if withheld else 'OTHER')}"
          f" path-says-every-channel={'yes' if every else 'no'} page_bytes={st}")
print(f'{len(ents)} entries: {ns} with SHA-256, {nz} integer sizes, {nw} withheld')
