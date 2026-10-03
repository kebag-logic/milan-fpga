#!/usr/bin/env python3
"""Compare each published record-write receipt's JSON with the committed record at a revision.
Usage: match_record_receipts.py RECEIPT_DIR REV   (run inside the repository)"""
import json, subprocess, sys, pathlib
d, rev = pathlib.Path(sys.argv[1]), sys.argv[2]
base = json.loads(subprocess.check_output(['git', 'show', f'{rev}:syn/ooc/pp_resource_baseline.json']))
ok = True
for ep in ('route-1x1', 'ooc-1x1', 'ooc-8x8'):
    txt = (d / f'record-write-C-{ep}.log').read_text()
    rc = (d / f'record-write-C-{ep}.rc').read_text().strip()
    rec = json.loads(txt[txt.index('\n{') + 1:])
    committed = base['endpoints'][ep]['record']
    same = rec == committed
    ok &= same and rc == '0'
    f = rec['figures']
    print(f'{ep}: receipt rc={rc} record==committed:{same} figures={json.dumps(f)}')
print('ALL MATCH' if ok else 'MISMATCH')
