#!/usr/bin/env python3
"""Check the page locator: tool hashes on both pages against the published
author/ packet, raw-artifact rows against author/RAW-ARTIFACTS.json, and both
packet manifests against the files they list.

usage: check_locator.py <repo-at-head> <review-evidence/b3-r1 dir>
"""
import hashlib, json, re, sys
from pathlib import Path

repo, ev = Path(sys.argv[1]), Path(sys.argv[2])
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bad = 0
raw = json.loads((ev / 'author/RAW-ARTIFACTS.json').read_text())
entries = raw['entries']
assert raw['files'] == len(entries), (raw['files'], len(entries))
by_sha = {e.get('sha256'): e for e in entries}
print(f'RAW-ARTIFACTS entries: {len(entries)}')
for page in ('docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md', 'docs/findings/451_USB_AUDIO_CAPTURE.md'):
    text = (repo / page).read_text()
    for m in re.finditer(r'^\| `([\w.]+\.py)`[^|]*\| `([0-9a-f]{64})` \|$', text, re.M):
        name, want = m.groups()
        got = sha(ev / 'author/tools' / name)
        ok = got == want; bad += not ok
        print(f'{page} tool {name}: page {want[:12]} packet {got[:12]} {"MATCH" if ok else "MISMATCH"}')
    for m in re.finditer(r'^\| ([^|]+) \| (\d+) \| `([0-9a-f]{64})` \|$', text, re.M):
        label, size, want = m.groups()
        e = by_sha.get(want)
        ok = e is not None and int(e['bytes']) == int(size)
        if ok:
            print(f'{page} raw "{label.strip()}": {size} B {want[:12]} -> INDEXED {e["path"]}')
        else:
            hits = [str(q.relative_to(ev)) for q in sorted((ev / 'author').rglob('*')) if q.is_file() and want in q.read_text(errors='ignore')]
            print(f'{page} raw "{label.strip()}": {size} B {want[:12]} -> NOTE: not in RAW-ARTIFACTS.json; hash recorded in {hits}')
for man in ('author/MANIFEST.sha256', 'author-r2/packet/MANIFEST.sha256'):
    base = (ev / man).parent
    n = miss = 0
    for line in (ev / man).read_text().splitlines():
        h, p = line.split(None, 1)
        f = base / p.lstrip('*')
        if f.exists():
            n += 1
            if sha(f) != h:
                arch = {e['file']: e for e in json.loads((ev / 'MANIFEST.json').read_text())}
                e = arch.get(str(f.relative_to(ev)))
                if e and e['path_redacted'] and e['original_sha256'] == h and e['published_sha256'] == sha(f):
                    print(f'  {man}: {p} differs by the archiver path redaction recorded in MANIFEST.json (explained)')
                else:
                    miss += 1; print(f'  {man}: HASH MISMATCH {p}')
        else:
            pass
    print(f'{man}: {n} listed files present here checked, {miss} mismatches')
    bad += miss
# Round-2 overlay files against the round-2 manifest
man = (ev / 'author-r2/packet/MANIFEST.sha256').read_text()
for p in ('HANDOFF.md', 'summary/summary.json', 'summary/usb-long-frame-1632.json', 'tools/usb_frame_words.py', 'receipts/mcasp-rx-rate.txt'):
    h = sha(ev / 'author-r2/packet' / p)
    ok = f'{h}  {p}' in man; bad += not ok
    print(f'author-r2/packet/{p}: {h[:12]} {"in manifest" if ok else "NOT IN MANIFEST"}')
print('RESULT', 'PASS' if bad == 0 else f'FAIL ({bad})')
sys.exit(1 if bad else 0)
