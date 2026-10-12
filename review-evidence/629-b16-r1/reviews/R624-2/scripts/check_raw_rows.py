#!/usr/bin/env python3
"""Check every raw-file row (| `run` | `file`... | bytes | `sha` |) and every
twelve-read row of the B16 sections against RAW-ARTIFACTS.json.
usage: check_raw_rows.py <findings.md> <RAW-ARTIFACTS.json> <start-line>"""
import json, re, sys
doc, raw, start = sys.argv[1], sys.argv[2], int(sys.argv[3])
files = json.load(open(raw))['files']
byhash = {}
for f in files:
    byhash.setdefault(f['sha256'], []).append(f)
row = re.compile(r'^\| ((?:`[^`]+`(?:, )?)+)[^|]*\| `([^`]+)`[^|]*\| ([^|]+) \| `([0-9a-f]{64})` \|$')
src = re.compile(r'^\| `(b16[a-z]?-(?:state|meters)-\d\.json)`[^|]*\| ([0-9:]+) \| `([0-9a-f]{64})` \|$')
ok = bad = 0
for n, line in enumerate(open(doc, encoding='utf-8'), 1):
    if n < start:
        continue
    s = line.strip()
    m = row.match(s)
    if m:
        runs = re.findall(r'`([^`]+)`', m.group(1)); name = m.group(2); size = m.group(3).strip(); sha = m.group(4)
        hits = byhash.get(sha, [])
        good = any(h['path'].split('/')[-1] == name and (isinstance(h['bytes'], str) and size == 'Withheld' or str(h['bytes']) == size.replace(',', '')) and h['path'].split('/')[0] in runs for h in hits)
        print(('OK ' if good else 'BAD') + f' line {n} {runs} {name} {size} {sha[:12]} -> {[ (h["path"], h["bytes"]) for h in hits]}')
        ok += good; bad += not good
        continue
    m = src.match(s)
    if m:
        hits = byhash.get(m.group(3), [])
        good = any(h['path'].endswith(m.group(1)) for h in hits)
        print(('OK ' if good else 'BAD') + f' line {n} {m.group(1)} {m.group(3)[:12]} -> {[h["path"] for h in hits]}')
        ok += good; bad += not good
print(f'ok={ok} bad={bad}')
