#!/usr/bin/env python3
"""Check every packet evidence-file row (`path` | bytes | sha256) in the B16
sections of the findings page against the published packet, accounting for
the publisher's path redaction recorded in MANIFEST.json.
usage: check_doc_hashes.py <findings.md> <packet-root(author-r2)> <MANIFEST.json> <start-line>"""
import hashlib, json, re, sys
doc, root, man, start = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
pub = {e['file'].split('/', 1)[1]: e for e in json.load(open(man)) if e['file'].startswith('author-r2/')}
row = re.compile(r'^\| `([^`]+)`[^|]*\| ([0-9,]+) \| `([0-9a-f]{64})` \|$')
ok = bad = 0
for n, line in enumerate(open(doc, encoding='utf-8'), 1):
    if n < start:
        continue
    m = row.match(line.strip())
    if not m:
        continue
    path, size, sha = m.group(1), int(m.group(2).replace(',', '')), m.group(3)
    try:
        b = open(f'{root}/{path}', 'rb').read()
    except FileNotFoundError:
        # raw files (pcap etc.) are not in the packet; look in RAW-ARTIFACTS
        print(f'RAW? line {n} {path}')
        continue
    h = hashlib.sha256(b).hexdigest()
    e = pub.get(path)
    orig = e['original_sha256'] if e else None
    good = (h == sha and len(b) == size) or (e and e['path_redacted'] and orig == sha)
    print(('OK ' if good else 'BAD') + f' line {n} {path} doc={sha[:12]}/{size} file={h[:12]}/{len(b)} redacted={e and e["path_redacted"]}')
    ok += bool(good); bad += not good
print(f'ok={ok} bad={bad}')
