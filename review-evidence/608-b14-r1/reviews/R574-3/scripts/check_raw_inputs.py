#!/usr/bin/env python3
"""Cross-check round2-recompute/inputs/raw-inputs.tsv against the archived raw index, and the two
included snapshots against their raw-index digests.
usage: check_raw_inputs.py <author dir at c848925d> <round2-recompute dir at 273764df>"""
import csv, hashlib, json, os, sys
A, R = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(os.path.join(R, 'inputs/raw-inputs.tsv')), delimiter='\t'))
ok = 0
copies = 0
for r in rows:
    line = open(os.path.join(A, 'raw-index', r['index'])).read().splitlines()[int(r['line']) - 1]
    j = json.loads(line)
    if j['sha256'] == r['sha256'] and int(j['bytes']) == int(r['bytes']) and j['path'] == r['published_path']:
        ok += 1
    if r['copy'] != '-':
        d = hashlib.sha256(open(os.path.join(R, 'inputs', r['copy']), 'rb').read()).hexdigest()
        print('copy', r['copy'], 'sha256 equal to raw index:', d == j['sha256'])
        copies += 1
print('rows', len(rows), 'equal to archived raw index (sha256, bytes, path):', ok, 'copies checked:', copies)
